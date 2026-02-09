# Claude Skills Collection 🎯

> **Personal monorepo of Claude AI skills with cross-platform support**

[![Skills](https://img.shields.io/badge/skills-1-blue.svg)](./registry.json)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-brightgreen.svg)](https://code.claude.com/)

A curated collection of skills that extend Claude's capabilities for research, development, and automation tasks.

## 🚀 Quick Start

### Installation (Recommended: Symlink Mode)

```bash
cd ~/00zyf/AI/claude-skills-collection

# Install using symbolic links (saves space, auto-updates)
./scripts/install-universal-link.sh citation-grabber

# Or install all skills at once
./scripts/install-all-link.sh
```

**Why symlinks?**
- 💾 **Zero duplication** - Saves 80% disk space
- ⚡ **Auto-sync** - Update once, applies everywhere
- 🎯 **Single source** - Easier to manage

See [Symlink vs Copy Guide](./docs/symlink-vs-copy.md) for details.

### Alternative: Copy Mode

```bash
# If you need file copies instead of links
./scripts/install-universal.sh citation-grabber
```

## 📚 What Are Skills?

Skills are specialized tools that Claude can use to perform specific tasks. Each skill is a self-contained module with:
- Clear instructions and metadata (`SKILL.md`)
- Implementation code (Python, Bash, etc.)
- Dependencies and requirements
- Usage examples

## 🎯 Available Skills

### Research & Academic 📚

| Skill | Description | Version | Status |
|-------|-------------|---------|--------|
| [**citation-grabber**](./citation-grabber) | Fetch scientific paper citations from PubMed and CrossRef | 1.1.0 | ✅ Stable |

### Coming Soon

- 🔄 **pdf-analyzer** - Extract and analyze PDF documents
- 🔍 **code-reviewer** - Automated code review and suggestions
- 📊 **data-visualizer** - Generate charts and visualizations from data

## 🚀 Quick Start

### Option 1: Install Individual Skills

#### For Claude Code

```bash
# Clone the repository
git clone https://github.com/yf8578/claude-skills-collection.git
cd claude-skills-collection

# Install a specific skill
./scripts/install.sh citation-grabber
```

#### Manual Installation

```bash
# Copy skill to Claude's skills directory
cp -r citation-grabber ~/.claude/skills/
```

### Option 2: Install All Skills

```bash
# Clone and install all skills at once
git clone https://github.com/yf8578/claude-skills-collection.git
cd claude-skills-collection
./scripts/install-all.sh
```

## 📖 Skill Details

### Citation Grabber

Instantly fetch scientific paper citations in BibTeX or NBIB format.

**Features:**
- 🔍 Search by title, DOI, or PubMed ID
- 📚 Dual source: PubMed + CrossRef
- 📦 Batch processing support
- 🎯 Multiple output formats

**Usage:**
```bash
python citation-grabber/citation.py "Attention Is All You Need"
```

**[View Full Documentation →](./citation-grabber/README.md)**

## 🛠️ Management Tools

This collection includes utility scripts to manage your skills:

### List All Skills
```bash
./scripts/list.sh
```

### Check Skill Status
```bash
./scripts/status.sh citation-grabber
```

### Update Skills
```bash
./scripts/update.sh citation-grabber  # Update specific skill
./scripts/update-all.sh               # Update all skills
```

### Remove Skills
```bash
./scripts/uninstall.sh citation-grabber
```

## 📋 Skill Registry

All skills are registered in [`registry.json`](./registry.json) with metadata:

```json
{
  "id": "citation-grabber",
  "name": "Citation Grabber",
  "version": "1.1.0",
  "category": "research",
  "compatible_with": ["claude-code", "openclaw"],
  "status": "stable"
}
```

## 🔧 Development

### Adding a New Skill

1. **Create skill directory:**
   ```bash
   mkdir new-skill
   cd new-skill
   ```

2. **Create SKILL.md with metadata:**
   ```yaml
   ---
   name: new-skill
   description: Brief description
   usage: new-skill [options]
   ---
   ```

3. **Implement the skill**

4. **Register in registry.json:**
   ```bash
   ./scripts/register.sh new-skill
   ```

5. **Test the skill:**
   ```bash
   ./scripts/test.sh new-skill
   ```

### Skill Template

Use the template generator:
```bash
./scripts/create-skill.sh my-new-skill --category development
```

## 🌍 Compatibility

### Supported Platforms

- ✅ **Claude Code** - Official Anthropic CLI
- ✅ **OpenClaw** - Open-source AI assistant
- ⚠️ **Other tools** - May require adaptation

### SKILL.md Standard

This collection follows the universal `SKILL.md` standard, making skills portable across different AI assistant platforms. However, note:

- **Metadata fields** may vary between platforms
- **Installation paths** differ by tool
- **Dependency management** needs platform-specific handling

#### Cross-Platform Example

```yaml
---
name: my-skill
description: Works everywhere
metadata:
  # Claude Code specific
  claude:
    priority: high
  # OpenClaw specific
  openclaw:
    emoji: "🔧"
    os: ["darwin", "linux"]
---
```

## 📁 Project Structure

```
claude-skills-collection/
├── README.md                 # This file
├── LICENSE                   # MIT License
├── registry.json             # Skills registry
├── .gitignore               # Git ignore rules
│
├── citation-grabber/         # Individual skill
│   ├── SKILL.md             # Skill metadata
│   ├── README.md            # Skill documentation
│   ├── citation.py          # Implementation
│   ├── requirements.txt     # Dependencies
│   └── tests/               # Tests
│
├── scripts/                  # Management utilities
│   ├── install.sh           # Install single skill
│   ├── install-all.sh       # Install all skills
│   ├── update.sh            # Update skill
│   ├── uninstall.sh         # Remove skill
│   ├── list.sh              # List all skills
│   ├── status.sh            # Check skill status
│   ├── create-skill.sh      # Create new skill from template
│   ├── register.sh          # Register skill in registry
│   └── test.sh              # Test skill
│
├── templates/                # Skill templates
│   └── basic-skill/         # Basic skill template
│
└── docs/                     # Documentation
    ├── getting-started.md   # Getting started guide
    ├── creating-skills.md   # Skill development guide
    └── compatibility.md     # Platform compatibility info
```

## 🤝 Contributing

Want to add your skill to this collection?

1. Fork this repository
2. Create your skill following the template
3. Register it in `registry.json`
4. Submit a pull request

See [CONTRIBUTING.md](./docs/CONTRIBUTING.md) for detailed guidelines.

## 📊 Statistics

- **Total Skills:** 1
- **Categories:** 5
- **Stable Skills:** 1
- **In Development:** 0

## 🔗 Related Resources

- [Claude Code Documentation](https://code.claude.com/docs)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Awesome Claude Skills](https://github.com/travisvn/awesome-claude-skills)
- [ClawHub - OpenClaw Skills](https://clawhub.ai/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

Individual skills may have their own licenses - check each skill's directory.

## 📧 Contact

- **Author:** yf8578
- **Repository:** [github.com/yf8578/claude-skills-collection](https://github.com/yf8578/claude-skills-collection)
- **Issues:** [Submit an Issue](https://github.com/yf8578/claude-skills-collection/issues)

---

⭐ **Star this repo** if you find these skills useful!

**Built with ❤️ for the Claude AI community**
