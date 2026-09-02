#!/usr/bin/env bash

set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "::error::Usage: $0 <tag> <ga|beta|preview>"
  exit 2
fi

TAG="$1"
TYPE="$2"

case "$TYPE" in
  ga)
    PATTERN='^v[0-9]+\.[0-9]+\.[0-9]+$'
    EXPECTED='vX.Y.Z'
    ;;

  beta)
    PATTERN='^v[0-9]+\.[0-9]+\.[0-9]+b[0-9]+$'
    EXPECTED='vX.Y.ZbN'
    ;;

  preview)
    PATTERN='^v[0-9]+\.[0-9]+\.[0-9]+a[0-9]+\.[0-9]+$'
    EXPECTED='vX.Y.Za{PR_NUMBER}.{ITERATION}'
    ;;

  *)
    echo "::error::Unknown tag type: $TYPE"
    exit 1
    ;;
esac

if [[ ! "$TAG" =~ $PATTERN ]]; then
  echo "::error::Invalid $TYPE release tag: $TAG"
  echo "Expected format: $EXPECTED"
  exit 1
fi

echo "Valid $TYPE release tag: $TAG"