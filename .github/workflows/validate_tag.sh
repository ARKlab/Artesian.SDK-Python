#!/usr/bin/env bash

set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "::error::Usage: $0 <tag> <ga|beta|dev|rc|preview>"
  exit 2
fi

TAG="$1"
TYPE="$2"

case "$TYPE" in
  ga)
    PATTERN='^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$'
    EXPECTED='vX.Y.Z'
    ;;

  beta)
    PATTERN='^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)b(0|[1-9][0-9]*)$'
    EXPECTED='vX.Y.ZbN'
    ;;

  dev)
    PATTERN='^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.dev(0|[1-9][0-9]*)$'
    EXPECTED='vX.Y.Z.devN'
    ;;

  rc)
    PATTERN='^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)rc(0|[1-9][0-9]*)$'
    EXPECTED='vX.Y.ZrcN'
    ;;

  preview)
    PATTERN='^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)a(0|[1-9][0-9]*)\.post(0|[1-9][0-9]*)$'
    EXPECTED='vX.Y.Za{PR_NUMBER}.post{ITERATION}'
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

if [[ "${GITHUB_REF:-}" == refs/tags/* ]]; then
  git fetch --no-tags origin "$GITHUB_REF"
  if [[ "$(git rev-parse FETCH_HEAD^{commit})" != "$(git rev-parse HEAD)" ]]; then
    echo "::error::Release tag no longer points to the checked-out commit."
    exit 1
  fi
fi

echo "Valid $TYPE release tag: $TAG"