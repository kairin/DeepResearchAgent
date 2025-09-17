import argparse
import asyncio
import os
import subprocess
import sys
from pathlib import Path

from mmengine import DictAction
from textual import work
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import (Button, Header, Footer, Log, Input, Select,
                           Label, Static, ListView, ListItem)

root = str(Path(__file__).resolve().parents[0])
sys.path.append(root)

# Apply compatibility fixes early
from src.compat import compatibility_manager
compatibility_manager.apply_compatibility_fixes()

from src.agent import create_agent
from src.config import config
from src.logger import logger
from src.models import model_manager
from src.tui.agent_integration import run_with_tui_progress
from src.project_cli import setup_project_cli


def parse_args():
    parser = argparse.ArgumentParser(
        description='DeepResearchAgent - Multi-Project Research Tool')
    
    # Add global TUI flag
    parser.add_argument(
        "--tui", action="store_true", help="Launch TUI mode")
    
    subparsers = parser.add_subparsers(
        dest='command', help='Available commands')

    # Main research command (default behavior)
    research_parser = subparsers.add_parser(
        'research', help='Run research tasks')
    research_parser.add_argument(
        "--config",
        default=os.path.join(root, "configs", "config_main.py"),
        help="config file path")
    research_parser.add_argument(
        "--task", type=str, help="Research task to execute")
    research_parser.add_argument(
        "--no-progress", action="store_true",
        help="Disable progress display")
    research_parser.add_argument(
        '--cfg-options',
        nargs='+',
        action=DictAction,
        help='override some settings in the used config'
    )

    # Setup project management commands
    setup_project_cli(subparsers)

    args = parser.parse_args()
    return args


