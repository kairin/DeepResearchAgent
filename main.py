import argparse
import asyncio
import os
import subprocess
import sys
from pathlib import Path

from mmengine import DictAction
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Header, Footer, Log

root = str(Path(__file__).resolve().parents[0])
sys.path.append(root)

# Apply compatibility fixes early
from src.compat import compatibility_manager
compatibility_manager.apply_compatibility_fixes()

from src.agent import create_agent
from src.config import config
from src.logger import logger
from src.models import model_manager
from src.tui.agent_integration import run_with_tui_progress


def parse_args():
    parser = argparse.ArgumentParser(description='main')
    parser.add_argument("--config", default=os.path.join(root, "configs", "config_main.py"), help="config file path")
    parser.add_argument("--task", type=str, help="Research task to execute")
    parser.add_argument("--no-progress", action="store_true", help="Disable progress display (use logs only)")
    parser.add_argument("--tui", action="store_true", help="Launch TUI mode")

    parser.add_argument(
        '--cfg-options',
        nargs='+',
        action=DictAction,
        help='override some settings in the used config, the key-value pair '
        'in xxx=yyy format will be merged into config file. If the value to '
        'be overwritten is a list, it should be like key="[a,b]" or key=a,b '
        'It also allows nested list/tuple values, e.g. key="[(a,b),(c,d)]" '
        'Note that the quotation marks are necessary and that no white space '
        'is allowed.')
    args = parser.parse_args()
    return args


class DeepResearchTUI(App):
    """TUI for DeepResearchAgent."""

    CSS = """
    Screen {
        layout: vertical;
    }

    Header {
        height: 3;
    }

    Footer {
        height: 3;
    }

    Vertical {
        height: 1fr;
        padding: 1;
    }

    Button {
        width: 100%;
        margin: 0 0 1 0;
    }

    Log {
        height: 1fr;
        border: solid $primary;
        padding: 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("g", "run_general", "Run General Agent"),
        ("a", "run_gaia", "Run Gaia Test"),
        ("o", "run_oai", "Run OAI Deep Research"),
        ("c", "run_cli", "Run CLI Fallback"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Vertical():
            yield Button("Run General Agent (g)", id="run_general")
            yield Button("Run Gaia Test (a)", id="run_gaia")
            yield Button("Run OAI Deep Research (o)", id="run_oai")
            yield Button("Run CLI Fallback (c)", id="run_cli")
            yield Button("Quit (q)", id="quit")
            yield Log(id="log")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        action_map = {
            "run_general": self.run_general_agent,
            "run_gaia": self.run_gaia_test,
            "run_oai": self.run_oai_deep_research,
            "run_cli": self.run_cli_fallback,
            "quit": self.exit,
        }
        if event.button.id in action_map:
            action_map[event.button.id]()

    def action_quit(self) -> None:
        self.exit()

    def action_run_general(self) -> None:
        self.run_general_agent()

    def action_run_gaia(self) -> None:
        self.run_gaia_test()

    def action_run_oai(self) -> None:
        self.run_oai_deep_research()

    def action_run_cli(self) -> None:
        self.run_cli_fallback()

    @work(exclusive=True, thread=True)
    def run_general_agent(self) -> None:
        self._run_agent("examples/run_general.py", "General Agent")

    @work(exclusive=True, thread=True)
    def run_gaia_test(self) -> None:
        self._run_agent("examples/run_gaia.py", "Gaia Test")

    @work(exclusive=True, thread=True)
    def run_oai_deep_research(self) -> None:
        self._run_agent(
            "examples/run_oai_deep_research.py",
            "OAI Deep Research"
        )

    @work(exclusive=True, thread=True)
    def run_cli_fallback(self) -> None:
        self._run_agent(
            "main.py",
            "CLI Fallback",
            ["--config", "configs/config_cli_fallback.py"]
        )

    def _run_agent(
        self, script: str, name: str, args: list[str] | None = None
    ) -> None:
        """Run an agent script in a worker thread to avoid blocking the UI."""
        log = self.query_one("#log", Log)
        log.write(f"Starting {name}...")
        cmd = ["uv", "run", "python", script]
        if args:
            cmd.extend(args)
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent,
                timeout=300  # 5-minute timeout
            )
            if result.returncode == 0:
                log.write(f"✓ {name} completed successfully.")
                if result.stdout.strip():
                    log.write(f"Output: {result.stdout.strip()}")
            else:
                log.write(
                    f"✗ {name} failed with exit code {result.returncode}."
                )
                if result.stderr.strip():
                    log.write(f"Error: {result.stderr.strip()}")
        except subprocess.TimeoutExpired:
            log.write(f"✗ {name} timed out after 5 minutes.")
        except Exception as e:
            log.write(f"✗ {name} encountered an error: {e}")


async def main(args, task: str | None = None):
    try:
        # Initialize the configuration
        config.init_config(args.config, args)

        # Initialize the logger
        logger.init_logger(log_path=config.log_path)
        logger.info(f"| Logger initialized at: {config.log_path}")
        logger.info(f"| Config:\n{config.pretty_text}")

        # Initialize models with validation
        logger.info("| Initializing models...")
        model_manager.init_models(use_local_proxy=True)

        # Display model validation for user
        from src.models.model_validator import validate_and_display_models
        validation_results = validate_and_display_models()

        logger.info(
            "| Model validation complete: %d models available",
            validation_results['summary']['total_models']
        )

    except RuntimeError as e:
        logger.error(f"| Startup failed: {e}")
        logger.error("| Please check your configuration and try again")
        sys.exit(1)
    except Exception as e:
        logger.error(f"| Unexpected error during startup: {e}")
        logger.error("| See logs above for details")
        sys.exit(1)

    # Create agent
    agent = await create_agent(config)
    logger.visualize_agent_tree(agent)

    # Use provided task or command line task or fallback to default
    if task is None:
        task = getattr(args, 'task', None)

    if task is None:
        # Default demo task as fallback
        task = (
            "Use deep_researcher_agent to search the latest papers on the "
            "topic of 'AI Agent' and then summarize it."
        )
        logger.info("| Using default demo task (no custom task provided)")
    else:
        logger.info(f"| Executing custom task: {task[:100]}...")

    # Determine if we should show progress display
    show_progress = not getattr(args, 'no_progress', False)

    if show_progress:
        # Run with TUI progress display
        logger.info("| Starting task execution with progress display...")
        res = await run_with_tui_progress(
            agent,
            task,
            is_hierarchical=True,
            show_progress=True
        )
    else:
        # Run without progress display (traditional logging)
        logger.info("| Starting task execution (logs only)...")
        res = await agent.run(task)

    logger.info(f"| Result: {res}")

if __name__ == '__main__':
    args = parse_args()
    if args.tui:
        app = DeepResearchTUI()
        asyncio.run(app.run_async())
    else:
        asyncio.run(main(args))
