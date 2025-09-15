# AGENTS.md

> 🔧 **Migration Notice**: This fork uses uv exclusively and Python 3.13. All commands below use uv instead of Poetry. See [CHANGELOG.md](CHANGELOG.md) for migration details.

## Project Overview

DeepResearchAgent is a hierarchical multi-agent framework designed for general-purpose task solving and deep research. The system uses a conductor-orchestra metaphor where a central planning agent coordinates specialized lower-level agents to tackle complex, multi-step tasks.

**Quick Links:**
- 📚 [Complete Architecture Guide](docs/architecture/OVERVIEW.md)
- ⚡ [Quick Start Guide](docs/usage/QUICK_START.md)
- 🔧 [Environment Setup](docs/setup/ENVIRONMENT_SETUP.md)
- 🤖 [Model Configuration](docs/models/CONFIGURATION.md)

### Core Architecture
- **Two-layer hierarchical structure** with planning and execution agents
- **Asynchronous framework** enabling parallel task execution
- **Tool-based architecture** with pluggable components
- **Multi-provider model support** (OpenAI, Anthropic, Google, Local)

## Quick Setup

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies and setup
uv sync --all-extras
uv run playwright install chromium --with-deps
cp .env.template .env

# Run examples
uv run python main.py
```

**Detailed Setup:** [docs/setup/ENVIRONMENT_SETUP.md](docs/setup/ENVIRONMENT_SETUP.md)

## Essential Commands

### Running
```bash
uv run python main.py                    # Full hierarchical system
uv run python examples/run_general.py   # Single agent
uv run pytest                           # Run tests
```

### Development
```bash
uv add package-name                      # Add dependency
uv sync --all-extras                     # Install dependencies
uv run black . && uv run isort .         # Format code
uv run ruff check .                      # Lint code
```

**Complete Command Reference:** [docs/usage/COMMANDS.md](docs/usage/COMMANDS.md)

## Configuration

### Basic Configuration
```bash
# Use default config
uv run python main.py

# Custom config
uv run python main.py --config configs/config_local_only.py

# Override settings
uv run python main.py --cfg-options agent_config.max_steps=10
```

### Environment Setup
```bash
# Copy template and edit
cp .env.template .env

# Add API keys (choose one or more)
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
GOOGLE_API_KEY=your-google-key-here
```

**Full Configuration Guide:** [docs/models/CONFIGURATION.md](docs/models/CONFIGURATION.md)

## Development

### Code Style & Architecture
- **Modular design**: Agents in `src/agent/`, tools in `src/tools/`
- **Async/await**: All operations use asyncio for concurrency
- **Config-driven**: MMEngine-based configuration system
- **Registry pattern**: Dynamic model and tool registration

**Detailed Guidelines:** [docs/development/CONTRIBUTING.md](docs/development/CONTRIBUTING.md)

### Testing
```bash
uv run pytest                           # Run all tests
uv run python examples/run_gaia.py      # GAIA benchmark
```

**Performance**: 83.39% average on GAIA benchmark

### 🚨 Git Archive Strategy

**EVERY COMMIT** must use archive branches:

```bash
DATETIME=$(date +"%Y%m%d-%H%M%S")
git checkout -b "archive/${DATETIME}-description"
git add . && git commit -m "Message"
git push -u origin "archive/${DATETIME}-description"
git checkout main && git merge "archive/${DATETIME}-description" --no-ff
```

**Full Git Guidelines:** [docs/development/GIT_STRATEGY.md](docs/development/GIT_STRATEGY.md)

## Supported Models

### Commercial APIs
- **OpenAI**: GPT-4.1, GPT-4o, o1, o3
- **Anthropic**: Claude-3.7-Sonnet, Claude-4-Sonnet
- **Google**: Gemini-2.5-Pro

### CLI Tools
- **Claude Code CLI**: `npm install -g @anthropics/claude-code`
- **Gemini CLI**: `gcloud auth application-default login`

### Local Models
- **vLLM**: Qwen 2.5 series (7B, 14B, 32B)
- **HuggingFace**: Direct model loading

**Model Configuration:** [docs/models/CONFIGURATION.md](docs/models/CONFIGURATION.md)

## Security & MCP

### Security Features
- Sandboxed Python execution with configurable restrictions
- Isolated browser instances with automatic cleanup
- API key security and monitoring

### Model Context Protocol
- Dynamic tool discovery and execution
- Local and remote MCP tool integration
- Tool evolution and reuse capabilities

**Security Details:** [docs/security/GUIDELINES.md](docs/security/GUIDELINES.md)

## Troubleshooting

### Quick Fixes
```bash
# Dependency issues
uv sync --reinstall

# Browser automation
uv run playwright install --force

# API validation
uv run python -c "from src.models.api_validator import APIConfigValidator; APIConfigValidator().validate_all_configs()"
```

**Complete Troubleshooting:** [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

## Documentation Structure

- 📁 **[docs/setup/](docs/setup/)** - Installation and environment setup
- 📁 **[docs/usage/](docs/usage/)** - Usage guides and examples
- 📁 **[docs/architecture/](docs/architecture/)** - System architecture and design
- 📁 **[docs/models/](docs/models/)** - Model configuration and integration
- 📁 **[docs/development/](docs/development/)** - Development guidelines and contribution
- 📁 **[docs/security/](docs/security/)** - Security considerations and best practices

**Documentation Index:** [docs/DOCUMENTATION_INDEX.md](docs/DOCUMENTATION_INDEX.md)