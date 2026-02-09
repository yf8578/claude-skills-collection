#!/bin/bash
# Install a specific skill to Claude Code

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SKILL_NAME=$1
CLAUDE_SKILLS_DIR="${HOME}/.claude/skills"

if [ -z "$SKILL_NAME" ]; then
    echo -e "${RED}Error: Skill name required${NC}"
    echo "Usage: $0 <skill-name>"
    echo ""
    echo "Available skills:"
    ls -d */ 2>/dev/null | grep -v "scripts\|templates\|docs" | sed 's#/##'
    exit 1
fi

# Check if skill exists
if [ ! -d "$SKILL_NAME" ]; then
    echo -e "${RED}Error: Skill '$SKILL_NAME' not found${NC}"
    exit 1
fi

# Check if SKILL.md exists
if [ ! -f "$SKILL_NAME/SKILL.md" ]; then
    echo -e "${RED}Error: $SKILL_NAME/SKILL.md not found${NC}"
    exit 1
fi

echo -e "${BLUE}📦 Installing skill: ${YELLOW}$SKILL_NAME${NC}"

# Create Claude skills directory if it doesn't exist
mkdir -p "$CLAUDE_SKILLS_DIR"

# Copy skill to Claude directory
echo -e "${BLUE}📁 Copying files to $CLAUDE_SKILLS_DIR/$SKILL_NAME${NC}"
cp -r "$SKILL_NAME" "$CLAUDE_SKILLS_DIR/"

# Install dependencies if requirements.txt exists
if [ -f "$SKILL_NAME/requirements.txt" ]; then
    echo -e "${BLUE}📦 Installing dependencies...${NC}"
    pip3 install -q -r "$SKILL_NAME/requirements.txt"
fi

# Make scripts executable
if [ -f "$CLAUDE_SKILLS_DIR/$SKILL_NAME"/*.sh ]; then
    chmod +x "$CLAUDE_SKILLS_DIR/$SKILL_NAME"/*.sh
fi

if [ -f "$CLAUDE_SKILLS_DIR/$SKILL_NAME"/*.py ]; then
    chmod +x "$CLAUDE_SKILLS_DIR/$SKILL_NAME"/*.py
fi

echo -e "${GREEN}✅ Successfully installed '$SKILL_NAME'${NC}"
echo -e "${BLUE}📍 Location: $CLAUDE_SKILLS_DIR/$SKILL_NAME${NC}"
echo ""
echo -e "${YELLOW}💡 Tip: Restart Claude Code to load the new skill${NC}"
