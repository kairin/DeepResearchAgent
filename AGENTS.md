# AGENTS.md

> 🔧 **Migration Notice**: This fork uses uv exclusively and Python 3.13. All commands below use uv instead of Poetry. See [CHANGELOG.md](CHANGELOG.md) for migration details.

## Project Overview

DeepResearchAgent (AgentOrchestra) is a hierarchical multi-agent framework designed for general-purpose task solving and deep research. The system uses a conductor-orchestra metaphor where a central planning agent coordinates specialized lower-level agents to tackle complex, multi-step tasks.

### Architecture
- **Two-layer hierarchical structure** with top-level planning and specialized execution agents
- **Planning Agent**: Decomposes tasks, coordinates workflow, and manages inter-agent communication
- **Specialized Agents**: Deep Analyzer, Deep Researcher, Browser Use, MCP Manager, and General Tool Calling agents
- **Asynchronous framework** enabling efficient parallel task execution

## Development Environment

### Setup Commands
```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Quick setup with uv
uv sync --all-extras
uv run playwright install chromium --with-deps --no-shell

# Or use make commands for full setup
make venv        # Create virtual environment
make install     # Install all dependencies

# Ubuntu 25.04+ with Python 3.13 (Recommended - Default)
make venv-system # Use system Python (preferred)
PYTHON_VERSION=3.13 make venv  # Or specify version explicitly
```

### Environment Configuration
1. Copy `.env.template` to `.env`
2. Configure API keys for supported providers:
   - OpenAI: `OPENAI_API_KEY`
   - Anthropic: `ANTHROPIC_API_KEY`
   - Google: `GOOGLE_API_KEY` and `GOOGLE_APPLICATION_CREDENTIALS`
   - Local models: `QWEN_API_BASE` and `QWEN_API_KEY`

### Local Model Setup (vLLM)
```bash
# Launch vLLM inference service
CUDA_VISIBLE_DEVICES=0,1 python -m vllm.entrypoints.openai.api_server \
  --model /path/to/Qwen3-32B \
  --served-model-name Qwen \
  --host 0.0.0.0 \
  --port 8000 \
  --max-num-seqs 16 \
  --enable-auto-tool-choice \
  --tool-call-parser hermes \
  --tensor_parallel_size 2
```

## Build and Test Commands

### Running the Framework
```bash
# Main example with hierarchical agents
uv run python main.py
# or: make run

# Single agent examples
uv run python examples/run_general.py    # or: make run-general
uv run python examples/run_gaia.py       # or: make run-gaia
uv run python examples/run_hle.py        # or: make run-hle
uv run python examples/run_oai_deep_research.py

# Run tests
uv run pytest                            # or: make test

# Code formatting and linting
uv run black . && uv run isort .         # or: make format
uv run ruff check .                      # or: make lint
uv run ruff check --fix .                # or: make lint-fix
```

### GAIA Benchmark Evaluation
```bash
# Download GAIA dataset
mkdir data && cd data
git clone https://huggingface.co/datasets/gaia-benchmark/GAIA

# Run evaluation
python examples/run_gaia.py
```

### Configuration
- Main config: `configs/config_main.py`
- Use `--config` flag to specify custom config files
- Override settings with `--cfg-options key=value`

### Dependency Management
```bash
# Add new dependency
uv add package-name                      # or: make add PKG=package-name

# Remove dependency
uv remove package-name                   # or: make remove PKG=package-name

# Update all dependencies
uv lock --upgrade                        # or: make update

# Install from lock file only
uv sync --frozen                         # or: make install-locked
```

## 🚨 CRITICAL: Git Archive Strategy (NON-NEGOTIABLE)

### Mandatory Branching Workflow

**EVERY SINGLE COMMIT** must follow this archive-first strategy to protect all work:

