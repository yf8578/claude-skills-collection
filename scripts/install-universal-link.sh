#!/bin/bash
# Universal installer using SYMBOLIC LINKS (recommended)
# Advantages:
#   - No duplicate files
#   - Auto-sync when you update skills in collection
#   - Saves disk space

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

SKILL_NAME=$1
COLLECTION_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [ -z "$SKILL_NAME" ]; then
    echo -e "${RED}Error: Skill name required${NC}"
    echo "Usage: $0 <skill-name>"
    exit 1
fi

if [ ! -d "$COLLECTION_DIR/$SKILL_NAME" ]; then
    echo -e "${RED}Error: Skill directory not found${NC}"
    exit 1
fi

SKILL_PATH="$COLLECTION_DIR/$SKILL_NAME"

echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${BLUE}🔗 Universal Skill Linker (Symlink Mode)${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Linking:${NC} ${YELLOW}$SKILL_NAME${NC}"
echo -e "${BLUE}Source:${NC} $SKILL_PATH"
echo ""
echo -e "${GREEN}✨ Using symbolic links (no file duplication)${NC}"
echo ""

INSTALLED_COUNT=0

# Function to create symlink and handle existing installations
create_link() {
    local target_dir=$1
    local target_path="$target_dir/$SKILL_NAME"

    # Remove existing (link or directory)
    if [ -L "$target_path" ]; then
        rm "$target_path"
    elif [ -d "$target_path" ]; then
        rm -rf "$target_path"
    fi

    # Create link
    mkdir -p "$target_dir"
    ln -s "$SKILL_PATH" "$target_path"
}

# 1. Claude Code
if [ -d "$HOME/.claude" ]; then
    echo -e "${BLUE}[Claude Code]${NC} Detected"
    create_link "$HOME/.claude/skills"
    echo -e "  ${GREEN}✓${NC} Linked: ~/.claude/skills/$SKILL_NAME → collection"
    ((INSTALLED_COUNT++))
else
    echo -e "${YELLOW}[Claude Code]${NC} Not found"
fi

echo ""

# 2. OpenClaw
# Note: OpenClaw might not support symlinks, fallback to copy
if command -v clawhub &> /dev/null; then
    echo -e "${BLUE}[OpenClaw]${NC} Detected"
    if [ -d "$HOME/.openclaw/skills" ]; then
        # Try symlink first
        if create_link "$HOME/.openclaw/skills" 2>/dev/null; then
            echo -e "  ${GREEN}✓${NC} Linked: ~/.openclaw/skills/$SKILL_NAME"
            ((INSTALLED_COUNT++))
        else
            # Fallback to copy
            echo -e "  ${YELLOW}⚠${NC}  Symlinks not supported, using copy instead"
            cp -r "$SKILL_PATH" "$HOME/.openclaw/skills/"
            echo -e "  ${GREEN}✓${NC} Copied to ~/.openclaw/skills/$SKILL_NAME"
            ((INSTALLED_COUNT++))
        fi
    fi
else
    echo -e "${YELLOW}[OpenClaw]${NC} Not found"
fi

echo ""

# 3. Codex
if [ -d "$HOME/.codex" ] || command -v codex &> /dev/null; then
    echo -e "${BLUE}[Codex]${NC} Detected"
    create_link "$HOME/.codex/skills"
    echo -e "  ${GREEN}✓${NC} Linked: ~/.codex/skills/$SKILL_NAME → collection"
    ((INSTALLED_COUNT++))
else
    echo -e "${YELLOW}[Codex]${NC} Not found"
fi

echo ""

# 4. Gemini CLI
if command -v gemini &> /dev/null || [ -d "$HOME/.gemini" ]; then
    echo -e "${BLUE}[Gemini CLI]${NC} Detected"

    # Try to read config
    GEMINI_TOOLS="$HOME/.gemini/tools"
    if [ -f "$HOME/.gemini/config.yaml" ]; then
        GEMINI_TOOLS=$(grep -A 2 "^tools:" "$HOME/.gemini/config.yaml" 2>/dev/null | grep "path:" | head -1 | cut -d: -f2- | xargs)
        if [ -z "$GEMINI_TOOLS" ]; then
            GEMINI_TOOLS="$HOME/.gemini/tools"
        fi
    fi

    create_link "$GEMINI_TOOLS"
    echo -e "  ${GREEN}✓${NC} Linked: $GEMINI_TOOLS/$SKILL_NAME → collection"
    ((INSTALLED_COUNT++))
else
    echo -e "${YELLOW}[Gemini CLI]${NC} Not found"
fi

echo ""

# 5. Google Antigravity
if command -v antigravity &> /dev/null || [ -d "$HOME/.antigravity" ]; then
    echo -e "${BLUE}[Google Antigravity]${NC} Detected (Experimental)"

    if [ -d "$HOME/.antigravity/extensions" ] || mkdir -p "$HOME/.antigravity/extensions" 2>/dev/null; then
        create_link "$HOME/.antigravity/extensions"
        echo -e "  ${GREEN}✓${NC} Linked: ~/.antigravity/extensions/$SKILL_NAME"
        ((INSTALLED_COUNT++))
    else
        echo -e "  ${YELLOW}⚠${NC}  Unable to create link"
    fi
else
    echo -e "${YELLOW}[Google Antigravity]${NC} Not found"
fi

echo ""

# Install dependencies
if [ -f "$SKILL_PATH/requirements.txt" ]; then
    echo -e "${BLUE}[Dependencies]${NC} Installing Python packages..."
    if pip3 install -q -r "$SKILL_PATH/requirements.txt"; then
        echo -e "  ${GREEN}✓${NC} Dependencies installed"
    else
        echo -e "  ${YELLOW}⚠${NC}  Some dependencies may have failed"
    fi
    echo ""
fi

# Summary
echo -e "${CYAN}═══════════════════════════════════════${NC}"
if [ $INSTALLED_COUNT -eq 0 ]; then
    echo -e "${YELLOW}⚠  No compatible AI CLI tools detected${NC}"
else
    echo -e "${GREEN}✅ Linking successful!${NC}"
    echo ""
    echo -e "Linked to ${GREEN}$INSTALLED_COUNT${NC} platform(s)"
    echo ""
    echo -e "${GREEN}🎉 Advantages of symlinks:${NC}"
    echo -e "   ${GREEN}•${NC} No duplicate files - saves disk space"
    echo -e "   ${GREEN}•${NC} Updates in collection apply everywhere automatically"
    echo -e "   ${GREEN}•${NC} Single source of truth: $COLLECTION_DIR"
    echo ""
    echo -e "${YELLOW}💡 Tip:${NC} Edit skills in collection, changes reflect immediately!"
fi
echo -e "${CYAN}═══════════════════════════════════════${NC}"
