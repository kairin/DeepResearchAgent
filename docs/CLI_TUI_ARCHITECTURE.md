# CLI/TUI Model Integration Architecture

## Overview

This document outlines a flexible architecture for integrating Claude Code and Google Gemini CLI tools with the DeepResearchAgent framework through an intelligent Terminal User Interface (TUI). The approach prioritizes user choice and system adaptability.

## Core Philosophy

### 🎯 **Adaptive Model Selection**
- **Detect what's available** on the user's system
- **Present intelligent recommendations** based on availability
- **Allow user choice** with clear explanations
- **Graceful fallbacks** when preferred options aren't available

### 🧩 **Non-Destructive Integration**
- Keep existing API-based models intact
- Add CLI adapters as new options
- Maintain backward compatibility
- Allow mixed model usage (some agents use API, others use CLI)

## User Experience Flow

### 1. **Initial Startup Detection**
```
🚀 DeepResearchAgent Startup
═══════════════════════════════

🔍 Detecting available model backends...

✅ Found: Claude Code CLI (v1.2.3)
✅ Found: OpenAI API Key configured
❌ Missing: Google Gemini CLI
✅ Found: Local GPU for transformers
⚠️  Missing: Anthropic API Key
```

### 2. **Smart Recommendations TUI**
```
🤖 Choose Your AI Backend
═════════════════════════

Recommended Setup:
┌────────────────────────────────────────┐
│ 💡 OPTIMAL CONFIGURATION              │
├────────────────────────────────────────┤
│ Planning Agent:     Claude Code CLI    │
│ Deep Analyzer:      Claude Code CLI    │
│ Browser Agent:      OpenAI GPT-4       │
│ Deep Researcher:    OpenAI GPT-4       │
└────────────────────────────────────────┘

Available Options:
[1] 🥇 Claude Code CLI       (Best for code/files)
[2] 🥈 OpenAI GPT-4         (Requires API key)
[3] 🥉 Local Transformers   (Slower, private)
[4] 🔧 Custom Configuration

[R] Use Recommended Setup
[Q] Quit

Choice: _
```

### 3. **Agent-Specific Configuration**
```
🎛️  Agent Configuration
════════════════════════

Planning Agent:
  Current: Claude Code CLI ✅
  Alternative: [Change]

Deep Analyzer:
  Current: Claude Code CLI ✅
  Alternative: [Change]

Browser Use Agent:
  Current: OpenAI GPT-4 ✅
  Alternative: [Change]

Deep Researcher:
  Current: OpenAI GPT-4 ✅
  Alternative: [Change]

[S] Save Configuration
[T] Test Configuration
[B] Back to Main Menu
```

### 4. **Runtime Status Display**
```
┌─ DeepResearchAgent Status ─────────────┐
│                                        │
│ 🟢 Planning Agent: Claude Code CLI     │
│ 🟢 Analyzer: Claude Code CLI           │
│ 🟡 Browser: OpenAI API (Rate Limited)  │
│ 🟢 Researcher: OpenAI API              │
│                                        │
│ Active Task: "Research AI Agents"      │
│ Progress: Step 2/5                     │
└────────────────────────────────────────┘
```

## Technical Architecture

### 1. **Model Detection System**

```python
class ModelBackendDetector:
    """Intelligent detection of available model backends"""

    detection_strategies = {
        'claude_code_cli': [
            'claude-code --version',
            'claude --version',
            'which claude-code'
        ],
        'gemini_cli': [
            'gemini --version',
            'gcloud ai --help',
            'google-generativeai --version'
        ],
        'api_keys': [
            'check_env_var("OPENAI_API_KEY")',
            'check_env_var("ANTHROPIC_API_KEY")',
            'validate_api_connectivity()'
        ],
        'local_models': [
            'nvidia-smi',  # GPU check
            'import torch; torch.cuda.is_available()',
            'check_model_cache("/models/")'
        ]
    }
```

### 2. **CLI Adapter Pattern**

```python
class CLIModelAdapter:
    """Base adapter for CLI tools"""

    def __init__(self, command, timeout=300):
        self.command = command
        self.timeout = timeout
        self.session_state = {}

    async def generate(self, messages, tools=None, **kwargs):
        # 1. Format messages for CLI tool
        # 2. Execute CLI command
        # 3. Parse response
        # 4. Handle tool calls
        # 5. Return standardized response
        pass

class ClaudeCodeAdapter(CLIModelAdapter):
    """Specific adapter for Claude Code CLI"""

    def format_for_claude_code(self, messages):
        # Convert agent messages to Claude Code format
        # Handle file references, tool descriptions
        # Manage working directory context
        pass

    def parse_claude_response(self, output):
        # Parse Claude Code output
        # Extract tool calls, file operations
        # Handle errors and retries
        pass

class GeminiCLIAdapter(CLIModelAdapter):
    """Specific adapter for Gemini CLI"""

    def format_for_gemini(self, messages):
        # Convert to Gemini CLI format
        # Handle prompt engineering
        pass
```

