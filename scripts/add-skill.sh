#!/bin/bash
# Add external skill to collection and install to all platforms
# Automatically handles ClawHub, GitHub, and local directories

set -e

COLLECTION_DIR="$HOME/00zyf/AI/claude-skills-collection"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_usage() {
    echo -e "${BLUE}Usage:${NC}"
    echo "  ./add-skill.sh <source> [options]"
    echo ""
    echo -e "${BLUE}Sources:${NC}"
    echo "  clawhub:skill-name      Download from ClawHub"
    echo "  github:user/repo        Clone from GitHub"
    echo "  local:/path/to/skill    Copy from local directory"
    echo "  /path/to/skill          Copy from local directory (auto-detected)"
    echo ""
    echo -e "${BLUE}Options:${NC}"
    echo "  --symlink               Use symbolic links (default)"
    echo "  --copy                  Use file copy instead of symlinks"
    echo "  --no-install            Don't install to platforms (only add to collection)"
    echo "  --no-commit             Don't commit to git"
    echo ""
    echo -e "${BLUE}Examples:${NC}"
    echo "  ./add-skill.sh clawhub:pdf-analyzer"
    echo "  ./add-skill.sh github:someuser/awesome-skill"
    echo "  ./add-skill.sh local:/tmp/my-skill"
    echo "  ./add-skill.sh /tmp/my-skill"
}

if [ $# -eq 0 ]; then
    print_usage
    exit 1
fi

SOURCE="$1"
USE_SYMLINK=true
DO_INSTALL=true
DO_COMMIT=true

# Parse options
shift
while [ $# -gt 0 ]; do
    case "$1" in
        --symlink)
            USE_SYMLINK=true
            ;;
        --copy)
            USE_SYMLINK=false
            ;;
        --no-install)
            DO_INSTALL=false
            ;;
        --no-commit)
            DO_COMMIT=false
            ;;
        *)
            echo -e "${RED}❌ Unknown option: $1${NC}"
            print_usage
            exit 1
            ;;
    esac
    shift
done

echo -e "${BLUE}🎯 Adding skill to collection...${NC}"
echo ""

# Determine source type and skill name
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

if [[ "$SOURCE" =~ ^clawhub: ]]; then
    # ClawHub source
    SKILL_NAME="${SOURCE#clawhub:}"
    echo -e "${BLUE}📦 Downloading from ClawHub: ${YELLOW}$SKILL_NAME${NC}"

    # Check if clawhub is installed
    if ! command -v clawhub &> /dev/null; then
        echo -e "${RED}❌ clawhub is not installed${NC}"
        echo -e "${YELLOW}💡 Install it from: https://clawhub.ai/${NC}"
        exit 1
    fi

    # Download to temp directory
    cd "$TEMP_DIR"
    clawhub install "$SKILL_NAME" || {
        echo -e "${RED}❌ Failed to download from ClawHub${NC}"
        exit 1
    }

    # Find where clawhub installed it
    if [ -d "$HOME/.openclaw/skills/$SKILL_NAME" ]; then
        SKILL_SOURCE="$HOME/.openclaw/skills/$SKILL_NAME"
    else
        echo -e "${RED}❌ Skill not found in ~/.openclaw/skills/$SKILL_NAME${NC}"
        exit 1
    fi

elif [[ "$SOURCE" =~ ^github: ]]; then
    # GitHub source
    REPO="${SOURCE#github:}"
    SKILL_NAME=$(basename "$REPO")
    echo -e "${BLUE}📦 Cloning from GitHub: ${YELLOW}$REPO${NC}"

    cd "$TEMP_DIR"
    git clone "https://github.com/$REPO.git" "$SKILL_NAME" || {
        echo -e "${RED}❌ Failed to clone from GitHub${NC}"
        exit 1
    }

    SKILL_SOURCE="$TEMP_DIR/$SKILL_NAME"

elif [[ "$SOURCE" =~ ^local: ]] || [ -d "$SOURCE" ]; then
    # Local directory
    if [[ "$SOURCE" =~ ^local: ]]; then
        SKILL_SOURCE="${SOURCE#local:}"
    else
        SKILL_SOURCE="$SOURCE"
    fi

    # Expand ~ to home directory
    SKILL_SOURCE="${SKILL_SOURCE/#\~/$HOME}"

    if [ ! -d "$SKILL_SOURCE" ]; then
        echo -e "${RED}❌ Directory not found: $SKILL_SOURCE${NC}"
        exit 1
    fi

    SKILL_NAME=$(basename "$SKILL_SOURCE")
    echo -e "${BLUE}📁 Copying from local: ${YELLOW}$SKILL_SOURCE${NC}"

