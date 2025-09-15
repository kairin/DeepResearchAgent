# Immediate Fixes Required

## 🚨 Critical Issues Identified

Based on the error output you encountered, there are **4 critical issues** that need immediate resolution:

### Issue 1: API Configuration Error 🔥 **BLOCKING**
**Error**: `httpx.UnsupportedProtocol: Request URL is missing an 'http://' or 'https://' protocol`

**Quick Fix**:
```bash
# Your .env file has placeholder values that cause crashes
# Replace xxxxx with actual values OR leave blank to disable

# Edit your .env file:
nano .env

# Either add real API keys:
ANTHROPIC_API_KEY=your_actual_anthropic_key
OPENAI_API_KEY=your_actual_openai_key

# OR comment out to disable:
# ANTHROPIC_API_KEY=xxxxx
# OPENAI_API_KEY=xxxxx
```

### Issue 2: Missing Dependencies ⚠️ **HIGH**
**Errors**:
- `No module named 'pytesseract'`
- `No module named 'CoolProp'`

**Quick Fix**:
```bash
# Install missing dependencies
uv add pytesseract coolprop

# For OCR support (Ubuntu/Debian):
sudo apt-get install tesseract-ocr

# For macOS:
brew install tesseract
```

### Issue 3: Pydantic Warnings ⚠️ **MEDIUM**
**Multiple deprecation warnings from Pydantic v1**

**Quick Fix** (temporary):
```bash
# Suppress warnings temporarily
export PYTHONWARNINGS="ignore::DeprecationWarning"
uv run python main.py
```

### Issue 4: MCP Tool Syntax ⚠️ **MEDIUM**
**Error**: `invalid syntax (<string>, line 69)`

**Quick Fix**: The system will work, some tools may be disabled.

## ⚡ Immediate Action Plan

### Option 1: Quick Start (5 minutes)
```bash
# 1. Fix .env file
cp .env.template .env
# Leave all API keys commented out or blank

# 2. Install missing deps
uv add pytesseract coolprop textual

# 3. Test basic functionality
PYTHONWARNINGS="ignore::DeprecationWarning" uv run python main.py
```

### Option 2: Full Setup (15 minutes)
```bash
# 1. Install CLI tools (recommended)
npm install -g @anthropics/claude-code  # Claude Code CLI
pip install google-generativeai         # Gemini CLI

# 2. Or configure API keys
nano .env
# Add your actual API keys, remove xxxxx placeholders

# 3. Install all dependencies
uv add pytesseract coolprop textual

# 4. Test with full configuration
uv run python main.py
```

## 📋 Phase 1 Implementation Ready

All planning documentation has been completed:

- ✅ **Comprehensive roadmap** with 4-phase implementation
- ✅ **SVG-TUI architecture** designed and documented
- ✅ **Critical issues identified** with detailed solutions
- ✅ **Implementation plan** ready to execute
- ✅ **Testing strategy** and validation criteria established

**Next Steps:**
1. **Resolve the immediate issues** above to get system working
2. **Follow Phase 1 plan** in `docs/planning/phase1/IMMEDIATE_ACTION_PLAN.md`
3. **Begin SVG-TUI development** following the comprehensive planning docs

The system is well-planned and ready for implementation once the current issues are resolved.