```bash
# 1. Create archive branch (NEVER skip this step)
DATETIME=$(date +"%Y%m%d-%H%M%S")
BRANCH_NAME="archive/${DATETIME}-brief-description"
git checkout -b "$BRANCH_NAME"

# 2. Commit and push archive branch
git add . && git commit -m "Commit message"
git push -u origin "$BRANCH_NAME"

# 3. Merge to main
git checkout main && git merge "$BRANCH_NAME" --no-ff
git push origin main
```

### Branch Naming Pattern
- **Format**: `archive/YYYYMMDD-HHMMSS-brief-description`
- **Example**: `archive/20250915-194049-poetry-to-uv-migration-python313`

### Critical Rules
- ✅ **ALWAYS** create archive branch first
- ✅ **ALWAYS** push archive branch to GitHub
- ✅ **NEVER** delete archive branches (permanent history)
- ❌ **NEVER** commit directly to main
- ❌ **NEVER** skip archive branch creation

See [GIT_STRATEGY.md](GIT_STRATEGY.md) for complete documentation.

## Code Style

### Architecture Patterns
- **Modular design**: Each agent type in separate modules under `src/agent/`
- **Async/await**: All agent operations use asyncio for concurrency
- **Tool-based**: Agents interact through standardized tool interfaces
- **Config-driven**: MMEngine-based configuration system

### Key Directories
- `src/agent/`: Agent implementations (planning, deep_researcher, deep_analyzer, etc.)
- `src/tools/`: Tool implementations (web_searcher, python_interpreter, etc.)
- `src/models/`: LLM model adapters (OpenAI, Anthropic, Google, local)
- `src/mcp/`: Model Context Protocol integration
- `configs/`: Configuration files for different use cases

### Agent Development
- Inherit from base classes in `src/base/`
- Implement async `run()` method for task execution
- Use `tool_calling_agent.py` for function calling capabilities
- Follow the registry pattern for model and tool registration

## Testing

### Framework Testing
- Unit tests in `tests/` directory
- Run specific agent tests: `python tests/test_analyzer.py`
- Integration tests use GAIA benchmark for validation

### Supported Models
- **Commercial**: GPT-4.1, Claude-3.7-Sonnet, Gemini-2.5-Pro
- **Local**: Qwen 2.5 series (7B, 14B, 32B) via vLLM or HuggingFace
- **Evaluation**: Function calling works best with GPT-4.1 and Gemini-2.5-Pro

## Security Considerations

### Sandboxed Execution
- Python code execution uses restricted environment with:
  - Configurable import controls
  - Restricted built-ins
  - Attribute access limitations
  - Resource limits
- See `docs/python_interpreter_sandbox.md` for details

### API Security
- Store API keys in `.env` file (never commit to repository)
- Use separate API keys for different environments
- Monitor API usage and rate limits

### Browser Automation
- Browser Use agent operates in isolated browser instances
- Automatic cleanup of browser processes
- Configurable security policies for web interactions

## Model Context Protocol (MCP)

### MCP Integration
- MCP Manager Agent enables dynamic tool discovery and execution
- Supports both local and remote MCP tool integration
- Load local MCP tools from JSON configuration files
- Tool evolution through automated creation, retrieval, and reuse

### Tool Management
- Tools registered in `src/registry.py`
- Custom tools follow the base tool interface
- Async tool execution with proper error handling

## Performance Notes

- **GAIA Benchmark Results**: 83.39% average (93.55% Level 1, 83.02% Level 2, 65.31% Level 3)
- **Asynchronous execution** enables parallel agent operations
- **Hierarchical coordination** reduces redundant computations
- **Tool caching** improves response times for repeated operations

## Troubleshooting

### Common Issues
1. **Browser automation failures**: Reinstall with `uv sync --all-extras`
2. **Model loading errors**: Check API keys and base URLs in `.env`
3. **vLLM issues**: Ensure CUDA setup and model path configuration
4. **MCP connection problems**: Verify MCP server endpoints and authentication

### Debug Mode
- Enable detailed logging in config files
- Use `logger.info()` for debugging agent interactions
- Monitor resource usage during multi-agent execution