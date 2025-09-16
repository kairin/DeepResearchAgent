# Model Configuration Guide

Comprehensive guide for configuring and using different LLM providers with DeepResearchAgent.

## Overview

DeepResearchAgent uses a **CLI-first model system** that automatically detects and prioritizes available tools:

1. **CLI Tools** (Highest Priority): Claude Code CLI, Gemini CLI
2. **Commercial APIs**: OpenAI, Anthropic, Google AI
3. **Local Models**: vLLM, HuggingFace Transformers
4. **Intelligent Fallbacks**: Automatic model aliasing for missing providers

## CLI-First Architecture

### Priority System
The model system follows this detection and registration order:

1. **CLI Detection**: Automatically detects Claude Code CLI and Gemini CLI
2. **API Validation**: Checks API keys and endpoints for commercial providers
3. **Local Registration**: Registers HuggingFace and vLLM models
4. **Intelligent Aliasing**: Maps missing models to available alternatives

### Model Aliasing
When preferred models aren't available, the system automatically creates aliases:

```
claude-3.7-sonnet-thinking → qwen2.5-32b-instruct
gemini-2.5-pro → qwen2.5-14b-instruct
gpt-4.1, o1, o3 → qwen2.5-32b-instruct
```

## Configuration Methods

### 1. Environment Variables (.env)

**CRITICAL**: Ensure correct spelling for HuggingFace API key:

```bash
# HuggingFace Configuration (Note: Correct spelling!)
HUGGINGFACE_API_KEY=hf_your-huggingface-token-here

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-key-here
OPENAI_API_BASE=https://api.openai.com/v1

# Anthropic Configuration
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
ANTHROPIC_API_BASE=https://api.anthropic.com

# Google AI Configuration
GOOGLE_API_KEY=your-google-ai-key-here
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Local Models
QWEN_API_BASE=http://localhost:8000/v1
QWEN_API_KEY=local-key
```

### 1.1. HuggingFace Integration

DeepResearchAgent uses HuggingFace Inference API for Qwen models with enhanced configuration:

- **Timeout**: 300 seconds (5 minutes) for stability
- **Token Limit**: 4096 tokens maximum
- **Temperature**: 0.1 for consistent tool calling
- **Authentication**: Uses `HUGGINGFACE_API_KEY` environment variable

### 2. Agent Configuration Files

Configure models in agent configuration files:

```python
# configs/config_main.py
planning_agent_config = dict(
    model_id='claude-3.7-sonnet-thinking',  # Anthropic model
    # ... other config
)

deep_researcher_agent_config = dict(
    model_id='gpt-4.1',  # OpenAI model
    # ... other config
)
```

### 3. Runtime Configuration

Override models at runtime:

```bash
# Override model for specific agent
uv run python main.py --cfg-options planning_agent_config.model_id=gpt-4o

# Override multiple models
uv run python main.py --cfg-options \
    planning_agent_config.model_id=claude37-sonnet \
    deep_researcher_agent_config.model_id=gemini-2.5-pro
```

## CLI Tools Setup (Recommended)

### Claude Code CLI

Claude Code CLI provides the best integration with Anthropic models.

#### Installation
```bash
# Install Claude Code CLI globally
npm install -g @anthropics/claude-code

# Verify installation
claude-code --version
```

#### Authentication
Follow the official Claude Code CLI authentication setup.

#### Benefits
- Direct integration with Claude models
- Better tool calling support
- No API rate limits (uses your Claude subscription)
- Enhanced coding capabilities

### Gemini CLI

#### Installation
```bash
# Install Google Cloud SDK
# See: https://cloud.google.com/sdk/docs/install

# Install Google Generative AI library
uv add google-generativeai

# Authenticate
gcloud auth application-default login
```

#### Verification
```bash
# Check authentication
gcloud auth list

# Test Gemini access
python -c "import google.generativeai; print('✓ Gemini CLI ready')"
```

### CLI Detection Results

The system automatically detects CLI tools on startup:

