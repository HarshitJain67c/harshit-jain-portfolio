#!/usr/bin/env bash
set -euo pipefail

python3 tests/validate_site.py
if command -v node >/dev/null 2>&1; then
  node --check script.js
fi

if rg -n 'href="#"|src=""|href=""|TODO|FIXME' index.html styles.css script.js; then
  echo "Placeholder or unfinished content found" >&2
  exit 1
fi
