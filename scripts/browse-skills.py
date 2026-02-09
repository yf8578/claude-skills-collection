#!/usr/bin/env python3
"""
Interactive Skills Browser
Browse, search, and install skills from multiple sources with a beautiful TUI
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Optional

try:
    from textual.app import App, ComposeResult
    from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
    from textual.widgets import (
        Header, Footer, Button, Static, Input, DataTable,
        Label, LoadingIndicator, Markdown, TabbedContent, TabPane
    )
    from textual.binding import Binding
    from textual.screen import ModalScreen
except ImportError:
    print("❌ Error: textual library not found")
    print("\n📦 Install it with:")
    print("   pip install textual")
    print("\nOr install all dependencies:")
    print("   pip install -r requirements-dev.txt")
    sys.exit(1)


COLLECTION_DIR = Path.home() / "00zyf" / "AI" / "claude-skills-collection"
REGISTRY_FILE = COLLECTION_DIR / "registry.json"


class SkillDetailScreen(ModalScreen):
    """Modal screen showing skill details"""

    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
        Binding("i", "install", "Install"),
    ]

    def __init__(self, skill: Dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skill = skill

    def compose(self) -> ComposeResult:
        markdown_content = f"""
# {self.skill.get('name', 'Unknown')}

**Version:** {self.skill.get('version', 'N/A')}
**Category:** {self.skill.get('category', 'N/A')}
**Status:** {self.skill.get('status', 'N/A')}
**Source:** {self.skill.get('source', 'N/A')}

## Description
{self.skill.get('description', 'No description available')}

## Tags
{', '.join(self.skill.get('tags', []))}

## Repository
{self.skill.get('repository', 'N/A')}

## Requirements
{', '.join(self.skill.get('requirements', ['None']))}

## Compatible With
{', '.join(self.skill.get('compatible_with', []))}

---