```
INFO     [src.models.cli_detector] CLI Tool Detection Results:
✅ claude_code_cli: Available (Version: 1.2.3)
✅ gemini_cli: Available (Account: user@gmail.com)

Available CLI model mappings:
  claude-3.7-sonnet-thinking → claude-code-cli
  gemini-2.5-pro → gemini-cli
```

### CLI Fallback Configuration

Use the CLI-first configuration for automatic fallbacks:

```bash
# Run with CLI-first priority
uv run python main.py --config configs/config_cli_fallback.py
```

## Provider-Specific Setup

### OpenAI Models

#### Available Models
- `gpt-4o` - Latest GPT-4 model
- `gpt-4.1` - Enhanced GPT-4 version
- `o1` - Reasoning-focused model
- `o3` - Latest reasoning model

#### Setup
```bash
# Get API key from https://platform.openai.com
export OPENAI_API_KEY=sk-your-key-here

# Optional: Custom base URL
export OPENAI_API_BASE=https://api.openai.com/v1
```

#### Example Configuration
```python
# In config file
model_config = dict(
    model_id='gpt-4o',
    api_key=os.getenv('OPENAI_API_KEY'),
    api_base=os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1'),
    max_tokens=4000,
    temperature=0.7
)
```

### Anthropic Models

#### Available Models
- `claude37-sonnet` - Claude 3.7 Sonnet
- `claude-3.7-sonnet-thinking` - Enhanced reasoning version
- `claude-4-sonnet` - Latest Claude 4

#### Setup
```bash
# Get API key from https://console.anthropic.com
export ANTHROPIC_API_KEY=sk-ant-your-key-here

# Optional: Custom base URL
export ANTHROPIC_API_BASE=https://api.anthropic.com
```

#### Example Configuration
```python
# In config file
model_config = dict(
    model_id='claude-3.7-sonnet-thinking',
    api_key=os.getenv('ANTHROPIC_API_KEY'),
    max_tokens=8000,
    temperature=0.1  # Lower temperature for reasoning tasks
)
```

### Google AI Models

#### Available Models
- `gemini-2.5-pro` - Latest Gemini Pro model
- `gemini-vision` - Multimodal capabilities

#### Setup Method 1: API Key
```bash
# Get API key from https://aistudio.google.com
export GOOGLE_API_KEY=your-google-ai-key-here
```

#### Setup Method 2: Service Account
```bash
# Download service account JSON from Google Cloud Console
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Or use gcloud CLI
gcloud auth application-default login
```

#### Example Configuration
```python
# In config file
model_config = dict(
    model_id='gemini-2.5-pro',
    api_key=os.getenv('GOOGLE_API_KEY'),
    # or use service account credentials automatically
)
```

### CLI Tools Integration

#### Claude Code CLI

##### Installation
```bash
# Install via npm
npm install -g @anthropics/claude-code

# Verify installation
claude-code --version
```

##### Usage
```python
# No additional configuration needed
# CLI tool is detected automatically
model_config = dict(
    model_id='claude-code-cli',
    # CLI handles authentication
)
```

#### Gemini CLI

##### Installation
```bash
# Install Google AI CLI
pip install google-generativeai

# Authenticate
gcloud auth application-default login
```

##### Usage
```python
# Uses gcloud authentication automatically
model_config = dict(
    model_id='gemini-cli',
    # CLI handles authentication
)
```

### Local Models

#### vLLM Setup

##### Installation
```bash
# Install vLLM
uv add vllm torch

# For GPU support
uv add vllm[cuda]
```

##### Server Launch
```bash
# Launch Qwen model
CUDA_VISIBLE_DEVICES=0,1 python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-32B-Instruct \
  --served-model-name Qwen \
  --host 0.0.0.0 \
  --port 8000 \
  --max-num-seqs 16 \
  --enable-auto-tool-choice \
  --tool-call-parser hermes \
  --tensor-parallel-size 2
```

##### Configuration
```bash
# Configure local server
export QWEN_API_BASE=http://localhost:8000/v1
export QWEN_API_KEY=local-key  # Can be any string
```

#### HuggingFace Models

