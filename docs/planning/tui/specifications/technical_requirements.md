# TUI Technical Requirements & Specifications

> **Status**: Planning Document - Implementation Pending
> **Target Framework**: Textual (Rich-based TUI framework)
> **Integration**: DeepResearchAgent Core System

## 🛠️ Technical Stack Analysis

### Framework Selection: Textual

**Primary Reasons for Textual:**

1. **Rich Integration**: Built on Rich library (already used in system)
2. **Widget System**: Complete form controls, buttons, lists, progress bars
3. **CSS-like Styling**: Familiar styling approach
4. **Reactive Programming**: Event-driven architecture matches agent system
5. **Python Native**: No external dependencies or language bridges

**Textual vs. Alternatives:**

| Feature | Textual | Rich (standalone) | Prompt Toolkit |
|---------|---------|-------------------|----------------|
| Complex Layouts | ✅ Excellent | ❌ Limited | ⚠️ Manual |
| Real-time Updates | ✅ Built-in | ✅ Via Live | ⚠️ Complex |
| Form Widgets | ✅ Complete | ❌ None | ✅ Good |
| Styling System | ✅ CSS-like | ✅ Rich syntax | ❌ Manual |
| Performance | ✅ Optimized | ✅ Fast | ✅ Fast |
| Learning Curve | ⚠️ Moderate | ✅ Easy | ❌ Steep |

## 📦 Package Structure

```
src/tui/
├── __init__.py
├── app.py                    # Main TUI application class
├── controllers/
│   ├── __init__.py
│   ├── task_controller.py    # Task management logic
│   ├── agent_controller.py   # Agent interaction logic
│   └── config_controller.py  # Configuration management
├── components/
│   ├── __init__.py
│   ├── dashboard.py          # Main dashboard widget
│   ├── task_input.py         # Task input form widget
│   ├── progress_monitor.py   # Real-time progress widget
│   ├── results_display.py    # Results viewing widget
│   ├── agent_status.py       # Agent status widget
│   └── settings_panel.py     # Settings management widget
├── models/
│   ├── __init__.py
│   ├── task_model.py         # Task data structures
│   ├── progress_model.py     # Progress tracking models
│   └── ui_state.py          # UI state management
├── utils/
│   ├── __init__.py
│   ├── formatters.py         # Text/data formatting utilities
│   ├── validators.py         # Input validation
│   └── svg_renderer.py       # SVG integration utilities
└── styles/
    ├── __init__.py
    ├── themes.py             # Color themes and styles
    └── layouts.py            # Layout configurations
```

## 🔧 Core Component Specifications

### 1. Main Application (app.py)

```python
class DeepResearchTUI(App[None]):
    """Main TUI application class"""

    TITLE = "🤖 DeepResearchAgent"
    SUB_TITLE = "Interactive Research & Analysis Platform"

    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+n", "new_task", "New Task"),
        ("ctrl+h", "show_history", "History"),
        ("ctrl+s", "show_settings", "Settings"),
        ("ctrl+l", "show_logs", "Logs"),
    ]

    CSS_PATH = "styles/default.css"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app"""
        yield Header()
        yield Container(
            Dashboard(id="dashboard"),
            TaskInput(id="task-input"),
            ProgressMonitor(id="progress"),
            ResultsDisplay(id="results"),
            AgentStatus(id="agent-status"),
            SettingsPanel(id="settings"),
            id="main-container"
        )
        yield Footer()
```

### 2. Task Input Component (task_input.py)

```python
class TaskInput(Widget):
    """Task input form with validation and templates"""

    def compose(self) -> ComposeResult:
        yield Static("📝 New Research Task", id="task-header")
        yield TextArea(
            placeholder="Describe your research task...",
            id="task-description"
        )
        yield Horizontal(
            Select([
                ("Research Paper", "research"),
                ("Web Analysis", "web"),
                ("Data Analysis", "data"),
                ("Custom Workflow", "custom")
            ], id="task-template"),
            Select([
                ("Planning + Research", ["planning", "research"]),
                ("Full Analysis", ["planning", "research", "analysis"]),
                ("Web + Browser", ["planning", "research", "browser"]),
                ("Custom Selection", "custom")
            ], id="agent-selection"),
            id="task-options"
        )
        yield Horizontal(
            Button("Start Task", id="start-task", variant="primary"),
            Button("Clear", id="clear-task"),
            Button("Cancel", id="cancel-task"),
            id="task-actions"
        )

    def validate_task(self, description: str) -> tuple[bool, str]:
        """Validate task input"""
        if len(description.strip()) < 10:
            return False, "Task description too short (minimum 10 characters)"

        if len(description) > 2000:
            return False, "Task description too long (maximum 2000 characters)"

        # Additional validation logic
        return True, ""
```

### 3. Progress Monitor Component (progress_monitor.py)