### 3. **Intelligent Model Router**

```python
class IntelligentModelRouter:
    """Routes tasks to optimal model backends"""

    routing_rules = {
        'file_operations': 'claude_code_cli',
        'code_analysis': 'claude_code_cli',
        'web_search': 'claude_code_cli',  # Has WebSearch tool
        'general_reasoning': ['api_openai', 'api_anthropic'],
        'creative_writing': ['api_anthropic', 'gemini_cli'],
        'math_computation': ['api_openai', 'local_models'],
    }

    def select_backend(self, task_type, available_backends):
        """Intelligent backend selection based on task"""
        pass
```

### 4. **Configuration Management**

```python
class AdaptiveConfig:
    """Dynamic configuration system"""

    def __init__(self):
        self.user_preferences = {}
        self.detected_backends = {}
        self.agent_assignments = {}

    def generate_optimal_config(self):
        """Generate config based on available backends"""
        pass

    def save_user_preferences(self):
        """Persist user choices"""
        pass

    def handle_backend_failure(self, failed_backend):
        """Automatic failover to backup backends"""
        pass
```

## Implementation Strategy

### Phase 1: Detection & TUI
1. **Backend Detection System**
   - CLI command availability
   - API key validation
   - Local model capability assessment
   - Performance benchmarking

2. **Interactive TUI**
   - Rich terminal interface using `rich` library
   - Clear visual hierarchy
   - Intuitive navigation
   - Real-time status updates

### Phase 2: CLI Adapters
1. **Claude Code Integration**
   - Command formatting strategies
   - Tool call translation
   - File operation handling
   - Session management

2. **Gemini CLI Integration**
   - Multiple CLI options (gemini, gcloud)
   - Response parsing
   - Error handling

### Phase 3: Intelligent Routing
1. **Task Analysis System**
   - Automatic backend selection
   - Performance optimization
   - Failover mechanisms

2. **Mixed Backend Orchestration**
   - Different agents using different models
   - Context passing between backends
   - State management

## Configuration Examples

### Example 1: CLI-First Configuration
```yaml
# config_cli_first.py
agents:
  planning_agent:
    model_backend: "claude_code_cli"
    fallback: "api_openai"

  deep_analyzer_agent:
    model_backend: "claude_code_cli"
    session_persistent: true

  browser_use_agent:
    model_backend: "gemini_cli"
    fallback: "api_google"

  deep_researcher_agent:
    model_backend: "intelligent_router"
    routing_preference: ["claude_code_cli", "api_openai"]
```

### Example 2: Hybrid Configuration
```yaml
# config_hybrid.py
agents:
  planning_agent:
    model_backend: "api_anthropic"  # Best for planning

  deep_analyzer_agent:
    model_backend: "claude_code_cli"  # Best for file ops

  browser_use_agent:
    model_backend: "claude_code_cli"  # Has web tools

  deep_researcher_agent:
    model_backend: "api_openai"  # Best for research
```

### Example 3: Offline-First Configuration
```yaml
# config_offline.py
agents:
  planning_agent:
    model_backend: "local_transformers"

  deep_analyzer_agent:
    model_backend: "claude_code_cli"  # If available
    fallback: "local_vllm"

  browser_use_agent:
    model_backend: "local_vllm"

  deep_researcher_agent:
    model_backend: "local_transformers"
```

## User Experience Benefits

### 🎯 **Intelligent Defaults**
- System automatically recommends optimal configuration
- Clear explanations for each recommendation
- One-click setup for common scenarios

### 🔧 **Flexible Configuration**
- Per-agent model selection
- Mixed backend usage
- Easy switching between configurations

### 📊 **Transparent Operation**
- Real-time backend status
- Performance metrics
- Clear error messages and solutions

### 🚀 **Progressive Enhancement**
- Works with minimal setup (local models)
- Gets better with API keys
- Best experience with CLI tools

## Technical Considerations

### Performance Optimization
- **CLI Session Management**: Keep persistent sessions for better performance
- **Caching**: Cache common responses and tool outputs
- **Parallel Processing**: Use multiple backends simultaneously
- **Smart Routing**: Route tasks to fastest available backend

### Error Handling
- **Graceful Degradation**: Fallback to alternative backends
- **Retry Logic**: Intelligent retry with exponential backoff
- **User Feedback**: Clear error messages with actionable solutions
- **Recovery Strategies**: Automatic failover and recovery

### Security & Privacy
- **Local-First Options**: Support fully offline operation
- **API Key Management**: Secure storage and validation
- **Data Flow Control**: Clear indication of where data goes
- **Permission Management**: Fine-grained access control

### Extensibility
- **Plugin Architecture**: Easy addition of new backends
- **Custom Adapters**: User-defined CLI tool integration
- **Configuration Templates**: Pre-built configurations for common setups
- **Community Configs**: Shareable configuration patterns

This architecture provides a seamless bridge between the existing API-based system and CLI tools while giving users maximum flexibility and control over their AI backend choices.