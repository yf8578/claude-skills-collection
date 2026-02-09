#!/bin/bash
# Check installation status of a skill

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

echo -e "${BLUE}📊 Skill Status: ${YELLOW}$SKILL_NAME${NC}"
echo ""

# Check if skill exists in collection
if [ -d "$SKILL_NAME" ]; then
    echo -e "${GREEN}✓${NC} Skill exists in collection"

    if [ -f "$SKILL_NAME/SKILL.md" ]; then
        echo -e "${GREEN}✓${NC} SKILL.md found"
    else
        echo -e "${RED}✗${NC} SKILL.md not found"
    fi
else
    echo -e "${RED}✗${NC} Skill not found in collection"
fi

echo ""

# Check if skill is installed
if [ -d "$CLAUDE_SKILLS_DIR/$SKILL_NAME" ]; then
    echo -e "${GREEN}✓${NC} Installed in Claude Code"
    echo -e "   Location: $CLAUDE_SKILLS_DIR/$SKILL_NAME"

    # Check if dependencies are installed
    if [ -f "$SKILL_NAME/requirements.txt" ]; then
        echo ""
        echo -e "${BLUE}Checking dependencies...${NC}"
        while IFS= read -r dep; do
            pkg=$(echo "$dep" | cut -d'>' -f1 | cut -d'=' -f1 | cut -d'<' -f1 | xargs)
            if python3 -c "import $pkg" 2>/dev/null; then
                echo -e "${GREEN}✓${NC} $dep"
            else
                echo -e "${RED}✗${NC} $dep (not installed)"
            fi
        done < "$SKILL_NAME/requirements.txt"
    fi
else
    echo -e "${RED}✗${NC} Not installed in Claude Code"
    echo -e "   Run: ./scripts/install.sh $SKILL_NAME"
fi
