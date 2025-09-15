# Environment Setup Guide

Complete guide for setting up DeepResearchAgent development environment.

## Quick Start

For immediate setup, run these commands:

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Quick setup with uv
uv sync --all-extras
uv run playwright install chromium --with-deps --no-shell

# Copy environment template
cp .env.template .env
```

## System Requirements

### Minimum Requirements
- **Python**: 3.8+ (Python 3.13 recommended)
- **Package Manager**: UV (latest version)
- **Operating System**: Linux, macOS, or Windows with WSL2
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 2GB free space for dependencies

### Recommended Tools
- **Git**: For version control
- **Node.js & npm**: For Claude Code CLI installation
- **gcloud CLI**: For Google AI integration
- **Docker**: For containerized deployment (optional)

## Installation Methods

### Method 1: UV (Recommended)

UV is the modern, fast Python package manager that handles virtual environments automatically.

```bash
# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc  # or restart terminal

# Verify installation
uv --version

# Install all dependencies
uv sync --all-extras

# Install browser automation
uv run playwright install chromium --with-deps
```

### Method 2: Make Commands

The project includes convenient Make targets:

```bash
# Create virtual environment
make venv

# Install all dependencies
make install

# For Ubuntu 25.04+ with Python 3.13 (recommended)
make venv-system

# Specify Python version explicitly
PYTHON_VERSION=3.13 make venv
```

## Environment Configuration

### 1. Create Environment File

```bash
cp .env.template .env
```

### 2. Configure API Keys

Edit `.env` file and add your API keys:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-key-here
OPENAI_API_BASE=https://api.openai.com/v1

# Anthropic Configuration
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
ANTHROPIC_API_BASE=https://api.anthropic.com

# Google AI Configuration
GOOGLE_API_KEY=your-google-ai-key-here
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Firecrawl for Web Scraping
FIRECRAWL_API_KEY=your-firecrawl-key-here

# Optional: Local Models
QWEN_API_BASE=http://localhost:8000/v1
QWEN_API_KEY=local-key
```

### 3. Backend Options

Choose one or more backend options:

#### Option A: API Keys (Simplest)
Add API keys to `.env` file as shown above.

#### Option B: CLI Tools (Recommended)
Install CLI tools for better performance:

```bash
# Claude Code CLI
npm install -g @anthropics/claude-code

# Google AI CLI
pip install google-generativeai
gcloud auth application-default login
```

#### Option C: Local Models
Set up local model server using vLLM:

```bash
# Install vLLM
uv add vllm

# Launch local server (example with Qwen)
CUDA_VISIBLE_DEVICES=0,1 python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-32B-Instruct \
  --served-model-name Qwen \
  --host 0.0.0.0 \
  --port 8000 \
  --max-num-seqs 16 \
  --enable-auto-tool-choice \
  --tool-call-parser hermes \
  --tensor_parallel_size 2
```

## Dependency Management

### Core Dependencies

All dependencies are automatically managed through `pyproject.toml`. The system includes:

- **Framework**: MMEngine, Pydantic, Python-dotenv
- **LLM Integration**: OpenAI, Anthropic, Google AI, LiteLLM
- **Web Automation**: Playwright, Browser-use, Firecrawl
- **Data Processing**: Pandas, NumPy, Beautiful Soup
- **Optional Features**: OCR (pytesseract), TUI (textual), Science (coolprop)

### Adding Dependencies

```bash
# Add new dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Add optional dependency group
uv add --optional-group=tui textual cairosvg
```

### Dependency Updates

```bash
# Update all dependencies
uv lock --upgrade

# Sync from lock file only (production)
uv sync --frozen

# Install with specific extras
uv sync --extra=dev --extra=tui
```

## Verification

### 1. Test Basic Setup

```bash
# Test dependency installation
uv run python -c "import openai, anthropic, litellm; print('✅ Core dependencies OK')"

# Test browser automation
uv run python -c "import playwright; print('✅ Browser automation OK')"

# Test optional features
uv run python -c "import pytesseract, coolprop, textual; print('✅ Optional features OK')"
```

### 2. Test Configuration

```bash
# Run with validation
uv run python main.py --help

# Test specific configuration
uv run python main.py --config configs/config_local_only.py
```

### 3. Run Example

```bash
# Simple agent example
uv run python examples/run_general.py

# Full hierarchical system
uv run python main.py
```

## Troubleshooting

### Common Issues

#### UV Installation
```bash
# If UV not found, reload shell
source ~/.bashrc
# or restart terminal

# Manual PATH setup
export PATH="$HOME/.local/bin:$PATH"
```

#### Dependency Conflicts
```bash
# Reset virtual environment
uv venv --clear

# Clean install
uv sync --reinstall
```

#### Browser Automation
```bash
# Reinstall Playwright browsers
uv run playwright install --force

# Install system dependencies (Ubuntu/Debian)
sudo apt-get install -y \
    libnss3 libatk-bridge2.0-0 libdrm2 libxkbcommon0 \
    libgtk-3-0 libgbm1 libasound2
```

#### API Configuration
```bash
# Validate configuration
uv run python -c "
from src.models.api_validator import APIConfigValidator
validator = APIConfigValidator()
results = validator.validate_all_configs()
print(validator.get_configuration_guidance())
"
```

### Platform-Specific Setup

#### Ubuntu/Debian
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y \
    python3-dev python3-pip \
    tesseract-ocr \
    libcairo2-dev libgirepository1.0-dev \
    build-essential

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### macOS
```bash
# Install Homebrew dependencies
brew install tesseract cairo pkg-config

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows (WSL2)
```bash
# Use Ubuntu setup in WSL2
# Ensure Docker Desktop is running for container features
```

## Performance Optimization

### Hardware Recommendations

- **CPU**: Multi-core processor (8+ cores for parallel agents)
- **GPU**: NVIDIA GPU with 8GB+ VRAM for local models
- **Memory**: 16GB+ RAM for large models
- **Storage**: SSD recommended for faster I/O

### Environment Variables

```bash
# Python optimizations
export PYTHONPATH="${PYTHONPATH}:/path/to/project"
export PYTHONUNBUFFERED=1

# Parallel processing
export UV_CONCURRENT_INSTALLS=8
export PLAYWRIGHT_BROWSERS_PATH=/opt/playwright

# GPU configuration (if available)
export CUDA_VISIBLE_DEVICES=0,1
export TORCH_USE_CUDA_DSA=1
```

## Security Considerations

### Environment Protection

```bash
# Set secure permissions for .env
chmod 600 .env

# Exclude from git
echo ".env" >> .gitignore
```

### API Key Security

- Never commit API keys to version control
- Use separate keys for development/production
- Rotate keys regularly
- Monitor API usage for anomalies

### Network Security

- Use HTTPS endpoints only
- Configure firewall for local model servers
- Implement rate limiting for production deployments

## Next Steps

After successful setup:

1. **Read Architecture Guide**: [docs/architecture/OVERVIEW.md](../architecture/OVERVIEW.md)
2. **Try Examples**: [docs/examples/GETTING_STARTED.md](../examples/GETTING_STARTED.md)
3. **Configure Models**: [docs/models/CONFIGURATION.md](../models/CONFIGURATION.md)
4. **Development Setup**: [docs/development/CONTRIBUTING.md](../development/CONTRIBUTING.md)

For complete troubleshooting, see [TROUBLESHOOTING.md](../TROUBLESHOOTING.md).