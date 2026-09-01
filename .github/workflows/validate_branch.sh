#!/usr/bin/env bash

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "::error::Usage: $0 <expected-branch>"
  exit 2
fi

EXPECTED_BRANCH="$1"

git fetch origin "$EXPECTED_BRANCH"

if ! git merge-base --is-ancestor "$GITHUB_SHA" "origin/$EXPECTED_BRANCH"; then
  echo "::error::Release tag does not point to a commit contained in $EXPECTED_BRANCH."
  exit 1
fi

echo "Release commit is contained in $EXPECTED_BRANCH."