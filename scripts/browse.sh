#!/bin/bash
# Launch the Skills Browser
# A beautiful TUI for browsing and installing skills

COLLECTION_DIR="$HOME/00zyf/AI/claude-skills-collection"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if textual is installed
if ! python3 -c "import textual" 2>/dev/null; then
    echo -e "${YELLOW}📦 Installing dependencies...${NC}"
    pip3 install -q -r "$COLLECTION_DIR/requirements-browser.txt"
fi

# Launch the browser
cd "$COLLECTION_DIR"
python3 "$SCRIPT_DIR/browse-skills.py" "$@"
