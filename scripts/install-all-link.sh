#!/bin/bash
# Install all skills using symbolic links

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🔗 Linking all skills...${NC}"
echo ""

# Get list of skill directories (exclude scripts, templates, docs)
SKILLS=$(ls -d */ 2>/dev/null | grep -v "scripts\|templates\|docs" | sed 's#/##')

if [ -z "$SKILLS" ]; then
    echo -e "${YELLOW}No skills found to link${NC}"
    exit 0
fi

SUCCESS=0
FAILED=0

for SKILL in $SKILLS; do
    echo -e "${BLUE}Linking: $SKILL${NC}"
    if ./scripts/install-universal-link.sh "$SKILL"; then
        ((SUCCESS++))
    else
        ((FAILED++))
    fi
    echo ""
done

echo -e "${GREEN}✅ Linking complete!${NC}"
echo -e "   ${GREEN}Success: $SUCCESS${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "   ${YELLOW}Failed: $FAILED${NC}"
fi