Press **i** to install | **Esc** to close
"""
        yield Container(
            Markdown(markdown_content),
            id="detail-dialog"
        )

    def action_install(self):
        """Install the skill"""
        self.dismiss(result="install")


class SkillsBrowser(App):
    """Interactive Skills Browser TUI"""

    CSS = """
    #detail-dialog {
        width: 80%;
        height: 80%;
        background: $surface;
        border: thick $primary;
        padding: 1 2;
    }

    .skill-table {
        height: 100%;
    }

    .search-box {
        dock: top;
        height: 3;
        padding: 1;
    }

    .action-bar {
        dock: bottom;
        height: 3;
        background: $surface;
    }

    .status-bar {
        dock: bottom;
        height: 1;
        background: $accent;
        color: $text;
        padding: 0 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("i", "install", "Install"),
        Binding("d", "detail", "Detail"),
        Binding("/", "focus_search", "Search"),
    ]

    def __init__(self):
        super().__init__()
        self.skills_data: List[Dict] = []
        self.filtered_skills: List[Dict] = []
        self.selected_skill: Optional[Dict] = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with TabbedContent(initial="installed"):
            with TabPane("Installed Skills", id="installed"):
                yield Input(
                    placeholder="Search installed skills...",
                    id="search-installed",
                    classes="search-box"
                )
                yield DataTable(id="table-installed", classes="skill-table")

            with TabPane("ClawHub (5,700+)", id="clawhub"):
                yield Static("ClawHub integration coming soon...\n\nFor now, use: clawhub search <keyword>", id="clawhub-content")

            with TabPane("GitHub", id="github"):
                yield Static("GitHub search coming soon...\n\nFor now, use: ./scripts/add-skill.sh github:user/repo", id="github-content")

        yield Static("Ready", id="status-bar", classes="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        """Load skills when app starts"""
        self.load_installed_skills()

    def load_installed_skills(self) -> None:
        """Load skills from registry.json"""
        try:
            if REGISTRY_FILE.exists():
                with open(REGISTRY_FILE) as f:
                    data = json.load(f)
                    self.skills_data = data.get("skills", [])
                    self.filtered_skills = self.skills_data.copy()
            else:
                self.skills_data = []
                self.filtered_skills = []

            self.update_table()
            self.update_status(f"Loaded {len(self.skills_data)} skills")
        except Exception as e:
            self.update_status(f"Error loading skills: {e}", error=True)

    def update_table(self) -> None:
        """Update the DataTable with filtered skills"""
        table = self.query_one("#table-installed", DataTable)
        table.clear(columns=True)

        # Add columns
        table.add_column("Name", width=20)
        table.add_column("Version", width=10)
        table.add_column("Category", width=15)
        table.add_column("Description", width=50)
        table.add_column("Status", width=10)

        # Add rows
        for skill in self.filtered_skills:
            table.add_row(
                skill.get('name', 'Unknown'),
                skill.get('version', 'N/A'),
                skill.get('category', 'N/A'),
                skill.get('description', '')[:47] + "..." if len(skill.get('description', '')) > 50 else skill.get('description', ''),
                skill.get('status', 'N/A')
            )

    def update_status(self, message: str, error: bool = False) -> None:
        """Update status bar"""
        status = self.query_one("#status-bar", Static)
        if error:
            status.update(f"❌ {message}")
        else:
            status.update(f"✓ {message}")

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle search input"""
        if event.input.id == "search-installed":
            query = event.value.lower()
            if query:
                self.filtered_skills = [
                    skill for skill in self.skills_data
                    if query in skill.get('name', '').lower() or
                       query in skill.get('description', '').lower() or
                       query in skill.get('category', '').lower() or
                       query in ' '.join(skill.get('tags', [])).lower()
                ]
            else:
                self.filtered_skills = self.skills_data.copy()

            self.update_table()
            self.update_status(f"Found {len(self.filtered_skills)} skills")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection"""
        if event.row_key.value is not None:
            row_index = event.row_key.value
            if 0 <= row_index < len(self.filtered_skills):
                self.selected_skill = self.filtered_skills[row_index]

    def action_refresh(self) -> None:
        """Refresh skills list"""
        self.update_status("Refreshing...")
        self.load_installed_skills()

    def action_detail(self) -> None:
        """Show skill details"""
        table = self.query_one("#table-installed", DataTable)
        if table.cursor_row is not None and table.cursor_row < len(self.filtered_skills):
            skill = self.filtered_skills[table.cursor_row]

            async def show_detail():
                result = await self.push_screen_wait(SkillDetailScreen(skill))
                if result == "install":
                    self.install_skill(skill)

            self.call_later(show_detail)

    def action_install(self) -> None:
        """Install selected skill"""
        table = self.query_one("#table-installed", DataTable)
        if table.cursor_row is not None and table.cursor_row < len(self.filtered_skills):
            skill = self.filtered_skills[table.cursor_row]
            self.install_skill(skill)

    def install_skill(self, skill: Dict) -> None:
        """Install a skill using add-skill.sh"""
        skill_id = skill.get('id', '')
        source = skill.get('source', '')

        # Determine source type
        if source == 'anthropic':
            source_arg = f"github:anthropics/skills/{skill_id}"
        elif source == 'custom':
            self.update_status(f"Skill {skill_id} is already installed", error=False)
            return
        else:
            repo = skill.get('repository', '')
            if 'github.com' in repo:
                # Extract user/repo from URL
                parts = repo.split('github.com/')[-1].split('/')
                if len(parts) >= 2:
                    source_arg = f"github:{parts[0]}/{parts[1]}"
                else:
                    self.update_status(f"Cannot determine source for {skill_id}", error=True)
                    return
            else:
                self.update_status(f"Unknown source for {skill_id}", error=True)
                return

        self.update_status(f"Installing {skill_id}...")

        # Run add-skill.sh
        script_path = COLLECTION_DIR / "scripts" / "add-skill.sh"
        try:
            result = subprocess.run(
                [str(script_path), source_arg],
                cwd=str(COLLECTION_DIR),
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                self.update_status(f"Successfully installed {skill_id}")
                self.load_installed_skills()
            else:
                self.update_status(f"Failed to install {skill_id}: {result.stderr}", error=True)
        except Exception as e:
            self.update_status(f"Error installing {skill_id}: {e}", error=True)

    def action_focus_search(self) -> None:
        """Focus on search input"""
        search = self.query_one("#search-installed", Input)
        search.focus()


def main():
    """Run the Skills Browser"""
    app = SkillsBrowser()
    app.run()


if __name__ == "__main__":
    main()
