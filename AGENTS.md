# AGENTS.md

> 🔧 **Migration Notice**: This fork uses uv exclusively and Python 3.13. All commands below use uv instead of Poetry. See [CHANGELOG.md](CHANGELOG.md) for migration details.

## Project Overview

DeepResearchAgent is a hierarchical multi-agent framework for complex task solving and deep research. A central planning agent coordinates specialized execution agents using an async, tool-based architecture with multi-provider model support.

**Quick Links:** [Architecture](docs/architecture/OVERVIEW.md) • [Quick Start](docs/usage/QUICK_START.md) • [Setup](docs/setup/ENVIRONMENT_SETUP.md) • [Models](docs/models/CONFIGURATION.md)

## Quick Setup

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies and setup
uv sync --all-extras
uv run playwright install chromium --with-deps
cp .env.template .env

# Run examples
uv run python main.py --tui    # Interactive TUI launcher
uv run python main.py          # Default agent run
```

**Detailed Setup:** [docs/setup/ENVIRONMENT_SETUP.md](docs/setup/ENVIRONMENT_SETUP.md)

## Essential Commands

### Running
```bash
uv run python main.py --tui                              # TUI launcher (interactive menu)
uv run python main.py --config configs/config_cli_fallback.py  # CLI-first (recommended)
uv run python main.py                                          # Full hierarchical system
uv run python examples/run_general.py                          # Single agent
uv run pytest                                                  # Run tests
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
```bash
# CLI-first (recommended for max subscriptions)
claude                                    # Local Claude Code CLI
gcloud cloud-shell ssh && gemini         # Google Cloud Shell Gemini
uv run python main.py --config configs/config_cli_fallback.py

# Local-only setup (offline development)
uv run python main.py --config configs/config_local_only.py
# Requires HUGGINGFACE_API_KEY in .env for model access

# Override settings
uv run python main.py --cfg-options agent_config.max_steps=10

# Environment setup
cp .env.template .env
# Configure as needed: HUGGINGFACE_API_KEY, optional: OPENAI_API_KEY, ANTHROPIC_API_KEY
```

**Full Guide:** [docs/models/CONFIGURATION.md](docs/models/CONFIGURATION.md)

## Development

### Architecture & Testing
- **Modular**: Agents in `src/agent/`, tools in `src/tools/`
- **Async**: All operations use asyncio
- **Config-driven**: MMEngine configuration system
- **Performance**: 83.39% GAIA benchmark average

```bash
uv run pytest                          # Run tests
uv run python examples/run_gaia.py     # GAIA benchmark
```

**Guidelines:** [docs/development/CONTRIBUTING.md](docs/development/CONTRIBUTING.md)

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

## Models
Connected models are validated at startup. Typical configuration includes:
- **CLI Tools**: Claude Code (`claude` command), Gemini (via `gcloud cloud-shell ssh`)
- **Local Models**: Qwen 2.5 series (7B/14B/32B) via HuggingFace API
- **Routing**: Primary CLI access with local model fallbacks

**Configuration:** [docs/models/CONFIGURATION.md](docs/models/CONFIGURATION.md)

## Security & MCP
- **Sandboxed execution**: Python restrictions, isolated browsers, API monitoring
- **MCP integration**: Dynamic tool discovery, local/remote tools, evolution

**Details:** [docs/security/GUIDELINES.md](docs/security/GUIDELINES.md)

## Troubleshooting

```bash
uv sync --reinstall                     # Fix dependencies
uv run playwright install --force       # Fix browser automation

# Model validation (shows actual connected models)
uv run python -c "from src.models.model_validator import validate_and_display_models; validate_and_display_models()"

# API validation
uv run python -c "from src.models.api_validator import APIConfigValidator; APIConfigValidator().validate_all_configs()"
```

**Full Guide:** [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

## Documentation
[Setup](docs/setup/) • [Usage](docs/usage/) • [Architecture](docs/architecture/) • [Models](docs/models/) • [Development](docs/development/) • [Security](docs/security/)

**Index:** [docs/DOCUMENTATION_INDEX.md](docs/DOCUMENTATION_INDEX.md)