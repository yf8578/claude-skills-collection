#!/bin/bash
# Install skill using symbolic links (recommended - saves space and auto-updates)

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SKILL_NAME=$1
CLAUDE_SKILLS_DIR="${HOME}/.claude/skills"
COLLECTION_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [ -z "$SKILL_NAME" ]; then
    echo -e "${RED}Error: Skill name required${NC}"
    echo "Usage: $0 <skill-name>"
    exit 1
fi

# Check if skill exists
if [ ! -d "$COLLECTION_DIR/$SKILL_NAME" ]; then
    echo -e "${RED}Error: Skill '$SKILL_NAME' not found${NC}"
    exit 1
fi

SKILL_PATH="$COLLECTION_DIR/$SKILL_NAME"

echo -e "${BLUE}🔗 Installing skill with symbolic link: ${YELLOW}$SKILL_NAME${NC}"
echo -e "${BLUE}   Source: $SKILL_PATH${NC}"

# Create Claude skills directory if it doesn't exist
mkdir -p "$CLAUDE_SKILLS_DIR"

# Remove existing installation (link or directory)
if [ -L "$CLAUDE_SKILLS_DIR/$SKILL_NAME" ]; then
    echo -e "${YELLOW}Removing existing link...${NC}"
    rm "$CLAUDE_SKILLS_DIR/$SKILL_NAME"
elif [ -d "$CLAUDE_SKILLS_DIR/$SKILL_NAME" ]; then
    echo -e "${YELLOW}Removing existing directory...${NC}"
    rm -rf "$CLAUDE_SKILLS_DIR/$SKILL_NAME"
fi

# Create symbolic link
ln -s "$SKILL_PATH" "$CLAUDE_SKILLS_DIR/$SKILL_NAME"

# Install dependencies if requirements.txt exists
if [ -f "$SKILL_PATH/requirements.txt" ]; then
    echo -e "${BLUE}📦 Installing dependencies...${NC}"
    pip3 install -q -r "$SKILL_PATH/requirements.txt"
fi

echo -e "${GREEN}✅ Successfully linked '$SKILL_NAME'${NC}"
echo -e "${BLUE}📍 Link: $CLAUDE_SKILLS_DIR/$SKILL_NAME${NC}"
echo -e "${BLUE}   → $SKILL_PATH${NC}"
echo ""
echo -e "${GREEN}💡 Advantages of linking:${NC}"
echo -e "   • No duplicate files (saves disk space)"
echo -e "   • Updates in collection automatically apply"
echo -e "   • Single source of truth"
echo ""
echo -e "${YELLOW}💡 Tip: Restart Claude Code to load the skill${NC}"
