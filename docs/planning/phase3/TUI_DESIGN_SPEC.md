# TUI Design Specification - SVG-Enhanced Interface

## 🎯 Objective
Design a beautiful, intuitive TUI using Textual framework with parallel SVG rendering capability for LLM visual understanding and enhanced user experience.

## 📋 Scope
This specification covers the complete TUI design including visual hierarchy, interaction patterns, SVG integration, and LLM visual context system.

## 🎯 Success Criteria
- Beautiful, professional interface that users love
- Intuitive navigation requiring no documentation
- Complete SVG representation for LLM understanding
- Responsive design across all terminal sizes
- Accessible and keyboard-friendly

## 🎨 Design Philosophy

### Core Principles
1. **Visual Clarity**: Every element has clear purpose and meaning
2. **Intelligent Defaults**: Smart recommendations with easy overrides
3. **Progressive Disclosure**: Show complexity only when needed
4. **Contextual Help**: Assistance based on current UI state
5. **LLM Transparency**: Visual state that LLMs can interpret

### Design System
```python
# Design tokens for consistent styling
DESIGN_TOKENS = {
    "colors": {
        "primary": "#00ff88",      # Bright green for selections
        "secondary": "#6366f1",    # Indigo for secondary actions
        "success": "#22c55e",      # Green for available/working
        "warning": "#f59e0b",      # Amber for attention needed
        "error": "#ef4444",        # Red for errors/unavailable
        "background": "#0d1117",   # Dark background
        "surface": "#161b22",      # Card/panel background
        "text_primary": "#f0f6fc", # Primary text
        "text_secondary": "#8b949e", # Secondary/disabled text
        "border": "#30363d"        # Subtle borders
    },
    "spacing": {
        "xs": 1, "sm": 2, "md": 4, "lg": 8, "xl": 16
    },
    "typography": {
        "heading": {"size": "bold", "color": "text_primary"},
        "body": {"size": "normal", "color": "text_primary"},
        "caption": {"size": "dim", "color": "text_secondary"}
    }
}
```

## 🖼️ Screen Designs

### 1. Startup Detection Screen

#### Visual Layout (SVG)
```xml
<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="800" height="600" fill="#0d1117"/>

  <!-- Header -->
  <text x="400" y="60" text-anchor="middle" fill="#f0f6fc"
        font-size="28" font-weight="bold">
    🤖 DeepResearchAgent Setup
  </text>

  <!-- Detection Progress -->
  <g id="detection-progress">
    <text x="400" y="120" text-anchor="middle" fill="#8b949e" font-size="16">
      🔍 Detecting available backends...
    </text>

    <!-- Progress Bar -->
    <rect x="200" y="140" width="400" height="8" fill="#30363d" rx="4"/>
    <rect x="200" y="140" width="280" height="8" fill="#00ff88" rx="4">
      <animate attributeName="width" values="0;400" dur="3s"/>
    </rect>

    <!-- Progress Text -->
    <text x="400" y="170" text-anchor="middle" fill="#8b949e" font-size="14">
      70% complete...
    </text>
  </g>

  <!-- Detection Results -->
  <g id="detection-results" transform="translate(150, 200)">
    <!-- Claude Code CLI -->
    <g id="claude-detection">
      <circle cx="20" cy="20" r="8" fill="#22c55e"/>
      <text x="40" y="25" fill="#f0f6fc" font-size="14">Claude Code CLI</text>
      <text x="40" y="40" fill="#8b949e" font-size="12">v1.2.3 - Ready</text>
    </g>

    <!-- OpenAI API -->
    <g id="openai-detection" transform="translate(0, 60)">
      <circle cx="20" cy="20" r="8" fill="#22c55e"/>
      <text x="40" y="25" fill="#f0f6fc" font-size="14">OpenAI API</text>
      <text x="40" y="40" fill="#8b949e" font-size="12">API Key configured</text>
    </g>

    <!-- Gemini CLI -->
    <g id="gemini-detection" transform="translate(0, 120)">
      <circle cx="20" cy="20" r="8" fill="none" stroke="#ef4444" stroke-width="2"/>
      <text x="40" y="25" fill="#8b949e" font-size="14">Gemini CLI</text>
      <text x="40" y="40" fill="#ef4444" font-size="12">Not installed</text>
    </g>

    <!-- Local Models -->
    <g id="local-detection" transform="translate(0, 180)">
      <circle cx="20" cy="20" r="8" fill="#f59e0b"/>
      <text x="40" y="25" fill="#f0f6fc" font-size="14">Local Models</text>
      <text x="40" y="40" fill="#8b949e" font-size="12">Available (CPU only)</text>
    </g>
  </g>

  <!-- Action Button -->
  <rect x="325" y="480" width="150" height="40" fill="#00ff88" rx="6"/>
  <text x="400" y="505" text-anchor="middle" fill="#0d1117"
        font-size="14" font-weight="bold">Continue Setup</text>

  <!-- Status Bar -->
  <rect x="0" y="560" width="800" height="40" fill="#161b22"/>
  <text x="20" y="585" fill="#8b949e" font-size="12">
    Press Enter to continue • Q to quit • R to refresh
  </text>
</svg>
```