else
    echo -e "${RED}❌ Invalid source: $SOURCE${NC}"
    print_usage
    exit 1
fi

# Validate skill structure
if [ ! -f "$SKILL_SOURCE/SKILL.md" ]; then
    echo -e "${YELLOW}⚠️  Warning: No SKILL.md found in $SKILL_NAME${NC}"
    echo -e "${YELLOW}   This skill may not work properly with AI tools${NC}"
fi

# Copy to collection
DEST_DIR="$COLLECTION_DIR/$SKILL_NAME"

if [ -d "$DEST_DIR" ]; then
    echo -e "${YELLOW}⚠️  Skill already exists: $SKILL_NAME${NC}"
    read -p "   Overwrite? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}❌ Cancelled${NC}"
        exit 0
    fi
    rm -rf "$DEST_DIR"
fi

echo -e "${BLUE}📋 Copying to collection: ${YELLOW}$DEST_DIR${NC}"
cp -r "$SKILL_SOURCE" "$DEST_DIR"

# Remove .git directory if exists
if [ -d "$DEST_DIR/.git" ]; then
    rm -rf "$DEST_DIR/.git"
    echo -e "${BLUE}   Removed .git directory${NC}"
fi

echo -e "${GREEN}✅ Skill added to collection!${NC}"
echo ""

# Register in registry.json
echo -e "${BLUE}📝 Registering in registry.json...${NC}"
cd "$COLLECTION_DIR"

if ! ./scripts/register.sh "$SKILL_NAME"; then
    echo -e "${YELLOW}⚠️  Warning: Registration might have failed, but skill is in collection${NC}"
fi

echo ""

# Install to platforms
if [ "$DO_INSTALL" = true ]; then
    echo -e "${BLUE}🚀 Installing to all platforms...${NC}"

    if [ "$USE_SYMLINK" = true ]; then
        ./scripts/install-universal-link.sh "$SKILL_NAME"
    else
        ./scripts/install-universal.sh "$SKILL_NAME"
    fi

    echo ""
fi

# Git commit
if [ "$DO_COMMIT" = true ]; then
    echo -e "${BLUE}📦 Committing to git...${NC}"

    git add "$SKILL_NAME"
    git add registry.json 2>/dev/null || true

    git commit -m "feat: Add skill $SKILL_NAME

Added via add-skill.sh from: $SOURCE

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>" || {
        echo -e "${YELLOW}⚠️  Nothing to commit (skill might already be tracked)${NC}"
    }

    echo ""
fi

# Summary
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✨ Successfully added skill: ${YELLOW}$SKILL_NAME${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}📍 Location:${NC} $DEST_DIR"

if [ "$DO_INSTALL" = true ]; then
    echo -e "${BLUE}🎯 Installed to:${NC}"
    [ -d "$HOME/.claude/skills/$SKILL_NAME" ] && echo "   ✅ Claude Code"
    [ -L "$HOME/.codex/skills/$SKILL_NAME" ] || [ -d "$HOME/.codex/skills/$SKILL_NAME" ] && echo "   ✅ Codex"
    [ -L "$HOME/.gemini/tools/$SKILL_NAME" ] || [ -d "$HOME/.gemini/tools/$SKILL_NAME" ] && echo "   ✅ Gemini CLI"
    [ -L "$HOME/.antigravity/extensions/$SKILL_NAME" ] || [ -d "$HOME/.antigravity/extensions/$SKILL_NAME" ] && echo "   ✅ Antigravity"
fi

echo ""
echo -e "${YELLOW}💡 Next steps:${NC}"
echo "   1. Restart your AI tools to load the skill"
echo "   2. Test the skill: ./scripts/status.sh $SKILL_NAME"
echo "   3. List all skills: ./scripts/list.sh"
if [ "$DO_COMMIT" = true ]; then
    echo "   4. Push to GitHub: git push"
fi

echo ""
echo -e "${GREEN}🎉 Done!${NC}"
