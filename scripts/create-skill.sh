#!/bin/bash
# Create a new skill from template

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SKILL_NAME=$1
CATEGORY=${2:-"productivity"}

if [ -z "$SKILL_NAME" ]; then
    echo -e "${RED}Error: Skill name required${NC}"
    echo "Usage: $0 <skill-name> [category]"
    echo ""
    echo "Available categories:"
    echo "  - research"
    echo "  - development"
    echo "  - productivity (default)"
    echo "  - data"
    echo "  - media"
    exit 1
fi

if [ -d "$SKILL_NAME" ]; then
    echo -e "${RED}Error: Skill '$SKILL_NAME' already exists${NC}"
    exit 1
fi

echo -e "${BLUE}🚀 Creating new skill: ${YELLOW}$SKILL_NAME${NC}"
echo -e "${BLUE}   Category: ${YELLOW}$CATEGORY${NC}"
echo ""

# Create skill directory
mkdir -p "$SKILL_NAME"

# Create SKILL.md
cat > "$SKILL_NAME/SKILL.md" <<EOF
---
name: $SKILL_NAME
description: Brief description of what this skill does
version: 0.1.0
usage: $SKILL_NAME [options]
metadata:
  category: $CATEGORY
  tags: []
  author: yf8578
  claude:
    priority: medium
  openclaw:
    emoji: "🔧"
    os: ["darwin", "linux", "win32"]
    requires:
      bins: ["python3"]
---

# ${SKILL_NAME//-/ }

Description of the skill and what it does.

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

This skill is part of the claude-skills-collection.

\`\`\`bash
./scripts/install.sh $SKILL_NAME
\`\`\`

## Usage

### Basic Usage

\`\`\`bash
python3 $SKILL_NAME/main.py [options]
\`\`\`

### Examples

**Example 1:**
\`\`\`bash
python3 $SKILL_NAME/main.py --help
\`\`\`

## Options

| Option | Description |
|--------|-------------|
| \`--help\` | Show help message |

## Requirements

- Python 3.8+
- See requirements.txt for dependencies

## License

MIT
EOF

# Create basic Python file
cat > "$SKILL_NAME/main.py" <<'EOF'
#!/usr/bin/env python3
"""
Main implementation file.
"""

import sys
import argparse


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Your skill description"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="0.1.0"
    )

    args = parser.parse_args()

    print("Hello from your new skill!")


if __name__ == "__main__":
    main()
EOF

# Create README
cat > "$SKILL_NAME/README.md" <<EOF
# $SKILL_NAME

[Add detailed documentation here]

## Installation

\`\`\`bash
./scripts/install.sh $SKILL_NAME
\`\`\`

## Usage

\`\`\`bash
python3 $SKILL_NAME/main.py
\`\`\`

## License

MIT
EOF

# Create requirements.txt
touch "$SKILL_NAME/requirements.txt"

# Create tests directory
mkdir -p "$SKILL_NAME/tests"
cat > "$SKILL_NAME/tests/__init__.py" <<EOF
"""Tests for $SKILL_NAME"""
EOF

# Make Python file executable
chmod +x "$SKILL_NAME/main.py"

echo -e "${GREEN}✅ Skill created successfully!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo -e "  1. Edit ${YELLOW}$SKILL_NAME/SKILL.md${NC} with your skill details"
echo -e "  2. Implement your skill in ${YELLOW}$SKILL_NAME/main.py${NC}"
echo -e "  3. Add dependencies to ${YELLOW}$SKILL_NAME/requirements.txt${NC}"
echo -e "  4. Register the skill: ${YELLOW}./scripts/register.sh $SKILL_NAME${NC}"
echo -e "  5. Test: ${YELLOW}python3 $SKILL_NAME/main.py${NC}"