#### Textual Implementation
```python
class DetectionScreen(Widget):
    """Backend detection screen with real-time updates"""

    def __init__(self):
        super().__init__()
        self.detection_progress = 0
        self.detected_backends = []

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("🤖 DeepResearchAgent Setup", classes="header")
            yield Static("🔍 Detecting available backends...", id="status")
            yield ProgressBar(total=100, show_eta=False, id="progress")
            yield DetectionResults(id="results")
            yield Button("Continue Setup", variant="primary", id="continue")

    def render_to_svg(self) -> str:
        """Generate SVG representation for LLM analysis"""
        return self.svg_renderer.render_detection_screen(
            progress=self.detection_progress,
            backends=self.detected_backends
        )

class DetectionResults(Widget):
    """Display detection results with status indicators"""

    def compose(self) -> ComposeResult:
        with Vertical():
            for backend in self.app.detection_manager.backends:
                yield BackendStatus(backend)

class BackendStatus(Widget):
    """Individual backend status display"""

    def __init__(self, backend: Backend):
        super().__init__()
        self.backend = backend

    def render(self) -> RenderResult:
        status_emoji = "✅" if self.backend.available else "❌"
        status_color = "green" if self.backend.available else "red"

        return Group(
            Text.assemble(
                (status_emoji, status_color),
                f" {self.backend.name}",
                ("white", "bold")
            ),
            Text(self.backend.status_message, style="dim")
        )
```

### 2. Model Selection Screen