```python
class ProgressMonitor(Widget):
    """Real-time progress tracking with agent status"""

    def __init__(self):
        super().__init__()
        self.task_progress = {}
        self.agent_states = {}
        self.start_time = None

    def compose(self) -> ComposeResult:
        yield Static("🔄 Task Execution Progress", id="progress-header")
        yield Container(
            ProgressBar(total=100, id="overall-progress"),
            Container(id="phase-progress"),
            Container(id="agent-activity"),
            Container(id="live-results"),
            id="progress-content"
        )

    def update_progress(self, phase: str, progress: int, status: str):
        """Update progress for specific phase"""
        self.task_progress[phase] = {
            'progress': progress,
            'status': status,
            'timestamp': time.time()
        }
        self.refresh_display()

    def update_agent_state(self, agent_name: str, state: dict):
        """Update agent execution state"""
        self.agent_states[agent_name] = {
            **state,
            'last_update': time.time()
        }
        self.refresh_agent_display()
```

### 4. Results Display Component (results_display.py)

```python
class ResultsDisplay(Widget):
    """Formatted results viewing with export options"""

    def compose(self) -> ComposeResult:
        yield Static("📊 Task Results", id="results-header")
        yield Tabs(
            "Summary", "Detailed", "Raw Data", "Export",
            id="results-tabs"
        )
        yield Container(
            Markdown(id="results-content"),
            id="results-viewer"
        )
        yield Horizontal(
            Button("📄 Export MD", id="export-md"),
            Button("📋 Copy Text", id="copy-text"),
            Button("🔗 Share", id="share-results"),
            Button("💾 Save File", id="save-file"),
            id="results-actions"
        )

    def display_results(self, results: dict, format_type: str = "markdown"):
        """Display results in specified format"""
        if format_type == "markdown":
            markdown_widget = self.query_one("#results-content", Markdown)
            markdown_widget.update(self.format_as_markdown(results))

    def format_as_markdown(self, results: dict) -> str:
        """Convert results to markdown format"""
        # Implementation for markdown formatting
        pass
```

## 🎨 Styling System

### CSS Theme Structure

```css
/* styles/default.css */

/* Main Application */
App {
    background: $background;
    color: $text;
}

/* Header */
Header {
    dock: top;
    height: 3;
    background: $primary;
    color: $text-primary;
}

/* Dashboard Layout */
#dashboard {
    layout: grid;
    grid-size: 2 2;
    grid-gutter: 1;
    height: 1fr;
}

#quick-actions {
    background: $surface;
    border: solid $border;
    height: 1fr;
}

#recent-tasks {
    background: $surface;
    border: solid $border;
    height: 1fr;
}

#system-status {
    background: $surface;
    border: solid $border;
    height: 1fr;
    column-span: 2;
}

/* Task Input */
#task-input {
    display: none;
    layout: vertical;
    background: $surface;
    border: solid $primary;
    padding: 1;
}

#task-description {
    height: 8;
    background: $input-bg;
    border: solid $input-border;
}

/* Progress Monitor */
#progress {
    display: none;
    layout: vertical;
    background: $surface;
    border: solid $accent;
    padding: 1;
}

.progress-bar {
    height: 1;
    background: $progress-bg;
    color: $progress-fg;
}

.agent-active {
    background: $success;
    color: $success-text;
}

.agent-waiting {
    background: $secondary;
    color: $secondary-text;
}

.agent-error {
    background: $error;
    color: $error-text;
}

/* Results Display */
#results {
    display: none;
    layout: vertical;
    background: $surface;
    border: solid $success;
    padding: 1;
}
```

## 📱 State Management

### UI State Model

```python
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional

class UIMode(Enum):
    DASHBOARD = "dashboard"
    TASK_INPUT = "task_input"
    TASK_EXECUTION = "task_execution"
    RESULTS_VIEW = "results_view"
    SETTINGS = "settings"
    HISTORY = "history"

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class UIState:
    """Central UI state management"""
    current_mode: UIMode = UIMode.DASHBOARD
    current_task_id: Optional[str] = None
    task_history: List[str] = None
    agent_states: Dict[str, dict] = None
    system_status: dict = None
    user_preferences: dict = None

    def __post_init__(self):
        if self.task_history is None:
            self.task_history = []
        if self.agent_states is None:
            self.agent_states = {}
        if self.system_status is None:
            self.system_status = {}
        if self.user_preferences is None:
            self.user_preferences = {}

class StateManager:
    """Centralized state management for TUI"""

    def __init__(self):
        self.state = UIState()
        self.observers = []

    def register_observer(self, callback):
        """Register state change observer"""
        self.observers.append(callback)

    def notify_observers(self, change_type: str, data: dict):
        """Notify all observers of state changes"""
        for callback in self.observers:
            callback(change_type, data)

    def set_mode(self, mode: UIMode):
        """Change UI mode"""
        old_mode = self.state.current_mode
        self.state.current_mode = mode
        self.notify_observers("mode_change", {
            "old_mode": old_mode,
            "new_mode": mode
        })

    def update_agent_state(self, agent_name: str, state_data: dict):
        """Update agent execution state"""
        self.state.agent_states[agent_name] = state_data
        self.notify_observers("agent_state", {
            "agent": agent_name,
            "state": state_data
        })
```

