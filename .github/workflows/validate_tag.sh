#!/usr/bin/env bash
set -euo pipefail

TAG="$1"
EXPECTED_BRANCH="$2"

git fetch origin "$EXPECTED_BRANCH" --tags

if ! TAG_COMMIT="$(git rev-parse -q --verify "${TAG}^{commit}")"; then
  echo "::error::Tag $TAG could not be resolved to a commit."
  exit 1
fi
echo "Tag:             $TAG"
echo "Tag commit:      $TAG_COMMIT"
echo "Expected branch: $EXPECTED_BRANCH"
echo "Branch HEAD:     $(git rev-parse "origin/$EXPECTED_BRANCH")"

if ! git merge-base --is-ancestor "$TAG_COMMIT" "origin/$EXPECTED_BRANCH"; then
  echo "::error::Tag $TAG does not point to a commit contained in $EXPECTED_BRANCH."
  exit 1
fi

echo "Tag commit is contained in $EXPECTED_BRANCH."