#### Visual Layout (SVG)
```xml
<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="800" height="600" fill="#0d1117"/>

  <!-- Header -->
  <text x="400" y="40" text-anchor="middle" fill="#f0f6fc"
        font-size="24" font-weight="bold">Choose Your AI Backend</text>

  <!-- Recommendation Panel -->
  <g id="recommendation-panel">
    <rect x="50" y="70" width="700" height="80" fill="#161b22"
          stroke="#00ff88" rx="8"/>
    <text x="70" y="95" fill="#00ff88" font-size="16" font-weight="bold">
      💡 Recommended Configuration
    </text>
    <text x="70" y="115" fill="#f0f6fc" font-size="14">
      Planning Agent: Claude Code CLI • Browser: OpenAI API
    </text>
    <text x="70" y="135" fill="#8b949e" font-size="12">
      Optimized for code tasks with web research capability
    </text>
  </g>

  <!-- Backend Options -->
  <g id="backend-options" transform="translate(50, 180)">
    <!-- Claude Code CLI - Selected -->
    <g id="claude-option">
      <rect width="320" height="80" fill="#2d5a27" stroke="#00ff88"
            stroke-width="2" rx="8"/>
      <circle cx="30" cy="25" r="8" fill="#00ff88"/>
      <text x="50" y="30" fill="#f0f6fc" font-size="16" font-weight="bold">
        🥇 Claude Code CLI
      </text>
      <text x="50" y="50" fill="#c9d1d9" font-size="14">
        Best for code analysis and file operations
      </text>
      <text x="50" y="65" fill="#8b949e" font-size="12">
        Version 1.2.3 • Local execution
      </text>
      <text x="280" y="30" fill="#00ff88" font-size="14">✓ Selected</text>
    </g>

    <!-- OpenAI API - Available -->
    <g id="openai-option" transform="translate(0, 100)">
      <rect width="320" height="80" fill="#161b22" stroke="#30363d"
            stroke-width="1" rx="8" class="hoverable"/>
      <circle cx="30" cy="25" r="8" fill="none" stroke="#8b949e" stroke-width="2"/>
      <text x="50" y="30" fill="#f0f6fc" font-size="16">
        🥈 OpenAI GPT-4
      </text>
      <text x="50" y="50" fill="#c9d1d9" font-size="14">
        Excellent for reasoning and research
      </text>
      <text x="50" y="65" fill="#8b949e" font-size="12">
        API key configured • ~$0.02/query
      </text>
    </g>

    <!-- Local Models - Available with Warning -->
    <g id="local-option" transform="translate(0, 200)">
      <rect width="320" height="80" fill="#161b22" stroke="#30363d"
            stroke-width="1" rx="8"/>
      <circle cx="30" cy="25" r="8" fill="none" stroke="#f59e0b" stroke-width="2"/>
      <text x="50" y="30" fill="#f0f6fc" font-size="16">
        🥉 Local Transformers
      </text>
      <text x="50" y="50" fill="#c9d1d9" font-size="14">
        Private, offline operation
      </text>
      <text x="50" y="65" fill="#f59e0b" font-size="12">
        ⚠️ Slower performance (CPU only)
      </text>
    </g>

    <!-- Gemini CLI - Unavailable -->
    <g id="gemini-option" transform="translate(380, 0)">
      <rect width="320" height="80" fill="#161b22" stroke="#30363d"
            stroke-width="1" rx="8" opacity="0.5"/>
      <circle cx="30" cy="25" r="8" fill="none" stroke="#ef4444" stroke-width="2"/>
      <text x="50" y="30" fill="#8b949e" font-size="16">
        ❌ Gemini CLI
      </text>
      <text x="50" y="50" fill="#8b949e" font-size="14">
        Not installed
      </text>
      <text x="50" y="65" fill="#ef4444" font-size="12">
        Run: pip install google-generativeai
      </text>
    </g>
  </g>

  <!-- Configuration Preview -->
  <g id="config-preview" transform="translate(400, 180)">
    <rect width="320" height="280" fill="#161b22" stroke="#30363d" rx="8"/>
    <text x="20" y="25" fill="#f0f6fc" font-size="16" font-weight="bold">
      Configuration Preview
    </text>

    <!-- Agent Assignments -->
    <g transform="translate(20, 50)">
      <text y="15" fill="#8b949e" font-size="12">Planning Agent:</text>
      <text y="30" fill="#00ff88" font-size="14">Claude Code CLI</text>

      <text y="55" fill="#8b949e" font-size="12">Deep Analyzer:</text>
      <text y="70" fill="#00ff88" font-size="14">Claude Code CLI</text>

      <text y="95" fill="#8b949e" font-size="12">Browser Agent:</text>
      <text y="110" fill="#6366f1" font-size="14">OpenAI GPT-4</text>

      <text y="135" fill="#8b949e" font-size="12">Researcher:</text>
      <text y="150" fill="#6366f1" font-size="14">OpenAI GPT-4</text>
    </g>

    <!-- Metrics -->
    <g transform="translate(20, 190)">
      <text y="15" fill="#8b949e" font-size="12">Estimated Cost:</text>
      <text y="30" fill="#22c55e" font-size="14">~$0.05/task</text>

      <text y="55" fill="#8b949e" font-size="12">Privacy Level:</text>
      <text y="70" fill="#f59e0b" font-size="14">Mixed (Local + API)</text>
    </g>
  </g>

  <!-- Action Buttons -->
  <g id="actions" transform="translate(50, 520)">
    <rect width="150" height="40" fill="#00ff88" rx="6"/>
    <text x="75" y="25" text-anchor="middle" fill="#0d1117"
          font-size="14" font-weight="bold">Apply Config</text>

    <rect x="170" width="150" height="40" fill="#161b22"
          stroke="#30363d" rx="6"/>
    <text x="245" y="25" text-anchor="middle" fill="#f0f6fc"
          font-size="14">Advanced Setup</text>

    <rect x="340" width="100" height="40" fill="#161b22"
          stroke="#30363d" rx="6"/>
    <text x="390" y="25" text-anchor="middle" fill="#f0f6fc"
          font-size="14">Help</text>
  </g>

  <!-- Status Bar -->
  <rect x="0" y="560" width="800" height="40" fill="#161b22"/>
  <text x="20" y="585" fill="#8b949e" font-size="12">
    ↑↓ Navigate • Enter Select • Space Toggle • Q Quit • H Help
  </text>
</svg>
```

