#!/bin/bash
# Register a skill in registry.json

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SKILL_NAME=$1

if [ -z "$SKILL_NAME" ]; then
    echo -e "${RED}Error: Skill name required${NC}"
    echo "Usage: $0 <skill-name>"
    exit 1
fi

if [ ! -d "$SKILL_NAME" ]; then
    echo -e "${RED}Error: Skill directory not found${NC}"
    exit 1
fi

if [ ! -f "$SKILL_NAME/SKILL.md" ]; then
    echo -e "${RED}Error: SKILL.md not found${NC}"
    exit 1
fi

echo -e "${BLUE}📝 Registering skill: ${YELLOW}$SKILL_NAME${NC}"

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo -e "${RED}Error: 'jq' is required but not installed${NC}"
    echo "Install with: brew install jq (macOS) or apt-get install jq (Linux)"
    exit 1
fi

# Extract metadata from SKILL.md
NAME=$(grep "^name:" "$SKILL_NAME/SKILL.md" | head -1 | cut -d: -f2- | xargs)
DESC=$(grep "^description:" "$SKILL_NAME/SKILL.md" | head -1 | cut -d: -f2- | xargs)
VERSION=$(grep "^version:" "$SKILL_NAME/SKILL.md" | head -1 | cut -d: -f2- | xargs)
CATEGORY=$(grep "category:" "$SKILL_NAME/SKILL.md" | grep -v "^#" | head -1 | cut -d: -f2- | xargs)

# Defaults
VERSION=${VERSION:-"0.1.0"}
CATEGORY=${CATEGORY:-"productivity"}

# Create new skill entry
NEW_SKILL=$(cat <<EOF
{
  "id": "$SKILL_NAME",
  "name": "${NAME:-$SKILL_NAME}",
  "version": "$VERSION",
  "description": "${DESC:-No description}",
  "category": "$CATEGORY",
  "tags": [],
  "path": "$SKILL_NAME",
  "main": "main.py",
  "skill_file": "$SKILL_NAME/SKILL.md",
  "requirements": [],
  "compatible_with": ["claude-code", "openclaw"],
  "status": "development",
  "last_updated": "$(date +%Y-%m-%d)"
}
EOF
)

# Check if skill already exists in registry
if jq -e ".skills[] | select(.id==\"$SKILL_NAME\")" registry.json > /dev/null 2>&1; then
    echo -e "${YELLOW}Skill already registered. Updating...${NC}"
    # Update existing entry
    jq ".skills |= map(if .id==\"$SKILL_NAME\" then $NEW_SKILL else . end)" registry.json > registry.json.tmp
else
    echo -e "${GREEN}Adding new skill to registry...${NC}"
    # Add new entry
    jq ".skills += [$NEW_SKILL]" registry.json > registry.json.tmp
fi

# Update total count
jq '.metadata.total_skills = (.skills | length)' registry.json.tmp > registry.json
rm registry.json.tmp

echo -e "${GREEN}✅ Successfully registered '$SKILL_NAME'${NC}"
echo -e "${BLUE}📊 Total skills: $(jq '.metadata.total_skills' registry.json)${NC}"
