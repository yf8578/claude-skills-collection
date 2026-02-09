---
name: citation-grabber
description: Search for scientific papers and fetch citations in BibTeX or NBIB format from PubMed and CrossRef
version: 1.1.0
usage: citation-grabber <title_or_doi_or_pmid_or_file> [--format bibtex|nbib] [--output <file>] [--quiet]
metadata:
  category: research
  tags: ["citation", "bibtex", "pubmed", "crossref", "academic"]
  author: yf8578
  repository: https://github.com/yf8578/citation-grabber
  # Claude Code specific
  claude:
    priority: high
    auto_install: true
  # OpenClaw/ClawHub specific
  openclaw:
    emoji: "📚"
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["python3"]
      python: ">=3.8"
    install:
      - id: pip-deps
        kind: pip
        packages: ["requests>=2.25.0"]
        label: "Install Python dependencies"
  # Codex specific
  codex:
    enabled: true
    runtime: python
  # Gemini CLI specific
  gemini:
    compatible: true
    runtime: python
---

# Citation Grabber

Instantly fetch scientific paper citations from the command line.

## Features

- 🔍 Search by **title**, **DOI**, or **PubMed ID**
- 📚 Supports **BibTeX** and **NBIB** output formats
- 🔄 Dual source: **PubMed** + **CrossRef**
- 📦 Batch processing from text files
- ✨ Smart fallback between data sources

## Installation

### Via Skills Collection

```bash
# From the skills collection repository
./scripts/install.sh citation-grabber
```

### Standalone

```bash
# Clone the standalone repository
git clone https://github.com/yf8578/citation-grabber.git
cd citation-grabber
pip install -r requirements.txt
```

## Usage

### Single Paper

**By Title:**
```bash
python3 citation.py "Attention Is All You Need"
```

**By DOI:**
```bash
python3 citation.py "10.1038/nature14539"
```

**By PubMed ID:**
```bash
python3 citation.py "12345678"
```

### Output Formats

**BibTeX (Default):**
```bash
python3 citation.py "Deep Learning" --format bibtex
```

**NBIB (PubMed Format for EndNote/Zotero):**
```bash
python3 citation.py "COVID-19 vaccine" --format nbib
```

### Batch Processing

Create a file `papers.txt` with paper titles/DOIs/PMIDs (one per line), then:

```bash
python3 citation.py papers.txt --output references.bib
```

### Quiet Mode

Suppress progress messages:

```bash
python3 citation.py "Paper Title" --quiet
```

## Requirements

- Python 3.8+
- requests library (auto-installed)
- Internet connection

## Links

- **Full Repository**: https://github.com/yf8578/citation-grabber
- **Documentation**: See repository README
- **License**: MIT