## 🔌 Integration Points

### 1. Core System Integration

```python
class AgentIntegrationBridge:
    """Bridge between TUI and core DeepResearchAgent system"""

    def __init__(self, tui_app, config_path: str):
        self.tui_app = tui_app
        self.config = None
        self.agent = None
        self.model_manager = None

    async def initialize_system(self):
        """Initialize core DeepResearchAgent system"""
        from src.config import config
        from src.models import model_manager
        from src.agent import create_agent

        # Initialize configuration
        config.init_config(config_path)

        # Initialize models
        model_manager.init_models(use_local_proxy=True)

        # Create agent
        self.agent = await create_agent(config)

        self.config = config
        self.model_manager = model_manager

    async def execute_task(self, task_description: str, callback=None):
        """Execute task with progress callbacks"""
        if not self.agent:
            raise RuntimeError("System not initialized")

        try:
            # Set up progress monitoring
            if callback:
                self.agent.set_progress_callback(callback)

            # Execute task
            result = await self.agent.run(task_description)
            return result

        except Exception as e:
            if callback:
                callback("error", {"error": str(e)})
            raise

    def get_system_status(self) -> dict:
        """Get current system status"""
        return {
            "models_registered": len(self.model_manager.registered_models) if self.model_manager else 0,
            "config_loaded": self.config is not None,
            "agent_ready": self.agent is not None,
            "model_aliases": getattr(self.model_manager, 'model_aliases', {})
        }
```

### 2. Progress Monitoring Integration

```python
class ProgressCallbackHandler:
    """Handle progress updates from agent execution"""

    def __init__(self, tui_component):
        self.tui_component = tui_component

    def __call__(self, event_type: str, data: dict):
        """Handle progress callback from agent"""
        if event_type == "agent_start":
            self.tui_component.update_agent_state(
                data["agent_name"],
                {"status": "active", "phase": data.get("phase")}
            )

        elif event_type == "agent_progress":
            self.tui_component.update_progress(
                data["phase"],
                data["progress"],
                data["status"]
            )

        elif event_type == "agent_complete":
            self.tui_component.update_agent_state(
                data["agent_name"],
                {"status": "complete", "result": data.get("result")}
            )

        elif event_type == "error":
            self.tui_component.display_error(data["error"])
```

## 🧪 Testing Strategy

### Unit Testing Structure

```
tests/tui/
├── test_components.py        # Widget unit tests
├── test_controllers.py       # Controller logic tests
├── test_integration.py       # Integration tests
├── test_state_management.py  # State management tests
└── fixtures/
    ├── mock_agents.py        # Mock agent responses
    ├── sample_tasks.py       # Sample task data
    └── ui_test_data.py       # UI testing data
```

### Testing Approach

1. **Component Testing**: Test individual widgets in isolation
2. **Integration Testing**: Test TUI ↔ Core system integration
3. **User Flow Testing**: Test complete user workflows
4. **Performance Testing**: Monitor UI responsiveness during long tasks
5. **Visual Testing**: SVG rendering and display accuracy

## 📊 Performance Requirements

### Response Time Targets

- **UI Mode Switching**: < 100ms
- **Task Input Validation**: < 50ms
- **Progress Updates**: < 200ms refresh rate
- **Results Display**: < 500ms for typical results
- **Agent Status Updates**: < 100ms

### Memory Usage

- **Base TUI**: < 50MB RAM
- **During Task Execution**: < 200MB additional
- **Results Caching**: < 100MB for recent results

### Scalability

- **Task History**: Support 1000+ historical tasks
- **Concurrent Monitoring**: Handle 4+ simultaneous agents
- **Large Results**: Handle results up to 10MB efficiently

## 🔒 Error Handling & Recovery

### Error Categories

1. **System Initialization Errors**
   - Missing configuration
   - Model loading failures
   - Agent creation failures

2. **Task Execution Errors**
   - Agent failures
   - Network timeouts
   - API authentication issues

3. **UI Interaction Errors**
   - Invalid input
   - State corruption
   - Display rendering issues

### Recovery Strategies

1. **Graceful Degradation**: Continue with limited functionality
2. **Auto-retry**: Retry failed operations with backoff
3. **User Notification**: Clear error messages with recovery options
4. **State Recovery**: Restore UI state after errors
5. **Emergency Mode**: Minimal functionality when core systems fail

---

**Note**: This is a technical specification document. Implementation should follow these specifications exactly to ensure system compatibility and performance targets.