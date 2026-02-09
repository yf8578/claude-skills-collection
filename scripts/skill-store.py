#!/usr/bin/env python3
"""
Skills Store - Interactive Browser for Skills
Browse, search, and install skills from ClawHub, GitHub, and more
"""

import os
import sys
import json
import subprocess
import asyncio
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass

try:
    from textual.app import App, ComposeResult
    from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
    from textual.widgets import (
        Header, Footer, Button, Static, Input, DataTable,
        Label, LoadingIndicator, Markdown, TabbedContent, TabPane,
        Tree, ProgressBar, Log
    )
    from textual.binding import Binding
    from textual.screen import ModalScreen
    from textual import work
    import requests
    from rich.console import Console
    from rich.table import Table as RichTable
except ImportError:
    print("❌ Missing dependencies!")
    print("\n📦 Install with:")
    print("   pip install textual requests rich")
    sys.exit(1)


COLLECTION_DIR = Path.home() / "00zyf" / "AI" / "claude-skills-collection"
REGISTRY_FILE = COLLECTION_DIR / "registry.json"

# ClawHub API (example - adjust if real API exists)
CLAWHUB_API = "https://api.clawhub.ai/v1/skills"  # Hypothetical
CLAWHUB_SEARCH = "https://clawhub.ai/search"


@dataclass
class Skill:
    """Skill data structure"""
    id: str
    name: str
    version: str
    description: str
    category: str
    tags: List[str]
    author: str
    repository: str
    source: str
    status: str
    installed: bool = False


