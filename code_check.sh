#!/usr/bin/env bash

set -e

runcmd() {
    echo "[*] Running $1..."
    if ! "$@"; then
        echo "[!] Error in $1"
        exit 1
    fi
}

# Formatting code with black
runcmd black .

# Spell checking with codespell
runcmd codespell -q 3 --skip="./.git,./node_modules"

# Type checking with mypy
runcmd mypy .

# Running tests with pytest
runcmd pytest

# Linting with ruff
runcmd ruff .

# Security check with safety
runcmd safety check

echo "[+] All checks passed!"