class DeepResearchTUI(App):
    """TUI for DeepResearchAgent with menu and description panels."""

    # State for project research mode
    research_mode = False
    selected_project = None
    research_task = ""
    current_selection = 0  # Track which menu item is selected

    # Menu items with descriptions
    MENU_ITEMS = [
        {
            "id": "run_general",
            "name": "Run General Agent",
            "description": "Execute the general research agent.\n\n"
                           "Runs the main pipeline with broad capabilities.",
            "shortcut": "g"
        },
        {
            "id": "run_gaia",
            "name": "Run Gaia Test",
            "description": "Execute GAIA benchmark tests.\n\n"
                           "Evaluates agent performance against benchmarks.",
            "shortcut": "a"
        },
        {
            "id": "run_oai",
            "name": "Run OAI Deep Research",
            "description": "Execute OpenAI's deep research pipeline.\n\n"
                           "Uses advanced OpenAI models for analysis.",
            "shortcut": "o"
        },
        {
            "id": "run_cli",
            "name": "Run CLI Fallback",
            "description": "Execute research with CLI-first config.\n\n"
                           "Optimized for Claude Code and Gemini.",
            "shortcut": "c"
        },
        {
            "id": "project_list",
            "name": "List Projects",
            "description": "Display all registered projects.\n\n"
                           "Shows names, IDs, paths, and status.",
            "shortcut": "p"
        },
        {
            "id": "project_research",
            "name": "Research on Project",
            "description": "Perform research on a specific project.\n\n"
                           "Select projects and define custom tasks.",
            "shortcut": "r"
        },
        {
            "id": "quit",
            "name": "Quit Application",
            "description": "Exit the DeepResearchAgent TUI.\n\n"
                           "All processes will be terminated.",
            "shortcut": "q"
        }
    ]

    CSS = """
    Screen {
        layout: vertical;
    }

    Header {
        height: 3;
    }

    Footer {
        height: 3;
    }

    Horizontal {
        height: 1fr;
    }

    #menu_panel {
        width: 40;
        border: solid $primary;
        padding: 1;
    }

    #description_panel {
        width: 1fr;
        border: solid $secondary;
        padding: 1;
    }

    #log {
        height: 1fr;
        border: solid $primary;
        padding: 1;
    }

    .menu-item {
        padding: 0 1;
        margin: 0 0 1 0;
        background: $surface;
    }

    .menu-item.selected {
        background: $primary;
        color: $primary-background;
    }

    .menu-item:hover {
        background: $accent;
    }

    Label {
        margin-bottom: 1;
    }

    Static {
        color: $text-muted;
    }
    """

    BINDINGS = [
        ("up", "cursor_up", "Move up"),
        ("down", "cursor_down", "Move down"),
        ("enter", "select_item", "Select item"),
        ("q", "quit", "Quit"),
        ("g", "run_general", "Run General Agent"),
        ("a", "run_gaia", "Run Gaia Test"),
        ("o", "run_oai", "Run OAI Deep Research"),
        ("c", "run_cli", "Run CLI Fallback"),
        ("p", "project_list", "List Projects"),
        ("r", "project_research", "Research on Project"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Horizontal():
            # Left panel: Menu
            with Vertical(id="menu_panel"):
                yield Label("🔬 DeepResearchAgent")
                for i, item in enumerate(self.MENU_ITEMS):
                    classes = "menu-item"
                    if i == self.current_selection:
                        classes += " selected"
                    yield Static(
                        f"[{item['shortcut']}] {item['name']}",
                        classes=classes,
                        id=f"menu_item_{i}"
                    )

            # Right panel: Description
            with Vertical(id="description_panel"):
                if self.research_mode:
                    # Project research mode UI
                    yield Label("🔬 Project Research")
                    if not self.selected_project:
                        project_options = self._get_project_options()
                        if project_options:
                            yield Label("Select a project:")
                            yield Select(
                                options=project_options,
                                id="project_select",
                                prompt="Choose a project..."
                            )
                        else:
                            yield Label("❌ No projects found.")
                            yield Button("Back to Main Menu",
                                         id="back_to_main")
                    else:
                        yield Label("Selected: "
                                    f"{self.selected_project['name']}")
                        yield Label("Enter research task:")
                        yield Input(
                            placeholder="What would you like to research?",
                            id="task_input"
                        )
                        yield Button("Start Research", id="start_research")
                        yield Button("Cancel", id="cancel_research")
                else:
                    # Main menu description
                    current_item = self.MENU_ITEMS[self.current_selection]
                    yield Label(f"📋 {current_item['name']}")
                    yield Static(current_item['description'])
                    yield Static(f"\nShortcut: [{current_item['shortcut']}]")

        # Bottom: Log
        yield Log(id="log")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        action_map = {
            "run_general": self.run_general_agent,
            "run_gaia": self.run_gaia_test,
            "run_oai": self.run_oai_deep_research,
            "run_cli": self.run_cli_fallback,
            "project_list": self.project_list,
            "project_research": self.start_project_research,
            "back_to_main": self.back_to_main,
            "start_research": self.start_research,
            "cancel_research": self.cancel_research,
            "quit": self.action_quit,
        }
        if event.button.id in action_map:
            action_map[event.button.id]()

    async def action_quit(self) -> None:
        self.exit()

    def action_run_general(self) -> None:
        self.run_general_agent()

    def action_run_gaia(self) -> None:
        self.run_gaia_test()

    def action_run_oai(self) -> None:
        self.run_oai_deep_research()

    def action_run_cli(self) -> None:
        self.run_cli_fallback()

    def action_cursor_up(self) -> None:
        """Move cursor up in menu."""
        if not self.research_mode:
            self.current_selection = max(0, self.current_selection - 1)
            self.refresh()

    def action_cursor_down(self) -> None:
        """Move cursor down in menu."""
        if not self.research_mode:
            self.current_selection = min(
                len(self.MENU_ITEMS) - 1,
                self.current_selection + 1
            )
            self.refresh()

    def action_select_item(self) -> None:
        """Select the currently highlighted menu item."""
        if not self.research_mode:
            current_item = self.MENU_ITEMS[self.current_selection]
            action_map = {
                "run_general": self.run_general_agent,
                "run_gaia": self.run_gaia_test,
                "run_oai": self.run_oai_deep_research,
                "run_cli": self.run_cli_fallback,
                "project_list": self.project_list,
                "project_research": self.start_project_research,
                "quit": self.action_quit,
            }
            if current_item["id"] in action_map:
                action_map[current_item["id"]]()

    @work(exclusive=True, thread=True)
    def run_general_agent(self) -> None:
        self._run_agent("examples/run_general.py", "General Agent")

    @work(exclusive=True, thread=True)
    def run_gaia_test(self) -> None:
        self._run_agent("examples/run_gaia.py", "Gaia Test")

    @work(exclusive=True, thread=True)
    def run_oai_deep_research(self) -> None:
        self._run_agent(
            "examples/run_oai_deep_research.py",
            "OAI Deep Research"
        )

    @work(exclusive=True, thread=True)
    def run_cli_fallback(self) -> None:
        self._run_agent(
            "main.py",
            "CLI Fallback",
            ["--config", "configs/config_cli_fallback.py"]
        )

    @work(exclusive=True, thread=True)
    def project_list(self) -> None:
        """List all projects in the registry."""
        log = self.query_one("#log", Log)
        log.write("📋 Listing projects...")

        try:
            from src.project_cli import list_projects_command

            # Create a mock args object
            class MockArgs:
                pass
            mock_args = MockArgs()
            list_projects_command(mock_args)
            log.write("✅ Project list displayed above")
        except Exception as e:
            log.write(f"❌ Error listing projects: {e}")

    @work(exclusive=True, thread=True)
    def project_research(self) -> None:
        """Research on a specific project."""
        log = self.query_one("#log", Log)
        log.write("🔬 Project research feature coming soon...")
        log.write("   Use CLI commands for now:")
        log.write("   uv run python main.py project-list")
        log.write("   uv run python main.py project-research <id> <task>")

    def _get_project_options(self):
        """Get project options for the select widget."""
        try:
            from src.project_registry import project_registry
            projects = project_registry.list_projects()
            if not projects:
                return []
            return [(project.name, project.id) for project in projects]
        except Exception:
            return []

    def start_project_research(self):
        """Start the project research mode."""
        self.research_mode = True
        self.selected_project = None
        self.research_task = ""
        self.refresh()

    def back_to_main(self):
        """Return to main menu."""
        self.research_mode = False
        self.selected_project = None
        self.research_task = ""
        self.refresh()

    def cancel_research(self):
        """Cancel research and return to project selection."""
        self.selected_project = None
        self.research_task = ""
        self.refresh()

    @work(exclusive=True, thread=True)
    def start_research(self) -> None:
        """Start the actual research on the selected project."""
        if not self.selected_project or not self.research_task:
            return

        log = self.query_one("#log", Log)
        log.write("🔬 Starting research on project: "
                  f"{self.selected_project['name']}")
        log.write(f"   Task: {self.research_task}")

        try:
            # Import required modules
            from src.project_cli import research_command

            # Create args object for research command
            class MockArgs:
                def __init__(self, project_id: str, task: str):
                    self.project_id = project_id
                    self.task = task

            mock_args = MockArgs(
                self.selected_project['id'],
                self.research_task
            )

            # Run the research
            research_command(mock_args)

            log.write("✅ Research completed!")
            self.back_to_main()

        except Exception as e:
            log.write(f"❌ Research failed: {e}")
            self.back_to_main()

    def on_select_changed(self, event: Select.Changed) -> None:
        """Handle project selection."""
        if event.select.id == "project_select" and event.value:
            try:
                from src.project_registry import project_registry
                project_id = str(event.value)
                project = project_registry.get_project(project_id)
                if project:
                    self.selected_project = {
                        'id': project.id,
                        'name': project.name,
                        'path': project.path
                    }
                    self.refresh()
            except Exception as e:
                log = self.query_one("#log", Log)
                log.write(f"❌ Error selecting project: {e}")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle task input submission."""
        if event.input.id == "task_input":
            self.research_task = event.value
            # Auto-start research when task is entered
            if self.selected_project and self.research_task:
                self.start_research()

    def _run_agent(
        self, script: str, name: str, args: list[str] | None = None
    ) -> None:
        """Run an agent script in a worker thread to avoid blocking the UI."""
        log = self.query_one("#log", Log)
        log.write(f"Starting {name}...")
        cmd = ["uv", "run", "python", script]
        if args:
            cmd.extend(args)
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent,
                timeout=300  # 5-minute timeout
            )
            if result.returncode == 0:
                log.write(f"✓ {name} completed successfully.")
                if result.stdout.strip():
                    log.write(f"Output: {result.stdout.strip()}")
            else:
                log.write(
                    f"✗ {name} failed with exit code {result.returncode}."
                )
                if result.stderr.strip():
                    log.write(f"Error: {result.stderr.strip()}")
        except subprocess.TimeoutExpired:
            log.write(f"✗ {name} timed out after 5 minutes.")
        except Exception as e:
            log.write(f"✗ {name} encountered an error: {e}")


async def main(args, task: str | None = None):
    try:
        # Initialize the configuration
        config.init_config(args.config, args)

        # Initialize the logger
        logger.init_logger(log_path=config.log_path)
        logger.info(f"| Logger initialized at: {config.log_path}")
        logger.info(f"| Config:\n{config.pretty_text}")

        # Initialize models with validation
        logger.info("| Initializing models...")
        model_manager.init_models(use_local_proxy=True)

        # Display model validation for user
        from src.models.model_validator import validate_and_display_models
        validation_results = validate_and_display_models()

        logger.info(
            "| Model validation complete: %d models available",
            validation_results['summary']['total_models']
        )

    except RuntimeError as e:
        logger.error(f"| Startup failed: {e}")
        logger.error("| Please check your configuration and try again")
        sys.exit(1)
    except Exception as e:
        logger.error(f"| Unexpected error during startup: {e}")
        logger.error("| See logs above for details")
        sys.exit(1)

    # Create agent
    agent = await create_agent(config)
    logger.visualize_agent_tree(agent)

    # Use provided task or command line task or fallback to default
    if task is None:
        task = getattr(args, 'task', None)

    if task is None:
        # Default demo task as fallback
        task = (
            "Use deep_researcher_agent to search the latest papers on the "
            "topic of 'AI Agent' and then summarize it."
        )
        logger.info("| Using default demo task (no custom task provided)")
    else:
        logger.info(f"| Executing custom task: {task[:100]}...")

    # Determine if we should show progress display
    show_progress = not getattr(args, 'no_progress', False)

    if show_progress:
        # Run with TUI progress display
        logger.info("| Starting task execution with progress display...")
        res = await run_with_tui_progress(
            agent,
            task,
            is_hierarchical=True,
            show_progress=True
        )
    else:
        # Run without progress display (traditional logging)
        logger.info("| Starting task execution (logs only)...")
        res = await agent.run(task)

    logger.info(f"| Result: {res}")

if __name__ == '__main__':
    args = parse_args()

    # Handle project management commands
    if hasattr(args, 'func') and args.func:
        # This is a project management command
        args.func(args)
        sys.exit(0)

    # Handle TUI mode - either explicitly requested or default when no command
    if getattr(args, 'tui', False) or args.command is None:
        app = DeepResearchTUI()
        asyncio.run(app.run_async())
    else:
        asyncio.run(main(args))
# TUI scrolling and click fixes applied