##### Available Models
- `qwen2.5-7b-instruct` - 7B parameter model
- `qwen2.5-14b-instruct` - 14B parameter model
- `qwen2.5-32b-instruct` - 32B parameter model

##### Usage
```python
# No setup required, downloads automatically
model_config = dict(
    model_id='qwen2.5-7b-instruct',
    # Model downloads from HuggingFace Hub
)
```

## Model Selection Strategies

### Task-Based Selection

#### Planning Tasks
- **Best**: `claude-3.7-sonnet-thinking` - Superior reasoning
- **Alternative**: `gpt-4o` - Good general performance
- **Local**: `qwen2.5-32b-instruct` - Best local option

#### Research Tasks
- **Best**: `gpt-4.1` - Excellent web research
- **Alternative**: `gemini-2.5-pro` - Good synthesis
- **Local**: `qwen2.5-14b-instruct` - Adequate for basic research

#### Analysis Tasks
- **Best**: `claude37-sonnet` - Deep analytical reasoning
- **Alternative**: `o1` - Strong logical reasoning
- **Local**: `qwen2.5-32b-instruct` - Best local analysis

#### Web Automation
- **Best**: `gpt-4.1` - Excellent UI understanding
- **Alternative**: `gemini-vision` - Good visual understanding
- **Local**: Limited support for visual tasks

### Performance vs Cost

#### High Performance (Expensive)
```python
config = dict(
    planning_agent='claude-3.7-sonnet-thinking',
    deep_researcher='gpt-4.1',
    deep_analyzer='claude37-sonnet',
    browser_agent='gpt-4.1'
)
```

#### Balanced Performance
```python
config = dict(
    planning_agent='gpt-4o',
    deep_researcher='gemini-2.5-pro',
    deep_analyzer='claude37-sonnet',
    browser_agent='gpt-4o'
)
```

#### Cost Optimized
```python
config = dict(
    planning_agent='qwen2.5-32b-instruct',
    deep_researcher='qwen2.5-14b-instruct',
    deep_analyzer='qwen2.5-32b-instruct',
    browser_agent='qwen2.5-7b-instruct'
)
```

## Advanced Configuration

### Load Balancing

```python
# Multiple models for the same task
deep_analyzer_tool_config = dict(
    analyzer_model_ids=[
        'claude37-sonnet',
        'gpt-4o',
        'gemini-2.5-pro'
    ],
    # Automatically load balances across models
)
```

### Fallback Configuration

```python
# Primary model with fallbacks
model_config = dict(
    primary_model='claude-3.7-sonnet-thinking',
    fallback_models=[
        'gpt-4o',
        'qwen2.5-32b-instruct'
    ]
)
```

### Custom Model Providers

```python
# Add custom provider
from src.models.custom_provider import CustomModel

# Register custom model
model_manager.register_model('custom-model', CustomModel(
    api_base='https://your-api.com/v1',
    api_key='your-key',
    model_id='your-model-id'
))
```

## Validation and Testing

### Configuration Validation

```bash
# Validate all configurations
uv run python -c "
from src.models.api_validator import APIConfigValidator
validator = APIConfigValidator()
results = validator.validate_all_configs()
print(validator.get_configuration_guidance())
"
```

### Model Testing

```bash
# Test specific model
uv run python -c "
import asyncio
from src.models import model_manager

async def test_model():
    model_manager.init_models()
    model = model_manager.registered_models['gpt-4o']
    response = await model.acompletion('Hello, how are you?')
    print(f'Response: {response}')

asyncio.run(test_model())
"
```

### Performance Benchmarking

```bash
# Run GAIA benchmark
uv run python examples/run_gaia.py --model-id gpt-4o

# Compare models
uv run python scripts/benchmark_models.py \
    --models gpt-4o,claude37-sonnet,qwen2.5-32b-instruct
```

## Troubleshooting

### Common Issues

#### API Key Errors
```bash
# Check API key format
uv run python -c "
import os
key = os.getenv('OPENAI_API_KEY', '')
print(f'Key length: {len(key)}')
print(f'Key format: {key[:7]}...{key[-4:] if len(key) > 10 else key}')
"
```

