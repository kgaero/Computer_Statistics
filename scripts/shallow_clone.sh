#!/usr/bin/env bash
# Shallow-clone helper that keeps top-level and nested submodules at depth 1.
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  shallow_clone.sh <repo-url>                  # fresh clone
  shallow_clone.sh --hydrate-existing [path]   # only hydrate submodules

Environment variables:
  SHALLOW_CLONE_JOBS   Number of parallel clone/update jobs (default: 4)
  SKIP_SUBMODULE_SYNC  Set to 1 to skip `git submodule sync`
USAGE
}

trim_trailing_slash() {
  local value="$1"
  value="${value%/}"
  printf '%s' "$value"
}

repo_basename() {
  local url="$1"
  url=$(trim_trailing_slash "$url")
  url="${url##*:}"
  url="${url##*/}"
  url="${url%.git}"
  printf '%s' "$url"
}

verify_submodules() {
  local repo_path="$1"
  local missing
  missing=$(git -C "$repo_path" submodule status --recursive | grep '^-' || true)
  if [[ -n "$missing" ]]; then
    echo "[shallow-clone] Submodules missing commits. Rerun hydration or inspect .gitmodules." >&2
    echo "$missing" >&2
    exit 1
  fi
}

hydrate_submodules() {
  local repo_path="$1"
  local jobs="$2"

  if [[ "${SKIP_SUBMODULE_SYNC:-0}" != "1" ]]; then
    git -C "$repo_path" submodule sync --recursive
  fi

  git -C "$repo_path" config submodule.recurse true >/dev/null
  git -C "$repo_path" submodule update --init --recursive \
    --depth 1 --jobs "$jobs" --recommend-shallow

  verify_submodules "$repo_path"
}

if [[ $# -eq 0 ]]; then
  usage
  exit 1
fi

JOBS="${SHALLOW_CLONE_JOBS:-4}"

if [[ "$1" == "--help" || "$1" == "-h" ]]; then
  usage
  exit 0
fi

if [[ "$1" == "--hydrate-existing" ]]; then
  shift
  target="${1:-$(pwd)}"
  if [[ ! -d "$target/.git" ]]; then
    echo "[shallow-clone] '$target' is not a git repository" >&2
    exit 1
  fi
  hydrate_submodules "$target" "$JOBS"
  exit 0
fi

REPO_URL="$1"
DEST_DIR="${2:-$(repo_basename "$REPO_URL")}"

if [[ -e "$DEST_DIR" ]]; then
  echo "[shallow-clone] Destination '$DEST_DIR' already exists" >&2
  exit 1
fi

printf '[shallow-clone] Cloning %s -> %s\n' "$REPO_URL" "$DEST_DIR"
git clone --depth=1 --recurse-submodules --shallow-submodules \
  --jobs="$JOBS" "$REPO_URL" "$DEST_DIR"

hydrate_submodules "$DEST_DIR" "$JOBS"

printf '[shallow-clone] Done. Repo ready at %s\n' "$DEST_DIR"
