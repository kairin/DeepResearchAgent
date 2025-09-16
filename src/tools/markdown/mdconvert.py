import os

from dotenv import load_dotenv

load_dotenv(verbose=True)

import tempfile
from typing import Any

import camelot
from litellm import transcription
from markitdown import MarkItDown
from markitdown._markitdown import (
    MediaConverter,
    DocumentConverterResult,
    PdfConverter,
)

from src.logger import logger
from src.models import model_manager


def read_tables_from_stream(file_stream):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as temp_pdf:
        temp_pdf.write(file_stream.read())
        temp_pdf.flush()
        tables = camelot.read_pdf(temp_pdf.name, flavor="lattice")
        return tables

def transcribe_audio(file_stream, audio_format):

    if "whisper" in model_manager.registed_models:
        # Use the Whisper model for transcription
        model = model_manager.registed_models["whisper"]
        result = model(
            file_stream=file_stream,
        )
    else:
        response = transcription(model="gpt-4o-transcribe", file=file_stream).json()
        result = response.get("text", "No transcription available.")

    return result

class AudioWhisperConverter(MediaConverter):

    def convert(
            self,
            local_path: str,
            **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        md_content = ""

        # Add metadata - for now we'll skip metadata extraction
        # as the exiftool_metadata function API may have changed
        metadata = None
        if metadata:
            for f in [
                "Title",
                "Artist",
                "Author",
                "Band",
                "Album",
                "Genre",
                "Track",
                "DateTimeOriginal",
                "CreateDate",
                # "Duration", -- Wrong values when read from memory
                "NumChannels",
                "SampleRate",
                "AvgBytesPerSec",
                "BitsPerSample",
            ]:
                if f in metadata:
                    md_content += f"{f}: {metadata[f]}\n"

        # Figure out the audio format for transcription from file path
        file_extension = os.path.splitext(local_path)[1].lower()
        if file_extension == ".wav":
            audio_format = "wav"
        elif file_extension == ".mp3":
            audio_format = "mp3"
        elif file_extension in [".mp4", ".m4a"]:
            audio_format = "mp4"
        else:
            audio_format = None

        # Transcribe
        if audio_format:
            try:
                with open(local_path, 'rb') as file_stream:
                    transcript = transcribe_audio(file_stream, audio_format=audio_format)
                    if transcript:
                        md_content += "\n\n### Audio Transcript:\n" + transcript
            except (FileNotFoundError, Exception):
                pass  # Skip transcription if file cannot be read

        # Return the result
        return DocumentConverterResult(markdown=md_content.strip())

class PdfWithTableConverter(PdfConverter):
    def convert(
        self,
        local_path: str,
        **kwargs: Any,  # Options to pass to the converter
    ) -> DocumentConverterResult:
        # Use the parent PdfConverter to get base conversion first
        try:
            base_result = super().convert(local_path, **kwargs)
            base_markdown = base_result.markdown if base_result else ""
        except Exception as e:
            logger.warning(f"Base PDF conversion failed: {e}")
            base_markdown = ""

        # Try to extract tables from the PDF
        try:
            with open(local_path, 'rb') as file_stream:
                tables = read_tables_from_stream(file_stream)
                num_tables = tables.n
                if num_tables == 0:
                    # No tables found, return base markdown
                    return DocumentConverterResult(markdown=base_markdown)
                else:
                    # Tables found, add them to the markdown
                    table_content = ""
                    for i in range(num_tables):
                        table = tables[i].df
                        table_content += f"Table {i + 1}:\n" + table.to_markdown(index=False) + "\n\n"

                    combined_markdown = base_markdown + "\n\n" + table_content
                    return DocumentConverterResult(markdown=combined_markdown)
        except Exception as e:
            logger.warning(f"Table extraction failed: {e}")
            return DocumentConverterResult(markdown=base_markdown)

class MarkitdownConverter:
    def __init__(self,
                 use_llm: bool = False,
                 model_id: str = None,
                 timeout: int = 30):

        self.timeout = timeout
        self.use_llm = use_llm
        self.model_id = model_id

        if use_llm:
            client = model_manager.registed_models(model_id).http_client
            self.client = MarkItDown(
                llm_client=client,
                llm_model=model_id,
            )
        else:
            self.client = MarkItDown()

        removed_converters = [
            PdfConverter
        ]

        self.client._page_converters = [
            converter for converter in self.client._page_converters
            if not isinstance(converter, tuple(removed_converters))
        ]
        self.client.register_page_converter(PdfWithTableConverter())
        self.client.register_page_converter(AudioWhisperConverter())

    def convert(self, source: str, **kwargs: Any):
        try:
            result = self.client.convert(
                source,
                **kwargs)
            return result
        except Exception as e:
            logger.error(f"Error during conversion: {e}")
            return None