#### Textual Implementation
```python
class ModelSelectionScreen(Widget):
    """Main model selection interface"""

    def __init__(self):
        super().__init__()
        self.selected_backends = {}
        self.recommended_config = None

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("Choose Your AI Backend", classes="header")
            yield RecommendationPanel(id="recommendation")
            with Horizontal():
                yield BackendGrid(id="backends")
                yield ConfigurationPreview(id="preview")
            with Horizontal(classes="actions"):
                yield Button("Apply Config", variant="primary", id="apply")
                yield Button("Advanced Setup", id="advanced")
                yield Button("Help", id="help")

    def render_to_svg(self) -> str:
        """Generate complete SVG for LLM visual understanding"""
        return self.svg_renderer.render_selection_screen(
            backends=self.app.available_backends,
            selected=self.selected_backends,
            recommendation=self.recommended_config,
            preview=self.generate_preview()
        )

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button interactions"""
        if event.button.id == "apply":
            await self.apply_configuration()
        elif event.button.id == "advanced":
            self.app.push_screen(AdvancedConfigScreen())
        elif event.button.id == "help":
            self.app.push_screen(HelpScreen())

class BackendCard(Widget):
    """Individual backend selection card"""

    def __init__(self, backend: Backend):
        super().__init__()
        self.backend = backend
        self.selected = False

    def render(self) -> RenderResult:
        # Dynamic styling based on state
        if not self.backend.available:
            style = "dim"
            emoji = "❌"
        elif self.selected:
            style = "green bold"
            emoji = "✅"
        else:
            style = "white"
            emoji = "⚪"

        return Panel(
            Group(
                Text.assemble((emoji, style), f" {self.backend.name}"),
                Text(self.backend.description),
                Text(self.backend.status, style="dim")
            ),
            title=self.backend.priority_emoji,
            border_style="green" if self.selected else "dim"
        )

    def on_click(self) -> None:
        """Handle selection"""
        if self.backend.available:
            self.selected = not self.selected
            self.refresh()
            self.app.update_configuration()
```

## 🎯 SVG-LLM Integration

### LLM Visual Context System
```python
class LLMVisualContext:
    """Provides visual context to LLMs for intelligent assistance"""

    def __init__(self, app: SVGTUIApp):
        self.app = app
        self.context_history = []

    def get_current_context(self) -> dict:
        """Get comprehensive visual and semantic context"""
        current_svg = self.app.render_full_ui_to_svg()

        return {
            "visual_state": {
                "svg_representation": current_svg,
                "screen_name": self.app.current_screen.__class__.__name__,
                "focused_element": self.get_focused_element_description(),
                "available_actions": self.get_available_actions(),
            },
            "semantic_state": {
                "user_progress": self.app.get_setup_progress(),
                "selected_backends": self.app.get_selected_backends(),
                "recommendations": self.app.get_current_recommendations(),
                "issues": self.app.get_current_issues(),
            },
            "interaction_state": {
                "last_user_action": self.app.last_user_action,
                "navigation_path": self.app.navigation_history,
                "help_requests": self.app.help_history,
            }
        }

    def analyze_user_intent(self, user_input: str) -> dict:
        """Analyze user intent based on visual context"""
        context = self.get_current_context()

        # LLM can see exactly what user is looking at
        analysis = {
            "visible_elements": self.extract_visible_elements(context["visual_state"]["svg_representation"]),
            "possible_actions": self.get_contextual_actions(context),
            "recommended_response": self.generate_contextual_help(user_input, context),
            "ui_modifications": self.suggest_ui_improvements(context)
        }

        return analysis

    def validate_user_expectations(self, user_description: str) -> bool:
        """Verify UI matches user's mental model"""
        current_svg = self.app.render_full_ui_to_svg()

        # LLM compares user expectation with actual visual state
        return self.llm_validator.compare_expectation_with_reality(
            user_expectation=user_description,
            actual_visual_state=current_svg
        )
```

