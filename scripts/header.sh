#!/usr/bin/env bash

set -e

error () {
  echo -e "\n${WARN_COLOR}[\xE2\x9C\x98] $1\n${NC}" >&2
  exit 1
}

get_repo_root () {
  # Check if the current directory is inside a Git repository
  if [ -d .git ] || git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    # Get the root directory of the Git repository
    repo_root="$(git rev-parse --show-toplevel)"
    echo "$repo_root"
  else
    error "Not inside a Git repository."
  fi
}

test_command_outcome () {
  if test $? -eq 0
  then
    echo -e "${OK_COLOR}[\xE2\x9C\x94] $1${NC}"
  else
    error "$1 failed. Correct the issues and try again."
  fi
}

# Colors
WARN_COLOR='\033[0;33m'
OK_COLOR='\033[0;92m'
NC='\033[0m' # No Color