#### Model Not Found
```bash
# List available models
uv run python -c "
from src.models import model_manager
model_manager.init_models()
print('Available models:', list(model_manager.registered_models.keys()))
"
```

#### Rate Limiting
```python
# Configure rate limiting
model_config = dict(
    model_id='gpt-4o',
    rate_limit=10,  # requests per minute
    retry_attempts=3
)
```

### Debug Mode

```bash
# Enable detailed model logging
export DEBUG=true
export MODEL_DEBUG=true

# Run with debug output
uv run python main.py
```

## Best Practices

### Security
- Never commit API keys to version control
- Use environment variables for sensitive data
- Rotate API keys regularly
- Monitor API usage for anomalies

### Performance
- Use appropriate model sizes for tasks
- Implement caching for repeated requests
- Monitor token usage and costs
- Use parallel execution when possible

### Reliability
- Implement proper error handling
- Use fallback models for critical tasks
- Monitor model availability
- Set reasonable timeout values

## Troubleshooting

### Common Issues

#### 1. HuggingFace API Key Error
**Problem**: `HUGGINGFACE_API_KEY appears too short` or authentication failures

**Solution**:
```bash
# Ensure correct spelling (common typo: HUGGINEFACE_API_KEY)
HUGGINGFACE_API_KEY=hf_your-token-here

# Verify token format (should start with hf_)
# Get token from: https://huggingface.co/settings/tokens
```

#### 2. KeyError: 'model-name'
**Problem**: `KeyError: 'gemini-2.5-pro'` or similar model not found errors

**Solution**: The CLI-first system automatically handles this with model aliasing. If you see this error:
```bash
# Use CLI-first configuration
uv run python main.py --config configs/config_cli_fallback.py

# Or install the missing CLI tool:
npm install -g @anthropics/claude-code  # For Claude models
uv add google-generativeai              # For Gemini models
```

#### 3. HuggingFace 504 Gateway Timeout
**Problem**: `504 Server Error: Gateway Time-out` from HuggingFace

**Solutions**:
- **Temporary issue**: Retry after a few minutes (HuggingFace endpoint overloaded)
- **Persistent issue**: Switch to CLI tools or local models
- **Configuration**: The system now uses 300s timeout (increased from 120s)

#### 4. CLI Tool Not Detected
**Problem**: `❌ claude_code_cli: claude-code command not found`

**Solution**:
```bash
# Install CLI tools
npm install -g @anthropics/claude-code
uv add google-generativeai

# Verify installation
claude-code --version
python -c "import google.generativeai"
```

#### 5. Tool Call Parsing Errors
**Problem**: `Error while parsing tool call from model output: 'function'`

**Solution**: The system now uses lower temperature (0.1) for more consistent tool calling. If issues persist:
```python
# In model configuration, ensure:
temperature=0.1          # Lower temperature
max_tokens=4096         # Sufficient token limit
timeout=300             # Extended timeout
```

### Model Aliasing Reference

When models are unavailable, the system automatically creates these aliases:

| Requested Model | Fallback Model | Provider |
|----------------|----------------|----------|
| `claude-3.7-sonnet-thinking` | `qwen2.5-32b-instruct` | HuggingFace |
| `claude37-sonnet` | `qwen2.5-32b-instruct` | HuggingFace |
| `gemini-2.5-pro` | `qwen2.5-14b-instruct` | HuggingFace |
| `gpt-4.1`, `o1`, `o3` | `qwen2.5-32b-instruct` | HuggingFace |

### Debug Mode

Enable detailed logging for troubleshooting:

```bash
# Set debug environment
export DEBUG=true

# Run with verbose output
uv run python main.py --config configs/config_cli_fallback.py
```

For additional configuration examples and advanced setups, see:
- [Model Integration Examples](../examples/MODEL_INTEGRATION.md)
- [Custom Provider Development](../development/CUSTOM_PROVIDERS.md)
- [Performance Optimization](../optimization/MODEL_PERFORMANCE.md)