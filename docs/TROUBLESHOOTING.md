# Troubleshooting Guide for DeepResearchAgent

This document records problems encountered during setup, testing, and execution, along with steps to resolve them. Please update this file as new issues and solutions are discovered.

## Table of Contents
- [🚨 Emergency Issues](#-emergency-issues)
- [Common Issues](#common-issues)
- [TUI Issues](#tui-issues)
- [Test Logs](#test-logs)
- [Resolutions](#resolutions)
- [References](#references)

---

## 🚨 Emergency Issues

### Terminal Flooded with Mouse Escape Sequences

**⚠️ CRITICAL**: If your terminal is completely unresponsive and flooded with escape sequences like `<35;83;16M`, see the **[Terminal Recovery Guide](TERMINAL_RECOVERY.md)** immediately.

**Quick Emergency Recovery:**
1. **Close terminal window** → Open new terminal (fastest solution)
2. **Rapid Ctrl+C** (press multiple times quickly)
3. **Type quickly:** `./fix` when you get a brief moment
4. **Detailed guide:** [docs/TERMINAL_RECOVERY.md](TERMINAL_RECOVERY.md)

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

## TUI Issues

### TUI Shows Raw Escape Sequences Instead of Interface
- **Symptoms:** When running `uv run python main.py --tui`, you see raw escape codes instead of a clean interface
- **Root Cause:** Not running in a proper TTY environment (IDE terminals, redirected output, etc.)
- **Resolution:**
  ```bash
  # Run in a native terminal application (not IDE terminal)
  uv run python main.py --tui

  # Or use CLI mode instead:
  uv run python main.py --config configs/config_cli_fallback.py
  ```

### TUI Crashes with "NoMatches: No nodes match '#log'"
- **Symptoms:** TUI crashes immediately with traceback about log widget
- **Root Cause:** Widget access before compose() completes
- **Resolution:** This has been fixed - widgets are now accessed in on_mount() instead of compose()

### Mouse Coordinates Appearing in TUI
- **Symptoms:** Raw mouse coordinates like `<35;83;16M` appear in the TUI interface
- **Root Cause:** Mouse tracking not properly disabled
- **Immediate Fix:**
  ```bash
  ./fix
  # OR
  uv run python tools/emergency/fix_mouse.py
  ```
- **Prevention:** This has been fixed with automatic cleanup in main.py

### TUI Not Responding to Keyboard Input
- **Symptoms:** Arrow keys, Enter, shortcuts don't work in TUI
- **Root Cause:** Either TTY issue or event handling problems
- **Debugging Steps:**
  1. Verify you're in a proper terminal (not IDE)
  2. Try `uv run python tools/development/test_minimal_tui.py` to test basic Textual functionality
  3. Check if Ctrl+C works to exit
- **Fallback:** Use CLI mode with `--config configs/config_cli_fallback.py`

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
