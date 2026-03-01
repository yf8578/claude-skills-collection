#!/bin/bash
# Check whether tracked skills have newer upstream commits.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REGISTRY="$ROOT_DIR/registry.json"
UPDATE_LOCK=false
TARGET_SKILL=""

usage() {
  echo "Usage: $0 [--update-lock] [skill-id]"
  echo "  --update-lock   write latest remote hashes into registry upstream_commit"
}

while [ $# -gt 0 ]; do
  case "$1" in
    --update-lock)
      UPDATE_LOCK=true
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      if [ -n "$TARGET_SKILL" ]; then
        echo "Error: only one skill-id can be specified"
        exit 1
      fi
      TARGET_SKILL="$1"
      ;;
  esac
  shift
done

if [ ! -f "$REGISTRY" ]; then
  echo "Error: registry.json not found"
  exit 1
fi

FILTER='.skills[] | select((.repository // "") != "")'
if [ -n "$TARGET_SKILL" ]; then
  FILTER="$FILTER | select(.id==\"$TARGET_SKILL\")"
fi

ROWS="$(jq -r "$FILTER | [.id, .repository, (.upstream_branch // \"main\"), (.upstream_commit // \"\")] | @tsv" "$REGISTRY")"
if [ -z "$ROWS" ]; then
  echo "No tracked skills found (skills with repository field)."
  if [ -n "$TARGET_SKILL" ]; then
    echo "Tip: bind source first: ./scripts/set-upstream.sh $TARGET_SKILL <repo-url> [branch]"
  fi
  exit 0
fi

ok=0
update=0
untracked=0
failed=0
TODAY="$(date +%F)"

while IFS=$'\t' read -r id repo branch locked_hash; do
  [ -n "$id" ] || continue

  remote_hash="$(git ls-remote "$repo" "refs/heads/$branch" | awk 'NR==1{print $1}')"
  if [ -z "$remote_hash" ]; then
    remote_hash="$(git ls-remote "$repo" HEAD | awk 'NR==1{print $1}')"
  fi

  if [ -z "$remote_hash" ]; then
    echo "[FAIL] $id  cannot access $repo"
    failed=$((failed+1))
    continue
  fi

  if [ -z "$locked_hash" ]; then
    echo "[UNTRACKED] $id  remote=$remote_hash  (no upstream_commit baseline)"
    untracked=$((untracked+1))
  elif [ "$locked_hash" = "$remote_hash" ]; then
    echo "[OK] $id  $remote_hash"
    ok=$((ok+1))
  else
    echo "[UPDATE] $id"
    echo "  locked=$locked_hash"
    echo "  remote=$remote_hash"
    update=$((update+1))
  fi

  if [ "$UPDATE_LOCK" = true ]; then
    tmp_file="${REGISTRY}.tmp"
    jq \
      --arg id "$id" \
      --arg hash "$remote_hash" \
      --arg today "$TODAY" \
      '.skills |= map(if .id==$id then . + {upstream_commit: $hash, upstream_checked_at: $today} else . end)' \
      "$REGISTRY" > "$tmp_file"
    mv "$tmp_file" "$REGISTRY"
  fi

done <<< "$ROWS"

echo ""
echo "Summary: ok=$ok update=$update untracked=$untracked failed=$failed"
if [ "$UPDATE_LOCK" = true ]; then
  echo "registry.json has been updated with latest upstream_commit values."
fi
