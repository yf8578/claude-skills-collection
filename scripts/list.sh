#!/bin/bash
# List all available skills with details

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}📚 Available Skills${NC}"
echo ""

# Check if registry.json exists
if [ ! -f "registry.json" ]; then
    echo -e "${YELLOW}Warning: registry.json not found${NC}"
    echo "Listing directories instead..."
    ls -d */ 2>/dev/null | grep -v "scripts\|templates\|docs" | sed 's#/##'
    exit 0
fi

# Parse registry.json and display skills
# This is a simple version; for production, use jq for JSON parsing
if command -v jq &> /dev/null; then
    # Use jq if available
    echo -e "${CYAN}Using registry.json for details:${NC}"
    echo ""

    jq -r '.skills[] | "  \u001b[1;33m\(.name)\u001b[0m (\(.version))\n    📁 \(.id)\n    📝 \(.description)\n    🏷️  \(.category) | Status: \(.status)\n    🔗 \(.repository)\n"' registry.json

    echo -e "${GREEN}Total skills: $(jq '.metadata.total_skills' registry.json)${NC}"
else
    # Fallback: simple directory listing
    echo -e "${YELLOW}Tip: Install 'jq' for detailed skill information${NC}"
    echo ""
    ls -d */ 2>/dev/null | grep -v "scripts\|templates\|docs" | sed 's#/##' | while read skill; do
        echo -e "  ${GREEN}✓${NC} $skill"
        if [ -f "$skill/SKILL.md" ]; then
            # Extract name from SKILL.md
            NAME=$(grep "^name:" "$skill/SKILL.md" 2>/dev/null | head -1 | cut -d: -f2- | xargs)
            DESC=$(grep "^description:" "$skill/SKILL.md" 2>/dev/null | head -1 | cut -d: -f2- | xargs)
            [ ! -z "$NAME" ] && echo -e "    Name: $NAME"
            [ ! -z "$DESC" ] && echo -e "    Desc: $DESC"
        fi
        echo ""
    done
fi
