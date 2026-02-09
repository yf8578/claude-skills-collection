#!/bin/bash
# Launch Skills Store - Interactive TUI
# Beautiful interface for browsing and installing skills

COLLECTION_DIR="$HOME/00zyf/AI/claude-skills-collection"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🏪 Launching Skills Store...${NC}"
echo ""

# Check if dependencies are installed
if ! python3 -c "import textual" 2>/dev/null; then
    echo -e "${YELLOW}📦 First-time setup: Installing dependencies...${NC}"
    pip3 install -q textual requests rich || {
        echo -e "${YELLOW}⚠️  Failed to install automatically${NC}"
        echo -e "${YELLOW}   Please install manually:${NC}"
        echo -e "   ${GREEN}pip3 install textual requests rich${NC}"
        exit 1
    }
    echo -e "${GREEN}✓ Dependencies installed${NC}"
    echo ""
fi

# Launch
cd "$COLLECTION_DIR"
python3 "$SCRIPT_DIR/skill-store.py" "$@"
