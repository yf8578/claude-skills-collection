#!/bin/bash
# Universal installer - detects and installs skills for multiple AI CLI tools

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
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

echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo -e "${BLUE}🌍 Universal Skill Installer${NC}"
echo -e "${CYAN}═══════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Installing:${NC} ${YELLOW}$SKILL_NAME${NC}"
echo ""

INSTALLED_COUNT=0

# 1. Claude Code
if [ -d "$HOME/.claude" ]; then
    echo -e "${BLUE}[Claude Code]${NC} Detected"
    mkdir -p "$HOME/.claude/skills"
    cp -r "$SKILL_NAME" "$HOME/.claude/skills/"
    echo -e "  ${GREEN}✓${NC} Installed to ~/.claude/skills/$SKILL_NAME"
    ((INSTALLED_COUNT++))
else
    echo -e "${YELLOW}[Claude Code]${NC} Not found"
fi

echo ""

# 2. OpenClaw / ClawHub
if command -v clawhub &> /dev/null; then
    echo -e "${BLUE}[OpenClaw]${NC} Detected"
    if clawhub sync --local "./$SKILL_NAME" 2>/dev/null; then
        echo -e "  ${GREEN}✓${NC} Synced via clawhub"
        ((INSTALLED_COUNT++))
    else
        echo -e "  ${YELLOW}⚠${NC}  Sync failed, trying alternative method..."
        # Alternative: copy to OpenClaw directory if exists
        if [ -d "$HOME/.openclaw/skills" ]; then
            cp -r "$SKILL_NAME" "$HOME/.openclaw/skills/"
            echo -e "  ${GREEN}✓${NC} Installed to ~/.openclaw/skills/$SKILL_NAME"
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
    mkdir -p "$HOME/.codex/skills"
    cp -r "$SKILL_NAME" "$HOME/.codex/skills/"
    echo -e "  ${GREEN}✓${NC} Installed to ~/.codex/skills/$SKILL_NAME"
    ((INSTALLED_COUNT++))
else
    echo -e "${YELLOW}[Codex]${NC} Not found"
fi

echo ""

# 4. Gemini CLI
if command -v gemini &> /dev/null || [ -d "$HOME/.gemini" ]; then
    echo -e "${BLUE}[Gemini CLI]${NC} Detected"

    # Try to read config
    if [ -f "$HOME/.gemini/config.yaml" ]; then
        # Extract tools path from config
        GEMINI_TOOLS=$(grep -A 2 "^tools:" "$HOME/.gemini/config.yaml" 2>/dev/null | grep "path:" | head -1 | cut -d: -f2- | xargs)

        if [ ! -z "$GEMINI_TOOLS" ]; then
            mkdir -p "$GEMINI_TOOLS"
            cp -r "$SKILL_NAME" "$GEMINI_TOOLS/"
            echo -e "  ${GREEN}✓${NC} Installed to $GEMINI_TOOLS/$SKILL_NAME"
            ((INSTALLED_COUNT++))
        else
            # Default path
            mkdir -p "$HOME/.gemini/tools"
            cp -r "$SKILL_NAME" "$HOME/.gemini/tools/"
            echo -e "  ${GREEN}✓${NC} Installed to ~/.gemini/tools/$SKILL_NAME"
            echo -e "  ${YELLOW}⚠${NC}  You may need to configure this path in ~/.gemini/config.yaml"
            ((INSTALLED_COUNT++))
        fi
    else
        # No config file, use default
        mkdir -p "$HOME/.gemini/tools"
        cp -r "$SKILL_NAME" "$HOME/.gemini/tools/"
        echo -e "  ${GREEN}✓${NC} Installed to ~/.gemini/tools/$SKILL_NAME"
        ((INSTALLED_COUNT++))
    fi
else
    echo -e "${YELLOW}[Gemini CLI]${NC} Not found"
fi

echo ""

# 5. Google Antigravity (experimental)
if command -v antigravity &> /dev/null || [ -d "$HOME/.antigravity" ]; then
    echo -e "${BLUE}[Google Antigravity]${NC} Detected (Experimental)"

    if [ -d "$HOME/.antigravity/extensions" ]; then
        cp -r "$SKILL_NAME" "$HOME/.antigravity/extensions/"
        echo -e "  ${GREEN}✓${NC} Installed to ~/.antigravity/extensions/$SKILL_NAME"
        ((INSTALLED_COUNT++))
    else
        echo -e "  ${YELLOW}⚠${NC}  Unable to determine installation path"
    fi
else
    echo -e "${YELLOW}[Google Antigravity]${NC} Not found"
fi

echo ""

# Install dependencies
if [ -f "$SKILL_NAME/requirements.txt" ]; then
    echo -e "${BLUE}[Dependencies]${NC} Installing Python packages..."
    if pip3 install -q -r "$SKILL_NAME/requirements.txt"; then
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
    echo ""
    echo "This skill can still be used as a standalone tool:"
    echo -e "  ${BLUE}cd $SKILL_NAME${NC}"
    echo -e "  ${BLUE}python3 main.py [options]${NC}"
else
    echo -e "${GREEN}✅ Installation successful!${NC}"
    echo ""
    echo -e "Installed for ${GREEN}$INSTALLED_COUNT${NC} platform(s)"
    echo ""
    echo -e "${YELLOW}💡 Tip:${NC} Restart your AI CLI tool to load the new skill"
fi
echo -e "${CYAN}═══════════════════════════════════════${NC}"
