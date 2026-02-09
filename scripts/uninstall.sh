#!/bin/bash
# Uninstall a skill from Claude Code

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SKILL_NAME=$1
CLAUDE_SKILLS_DIR="${HOME}/.claude/skills"

if [ -z "$SKILL_NAME" ]; then
    echo -e "${RED}Error: Skill name required${NC}"
    echo "Usage: $0 <skill-name>"
    exit 1
fi

SKILL_PATH="$CLAUDE_SKILLS_DIR/$SKILL_NAME"

if [ ! -d "$SKILL_PATH" ]; then
    echo -e "${YELLOW}Skill '$SKILL_NAME' is not installed${NC}"
    exit 0
fi

echo -e "${BLUE}🗑️  Uninstalling skill: ${YELLOW}$SKILL_NAME${NC}"

# Ask for confirmation
read -p "Are you sure you want to remove '$SKILL_NAME'? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Cancelled${NC}"
    exit 0
fi

# Remove the skill directory
rm -rf "$SKILL_PATH"

echo -e "${GREEN}✅ Successfully uninstalled '$SKILL_NAME'${NC}"
