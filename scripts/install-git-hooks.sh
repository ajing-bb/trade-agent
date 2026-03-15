#!/bin/sh
set -eu

repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root"

git config core.hooksPath .githooks
chmod +x .githooks/pre-commit

echo "Installed git hooks:"
echo "  core.hooksPath=.githooks"
echo "  enabled: pre-commit"
