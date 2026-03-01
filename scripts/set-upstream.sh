#!/bin/bash
# Bind a skill to its upstream repository and snapshot current upstream commit.

set -euo pipefail

REGISTRY="$(cd "$(dirname "$0")/.." && pwd)/registry.json"

usage() {
  echo "Usage: $0 <skill-id> <repo-url> [branch]"
  echo "Example: $0 citation-grabber https://github.com/yf8578/citation-grabber.git main"
}

if [ $# -lt 2 ] || [ $# -gt 3 ]; then
  usage
  exit 1
fi

SKILL_ID="$1"
REPO_URL="$2"
BRANCH="${3:-main}"
TODAY="$(date +%F)"

if [ ! -f "$REGISTRY" ]; then
  echo "Error: registry.json not found"
  exit 1
fi

if ! jq -e --arg id "$SKILL_ID" '.skills[] | select(.id==$id)' "$REGISTRY" >/dev/null; then
  echo "Error: skill '$SKILL_ID' not found in registry"
  exit 1
fi

REMOTE_HASH="$(git ls-remote "$REPO_URL" "refs/heads/$BRANCH" | awk 'NR==1{print $1}')"
if [ -z "$REMOTE_HASH" ]; then
  REMOTE_HASH="$(git ls-remote "$REPO_URL" HEAD | awk 'NR==1{print $1}')"
fi

if [ -z "$REMOTE_HASH" ]; then
  echo "Error: failed to resolve remote hash from $REPO_URL"
  exit 1
fi

SOURCE="external"
if echo "$REPO_URL" | grep -q 'github.com'; then
  SOURCE="github"
fi

TMP_FILE="${REGISTRY}.tmp"
jq \
  --arg id "$SKILL_ID" \
  --arg repo "$REPO_URL" \
  --arg source "$SOURCE" \
  --arg branch "$BRANCH" \
  --arg hash "$REMOTE_HASH" \
  --arg today "$TODAY" \
  '
  .skills |= map(
    if .id==$id then
      . + {
        repository: $repo,
        source: $source,
        upstream_branch: $branch,
        upstream_commit: $hash,
        upstream_checked_at: $today
      }
    else . end
  )
  ' "$REGISTRY" > "$TMP_FILE"

mv "$TMP_FILE" "$REGISTRY"

echo "Updated upstream for $SKILL_ID"
echo "repo=$REPO_URL"
echo "branch=$BRANCH"
echo "upstream_commit=$REMOTE_HASH"
