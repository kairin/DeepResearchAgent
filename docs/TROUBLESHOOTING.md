# Troubleshooting Guide for DeepResearchAgent

This document records problems encountered during setup, testing, and execution, along with steps to resolve them. Please update this file as new issues and solutions are discovered.

## Table of Contents
- [Common Issues](#common-issues)
- [Test Logs](#test-logs)
- [Resolutions](#resolutions)
- [References](#references)

---

## Common Issues

### 1. Missing Python Modules
- **Symptoms:** Errors like `No module named 'pytesseract'` or `No module named 'CoolProp'` during execution.
- **Resolution:**
  ```bash
  uv pip install pytesseract CoolProp
  ```

### 2. Deprecation Warnings
- **Symptoms:** Warnings from Pydantic or aifc about deprecated features.
- **Resolution:**
  - These are not fatal but should be addressed for long-term stability. Update dependencies or code as needed.

### 3. Connection Errors / API Misconfiguration
- **Symptoms:**
  - `httpx.UnsupportedProtocol: Request URL is missing an 'http://' or 'https://' protocol.`
  - `openai.APIConnectionError: Connection error.`
- **Resolution:**
  - Check your `.env` file for correct API keys and endpoint URLs.
  - Ensure all required environment variables are set.

### 4. MarkItDown Constructor Error
- **Symptoms:** `TypeError: MarkItDown.__init__() got an unexpected keyword argument 'enable_plugins'`
- **Resolution:**
  - Remove the `enable_plugins` argument from the MarkItDown constructor in `src/tools/markdown/mdconvert.py`.

---

## Test Logs

### Example Test Run (2025-09-15)
- App started, loaded config, initialized agents.
- Encountered missing modules and deprecation warnings.
- Main error: Connection error due to misconfigured API endpoint.
- All errors were real, not hardcoded.

---

## Resolutions
- See above for step-by-step fixes.
- For persistent issues, consult the [README.md](../README.md) and [AGENTS.md](../AGENTS.md).

---

## References
- [AGENTS.md](../AGENTS.md)
- [README.md](../README.md)
- [docs/README.md](README.md)

---

For further troubleshooting, add new issues and solutions below as they are discovered.
