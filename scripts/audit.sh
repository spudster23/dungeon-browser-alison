#!/usr/bin/env bash
# CVE gate: fails on any known vulnerability in the locked dependency set.
set -euo pipefail
cd "$(dirname "$0")/.."
uv export --format requirements-txt --no-emit-project --locked 2>/dev/null \
  | uvx pip-audit -r /dev/stdin --disable-pip --require-hashes
