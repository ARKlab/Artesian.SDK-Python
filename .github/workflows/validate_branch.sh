#!/usr/bin/env bash

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "::error::Usage: $0 <expected-branch>"
  exit 2
fi

EXPECTED_BRANCH="$1"

git fetch origin "$EXPECTED_BRANCH"

COMMIT_SHA="$GITHUB_SHA"
if [[ "${GITHUB_REF:-}" == refs/tags/* ]]; then
  COMMIT_SHA="$(git rev-parse "${GITHUB_REF}^{commit}")"
fi

if ! git merge-base --is-ancestor "$COMMIT_SHA" "origin/$EXPECTED_BRANCH"; then
  echo "::error::Release tag does not point to a commit contained in $EXPECTED_BRANCH."
  exit 1
fi

echo "Release commit is contained in $EXPECTED_BRANCH."