class InstallProgressScreen(ModalScreen):
    """Modal screen showing installation progress"""

    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
    ]

    def __init__(self, skill_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skill_name = skill_name

    def compose(self) -> ComposeResult:
        yield Container(
            Static(f"Installing {self.skill_name}...", id="install-title"),
            Log(id="install-log", auto_scroll=True),
            Button("Close", id="close-btn", variant="primary"),
            id="install-dialog"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close-btn":
            self.dismiss()


class SkillDetailScreen(ModalScreen):
    """Modal screen showing skill details with install option"""

    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
        Binding("i", "install", "Install"),
    ]

    CSS = """
    #detail-dialog {
        width: 80%;
        height: 85%;
        background: $surface;
        border: thick $primary;
        padding: 1 2;
    }

    #detail-content {
        height: 1fr;
        overflow-y: auto;
    }

    #detail-actions {
        dock: bottom;
        height: 3;
        layout: horizontal;
        align: center middle;
    }

    .action-button {
        margin: 0 1;
    }
    """

    def __init__(self, skill: Skill, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skill = skill

    def compose(self) -> ComposeResult:
        installed_badge = "✅ INSTALLED" if self.skill.installed else "📦 NOT INSTALLED"

        markdown_content = f"""
# {self.skill.name} {installed_badge}

**Version:** {self.skill.version}
**Category:** {self.skill.category}
**Author:** {self.skill.author}
**Status:** {self.skill.status}
**Source:** {self.skill.source}

## Description
{self.skill.description}

## Tags
{', '.join(self.skill.tags) if self.skill.tags else 'None'}

## Repository
{self.skill.repository}

## Installation
This skill will be installed to:
- Claude Code: `~/.claude/skills/`
- Codex: `~/.codex/skills/`
- Gemini CLI: `~/.gemini/tools/`
- Antigravity: `~/.antigravity/extensions/`

---
"""
        with Container(id="detail-dialog"):
            with ScrollableContainer(id="detail-content"):
                yield Markdown(markdown_content)
            with Horizontal(id="detail-actions"):
                if not self.skill.installed:
                    yield Button("📥 Install", id="install-btn", variant="success", classes="action-button")
                else:
                    yield Button("🔄 Reinstall", id="reinstall-btn", variant="primary", classes="action-button")
                yield Button("❌ Close", id="close-btn", variant="default", classes="action-button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id in ("install-btn", "reinstall-btn"):
            self.dismiss(result="install")
        elif event.button.id == "close-btn":
            self.dismiss()

    def action_install(self) -> None:
        """Install the skill"""
        self.dismiss(result="install")


class SearchScreen(ModalScreen):
    """Modal screen for advanced search"""

    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
    ]

    CSS = """
    #search-dialog {
        width: 60%;
        height: 70%;
        background: $surface;
        border: thick $primary;
        padding: 1 2;
    }
    """

    def compose(self) -> ComposeResult:
        with Container(id="search-dialog"):
            yield Static("🔍 Advanced Search", id="search-title")
            yield Input(placeholder="Search by name, description, tags...", id="search-input")
            yield Static("\nCategories:", classes="search-section")
            yield Button("📚 Research", id="cat-research", variant="default")
            yield Button("💻 Development", id="cat-development", variant="default")
            yield Button("⚡ Productivity", id="cat-productivity", variant="default")
            yield Button("📊 Data", id="cat-data", variant="default")
            yield Button("🎨 Media", id="cat-media", variant="default")
            yield Static("\n")
            yield Button("Search", id="search-btn", variant="primary")


class SkillsStore(App):
    """Skills Store - Interactive TUI for browsing and installing skills"""

    CSS = """
    Screen {
        background: $surface;
    }

    #main-container {
        height: 100%;
    }

    .skill-table {
        height: 100%;
    }

    .search-box {
        dock: top;
        height: 3;
        padding: 0 1;
        margin: 1 0;
    }

    .stats-bar {
        dock: top;
        height: 3;
        background: $boost;
        padding: 1;
        margin: 0 0 1 0;
    }

    .status-bar {
        dock: bottom;
        height: 1;
        background: $accent;
        color: $text;
        padding: 0 1;
    }

    #install-dialog {
        width: 70%;
        height: 70%;
        background: $surface;
        border: thick $primary;
        padding: 1 2;
    }

    #install-title {
        text-align: center;
        text-style: bold;
        padding: 1;
    }

    #install-log {
        height: 1fr;
        border: solid $primary;
        margin: 1 0;
    }

    #close-btn {
        dock: bottom;
        width: 100%;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("i", "install_selected", "Install"),
        Binding("d", "show_detail", "Detail"),
        Binding("/", "focus_search", "Search"),
        Binding("?", "show_help", "Help"),
    ]

    TITLE = "Skills Store - Browse & Install Skills"

    def __init__(self):
        super().__init__()
        self.installed_skills: List[Skill] = []
        self.available_skills: List[Skill] = []
        self.filtered_skills: List[Skill] = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Container(id="main-container"):
            yield Static(
                "📦 Total: 0 | ✅ Installed: 0 | 🌐 Available: 0",
                id="stats",
                classes="stats-bar"
            )

            with TabbedContent(initial="tab-installed"):
                with TabPane("Installed (0)", id="tab-installed"):
                    yield Input(
                        placeholder="Search installed skills (name, category, tags)...",
                        id="search-installed",
                        classes="search-box"
                    )
                    yield DataTable(
                        id="table-installed",
                        classes="skill-table",
                        cursor_type="row",
                        zebra_stripes=True
                    )

                with TabPane("Discover", id="tab-discover"):
                    yield Markdown("""
# 🌟 Discover Skills

## Available Sources

### 🔹 ClawHub (5,700+ skills)
The largest repository of AI skills. Use the command:
```bash
clawhub search <keyword>
```

Then add to your collection:
```bash
./scripts/add-skill.sh clawhub:skill-name
```

### 🔹 GitHub
Thousands of open-source skills. Add directly:
```bash
./scripts/add-skill.sh github:username/repo
```

### 🔹 Anthropic Official (6 skills)
Already included in this collection:
- pdf, docx, pptx, xlsx
- mcp-builder, skill-creator

### 🔹 Create Your Own
```bash
./scripts/create-skill.sh my-skill
```

---

**Coming Soon:** Direct integration with ClawHub API for browsing within this UI!
                    """, id="discover-content")

                with TabPane("Help", id="tab-help"):
                    yield Markdown("""
# 📖 Skills Store Help

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `↑/↓` | Navigate skills |
| `Enter` or `d` | View details |
| `i` | Install selected skill |
| `/` | Focus search |
| `r` | Refresh list |
| `Tab` | Switch tabs |
| `?` | Show this help |
| `q` | Quit |

## How to Use

### 1. Browse Installed Skills
- Switch to "Installed" tab
- Use search to filter skills
- Press `Enter` to view details

### 2. Install New Skills

**From ClawHub:**
```bash
# Outside this app:
clawhub search pdf

# Then add:
cd ~/00zyf/AI/claude-skills-collection
./scripts/add-skill.sh clawhub:pdf-analyzer
```

**From GitHub:**
```bash
./scripts/add-skill.sh github:username/skill-name
```

**From Local:**
```bash
./scripts/add-skill.sh /path/to/skill
```

### 3. Manage Skills
```bash
# List all
./scripts/list.sh

# Check status
./scripts/status.sh skill-name

# Uninstall
./scripts/uninstall.sh skill-name
```

## Tips

- Skills are installed to all platforms (Claude Code, Codex, Gemini CLI, Antigravity)
- Symlinks save 60-80% disk space
- All changes are Git-tracked
- See `USAGE_GUIDE.md` for complete documentation

---

**Project:** claude-skills-collection
**Location:** ~/00zyf/AI/claude-skills-collection
                    """, id="help-content")

        yield Static("Ready - Press ? for help", id="status-bar", classes="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        """Load skills when app starts"""
        self.load_installed_skills()
        self.update_stats()

    def load_installed_skills(self) -> None:
        """Load skills from registry.json"""
        try:
            if REGISTRY_FILE.exists():
                with open(REGISTRY_FILE) as f:
                    data = json.load(f)
                    raw_skills = data.get("skills", [])

                    self.installed_skills = [
                        Skill(
                            id=s.get('id', ''),
                            name=s.get('name', 'Unknown'),
                            version=s.get('version', 'N/A'),
                            description=s.get('description', ''),
                            category=s.get('category', 'N/A'),
                            tags=s.get('tags', []),
                            author=s.get('author', 'Unknown'),
                            repository=s.get('repository', ''),
                            source=s.get('source', 'unknown'),
                            status=s.get('status', 'unknown'),
                            installed=True
                        )
                        for s in raw_skills
                    ]
                    self.filtered_skills = self.installed_skills.copy()
            else:
                self.installed_skills = []
                self.filtered_skills = []

            self.update_table()
            self.update_tab_title("tab-installed", f"Installed ({len(self.installed_skills)})")
            self.update_status(f"Loaded {len(self.installed_skills)} installed skills")
        except Exception as e:
            self.update_status(f"Error loading skills: {e}", error=True)

    def update_table(self) -> None:
        """Update the DataTable with filtered skills"""
        table = self.query_one("#table-installed", DataTable)
        table.clear(columns=True)

        # Add columns
        table.add_column("Name", width=25)
        table.add_column("Version", width=10)
        table.add_column("Category", width=15)
        table.add_column("Description", width=50)
        table.add_column("Source", width=12)

        # Add rows
        for skill in self.filtered_skills:
            desc = skill.description
            if len(desc) > 47:
                desc = desc[:47] + "..."

            table.add_row(
                skill.name,
                skill.version,
                skill.category,
                desc,
                skill.source
            )

    def update_stats(self) -> None:
        """Update statistics bar"""
        total = len(self.installed_skills)
        installed = len(self.installed_skills)
        available = len(self.available_skills)

        stats = self.query_one("#stats", Static)
        stats.update(f"📦 Total: {total} | ✅ Installed: {installed} | 🌐 Available: {available}")

    def update_tab_title(self, tab_id: str, new_title: str) -> None:
        """Update tab title"""
        try:
            # This is a workaround - textual doesn't have direct tab title update
            pass
        except:
            pass

    def update_status(self, message: str, error: bool = False) -> None:
        """Update status bar"""
        status = self.query_one("#status-bar", Static)
        prefix = "❌" if error else "✓"
        status.update(f"{prefix} {message}")

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle search input"""
        if event.input.id == "search-installed":
            query = event.value.lower()
            if query:
                self.filtered_skills = [
                    skill for skill in self.installed_skills
                    if query in skill.name.lower() or
                       query in skill.description.lower() or
                       query in skill.category.lower() or
                       query in ' '.join(skill.tags).lower()
                ]
            else:
                self.filtered_skills = self.installed_skills.copy()

            self.update_table()
            self.update_status(f"Found {len(self.filtered_skills)} skills")

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection - show detail"""
        self.action_show_detail()

    def action_refresh(self) -> None:
        """Refresh skills list"""
        self.update_status("Refreshing...")
        self.load_installed_skills()
        self.update_stats()

    def action_show_detail(self) -> None:
        """Show skill details"""
        table = self.query_one("#table-installed", DataTable)
        if table.cursor_row is not None and table.cursor_row < len(self.filtered_skills):
            skill = self.filtered_skills[table.cursor_row]

            async def show_detail():
                result = await self.push_screen_wait(SkillDetailScreen(skill))
                if result == "install":
                    await self.install_skill(skill)

            self.call_later(show_detail)

    def action_install_selected(self) -> None:
        """Install selected skill"""
        table = self.query_one("#table-installed", DataTable)
        if table.cursor_row is not None and table.cursor_row < len(self.filtered_skills):
            skill = self.filtered_skills[table.cursor_row]

            async def do_install():
                await self.install_skill(skill)

            self.call_later(do_install)

    async def install_skill(self, skill: Skill) -> None:
        """Install a skill using add-skill.sh"""
        # Determine source argument
        if skill.installed:
            source_arg = f"local:{COLLECTION_DIR}/{skill.id}"
        elif skill.source == 'anthropic':
            self.update_status(f"Skill {skill.id} is from Anthropic and should already be installed")
            return
        else:
            repo = skill.repository
            if 'github.com' in repo:
                parts = repo.rstrip('/').split('github.com/')[-1].split('/')
                if len(parts) >= 2:
                    source_arg = f"github:{parts[0]}/{parts[1]}"
                else:
                    self.update_status(f"Cannot determine source for {skill.id}", error=True)
                    return
            else:
                self.update_status(f"Unknown source for {skill.id}", error=True)
                return

        # Show progress screen
        progress_screen = InstallProgressScreen(skill.name)
        self.push_screen(progress_screen)

        log_widget = progress_screen.query_one("#install-log", Log)
        log_widget.write_line(f"Installing {skill.name}...")
        log_widget.write_line(f"Source: {source_arg}")
        log_widget.write_line("")

        # Run installation
        script_path = COLLECTION_DIR / "scripts" / "add-skill.sh"
        try:
            process = await asyncio.create_subprocess_exec(
                str(script_path),
                source_arg,
                cwd=str(COLLECTION_DIR),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT
            )

            # Stream output
            while True:
                line = await process.stdout.readline()
                if not line:
                    break
                log_widget.write_line(line.decode().rstrip())

            await process.wait()

            if process.returncode == 0:
                log_widget.write_line("")
                log_widget.write_line("✅ Installation successful!")
                self.update_status(f"Successfully installed {skill.id}")
                self.load_installed_skills()
                self.update_stats()
            else:
                log_widget.write_line("")
                log_widget.write_line(f"❌ Installation failed (exit code: {process.returncode})")
                self.update_status(f"Failed to install {skill.id}", error=True)

        except Exception as e:
            log_widget.write_line(f"❌ Error: {e}")
            self.update_status(f"Error installing {skill.id}: {e}", error=True)

    def action_focus_search(self) -> None:
        """Focus on search input"""
        try:
            search = self.query_one("#search-installed", Input)
            search.focus()
        except:
            pass

    def action_show_help(self) -> None:
        """Switch to help tab"""
        tabs = self.query_one(TabbedContent)
        tabs.active = "tab-help"


def main():
    """Run the Skills Store"""
    app = SkillsStore()
    app.run()


if __name__ == "__main__":
    main()
