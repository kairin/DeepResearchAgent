# Quick Start Guide

Get DeepResearchAgent running in minutes with this step-by-step guide.

## Prerequisites

- **Python 3.8+** (Python 3.13 recommended)
- **Git** for cloning the repository
- **Internet connection** for downloading dependencies

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-org/DeepResearchAgent.git
cd DeepResearchAgent
```

### 2. Install UV Package Manager

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Reload shell or restart terminal
source ~/.bashrc
```

### 3. Install Dependencies

```bash
# Install all dependencies
uv sync --all-extras

# Install browser automation
uv run playwright install chromium --with-deps
```

### 4. Configure Environment

```bash
# Copy environment template
cp .env.template .env

# Edit .env file with your API keys (optional for basic testing)
nano .env
```

## Basic Usage

### Option 1: Use Local Models (No API Keys Required)

```bash
# Run with HuggingFace models (no API keys needed)
uv run python examples/run_general.py
```

### Option 2: Use API Models

Add API keys to `.env` file:

```bash
# Add at least one API key
OPENAI_API_KEY=sk-your-openai-key-here
# or
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
```

Then run:

```bash
# Run full hierarchical system
uv run python main.py
```

## First Example

### Simple Research Task

```bash
# Run a simple research example
uv run python -c "
import asyncio
from src.agent import create_agent
from src.config import config

async def main():
    config.init_config('configs/config_main.py', None)
    agent = await create_agent(config)

    task = 'Search for the latest developments in AI agents and summarize the key findings.'
    result = await agent.run(task)
    print(f'Result: {result}')

asyncio.run(main())
"
```

### Interactive Agent

```bash
# Run interactive example
uv run python examples/run_general.py
```

This will prompt you to enter tasks interactively.

## Available Examples

### Single Agent Examples

```bash
# General-purpose agent
uv run python examples/run_general.py

# Deep research focused
uv run python examples/run_gaia.py

# High-level reasoning
uv run python examples/run_hle.py

# OpenAI deep research
uv run python examples/run_oai_deep_research.py
```

### Hierarchical System

```bash
# Full multi-agent system
uv run python main.py
```

## Configuration Options

### Basic Configuration

```bash
# Use default configuration
uv run python main.py

# Use custom configuration
uv run python main.py --config configs/config_local_only.py

# Override specific settings
uv run python main.py --cfg-options agent_config.max_steps=10
```

### Available Configurations

- `configs/config_main.py` - Default hierarchical setup
- `configs/config_local_only.py` - Local models only
- `configs/config_single_agent.py` - Single agent mode

## Common Tasks

### Research and Analysis

```python
# Example task for research
task = """
Research the latest trends in renewable energy technology.
Focus on:
1. Solar panel efficiency improvements
2. Battery storage innovations
3. Grid integration challenges
Provide a comprehensive summary with sources.
"""
```

### Web Automation

```python
# Example task for web automation
task = """
Navigate to a weather website and extract:
1. Current temperature for New York
2. 5-day forecast
3. Any weather alerts
Present the information in a structured format.
"""
```

### Data Analysis

```python
# Example task for analysis
task = """
Analyze the following data trends:
- Compare performance metrics across different time periods
- Identify patterns and anomalies
- Provide actionable insights
"""
```

## Testing Your Setup

### 1. Dependency Check

```bash
# Verify core dependencies
uv run python -c "
import openai, anthropic, litellm, playwright
print('✅ All core dependencies installed successfully')
"
```

### 2. Model Validation

```bash
# Check model configuration
uv run python -c "
from src.models.api_validator import APIConfigValidator
validator = APIConfigValidator()
results = validator.validate_all_configs()
print('Available providers:', validator.get_available_providers())
"
```

### 3. Run Test Task

```bash
# Simple test with minimal configuration
uv run python -c "
import asyncio
from src.agent.general_tool_calling_agent import GeneralToolCallingAgent

async def test():
    agent = GeneralToolCallingAgent(
        name='test_agent',
        model_id='qwen2.5-7b-instruct',  # Local model, no API key needed
        max_steps=3
    )

    result = await agent.run('What is 2+2? Explain your reasoning.')
    print(f'Test result: {result}')

asyncio.run(test())
"
```

## Troubleshooting

### Common Issues

#### UV Not Found
```bash
# Reload shell configuration
source ~/.bashrc
# or restart terminal

# Check PATH
echo $PATH | grep -o "[^:]*\.local/bin[^:]*"
```

#### Dependency Errors
```bash
# Clean install
uv sync --reinstall

# Check for conflicts
uv lock --check
```

#### Model Loading Errors
```bash
# Check API configuration
uv run python -c "
import os
print('OPENAI_API_KEY:', 'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET')
print('ANTHROPIC_API_KEY:', 'SET' if os.getenv('ANTHROPIC_API_KEY') else 'NOT SET')
"
```

#### Browser Automation Issues
```bash
# Reinstall Playwright
uv run playwright uninstall
uv run playwright install chromium --with-deps
```

### Getting Help

If you encounter issues:

1. **Check Logs**: Look in `workdir/main/log.txt` for detailed error messages
2. **Validate Setup**: Run the test commands above
3. **Documentation**: See [docs/troubleshooting/COMMON_ISSUES.md](../troubleshooting/COMMON_ISSUES.md)
4. **Examples**: Review working examples in `examples/` directory

## Next Steps

After successful setup:

1. **Learn Architecture**: [docs/architecture/OVERVIEW.md](../architecture/OVERVIEW.md)
2. **Explore Examples**: [docs/examples/](../examples/)
3. **Configure Models**: [docs/models/CONFIGURATION.md](../models/CONFIGURATION.md)
4. **Development**: [docs/development/CONTRIBUTING.md](../development/CONTRIBUTING.md)

## Performance Tips

### Faster Execution
- Use API models (GPT-4, Claude) for better performance
- Enable parallel execution with higher concurrency
- Use local models for privacy but expect slower responses

### Resource Optimization
- Close unused browser instances
- Monitor memory usage with large models
- Use appropriate model sizes for your hardware

### Cost Optimization
- Use smaller models for simple tasks
- Implement caching for repeated operations
- Monitor API usage and costs

For detailed performance tuning, see [docs/optimization/PERFORMANCE.md](../optimization/PERFORMANCE.md).