### Contextual Help System
```python
class ContextualHelpSystem:
    """Provides intelligent help based on visual UI state"""

    def get_help_for_current_state(self) -> str:
        """Generate contextual help based on what user sees"""
        svg_state = self.app.render_full_ui_to_svg()

        # LLM analyzes SVG and generates specific help
        help_content = f"""
        Based on what I can see in your current interface:

        Current Screen: {self.identify_screen_from_svg(svg_state)}

        Available Actions:
        {self.extract_available_actions_from_svg(svg_state)}

        Recommendations:
        {self.generate_contextual_recommendations(svg_state)}

        Next Steps:
        {self.suggest_next_steps(svg_state)}
        """

        return help_content

    def explain_visual_elements(self, svg_content: str) -> str:
        """Explain what user sees in plain language"""
        elements = self.parse_svg_elements(svg_content)

        explanations = []
        for element in elements:
            if element.type == "selected_backend":
                explanations.append(f"✅ {element.name} is currently selected (shown in green)")
            elif element.type == "available_backend":
                explanations.append(f"⚪ {element.name} is available for selection")
            elif element.type == "unavailable_backend":
                explanations.append(f"❌ {element.name} is not available ({element.reason})")

        return "\n".join(explanations)
```

## 📱 Responsive Design

### Terminal Size Adaptation
```python
class ResponsiveLayout:
    """Adapts layout based on terminal dimensions"""

    def __init__(self):
        self.breakpoints = {
            "small": 80,   # columns
            "medium": 120,
            "large": 160,
            "xlarge": 200
        }

    def get_layout_for_size(self, width: int, height: int) -> str:
        """Return appropriate layout configuration"""
        if width < self.breakpoints["small"]:
            return "compact"
        elif width < self.breakpoints["medium"]:
            return "standard"
        elif width < self.breakpoints["large"]:
            return "expanded"
        else:
            return "full"

    def adapt_svg_viewport(self, svg_content: str, terminal_size: tuple) -> str:
        """Adapt SVG viewport to terminal size"""
        width, height = terminal_size

        # Calculate optimal aspect ratio
        aspect_ratio = width / height

        # Adjust SVG viewBox
        modified_svg = self.update_svg_viewbox(
            svg_content,
            viewbox_width=800,
            viewbox_height=int(800 / aspect_ratio)
        )

        return modified_svg
```

### Accessibility Features
```python
class AccessibilityFeatures:
    """Ensure TUI is accessible to all users"""

    def __init__(self):
        self.screen_reader_mode = False
        self.high_contrast_mode = False
        self.keyboard_navigation = True

    def generate_screen_reader_description(self, svg_content: str) -> str:
        """Generate text description of visual interface"""
        elements = self.parse_svg_for_accessibility(svg_content)

        description_parts = []
        for element in elements:
            description_parts.append(element.get_accessibility_description())

        return " ".join(description_parts)

    def enable_high_contrast_mode(self):
        """Switch to high contrast color scheme"""
        self.design_tokens["colors"].update({
            "primary": "#ffffff",
            "background": "#000000",
            "text_primary": "#ffffff",
            "text_secondary": "#cccccc"
        })
```

## 🔄 Update Process

### Phase 3 Implementation Timeline

#### Week 5: Foundation
- [ ] Textual TUI framework setup
- [ ] Basic screen structure
- [ ] SVG rendering foundation
- [ ] Design system implementation

#### Week 6: Core Screens
- [ ] Detection screen with animations
- [ ] Model selection interface
- [ ] Configuration preview system
- [ ] Navigation and routing

#### Week 7: SVG Integration
- [ ] Complete SVG generation system
- [ ] LLM visual context integration
- [ ] Contextual help system
- [ ] Export and debugging tools

### Testing Requirements
- [ ] Visual regression testing
- [ ] Accessibility compliance testing
- [ ] Cross-terminal compatibility testing
- [ ] LLM visual understanding validation

## 🎯 Success Validation

### User Experience Metrics
- [ ] New users complete setup in <5 minutes
- [ ] Zero user confusion about current state
- [ ] 100% keyboard navigation capability
- [ ] Clear visual feedback for all actions

### Technical Metrics
- [ ] SVG generation <100ms per screen
- [ ] Responsive design across all terminal sizes
- [ ] LLM visual context accuracy >95%
- [ ] Memory usage <100MB for UI components

This specification provides a comprehensive foundation for implementing a beautiful, intelligent TUI that leverages SVG for enhanced LLM understanding while maintaining excellent user experience and accessibility.