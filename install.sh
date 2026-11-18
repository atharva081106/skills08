#!/usr/bin/env bash
# Skills08 One-Line Unix/macOS Installer
# Usage: curl -fsSL https://raw.githubusercontent.com/atharva081106/skills08/main/install.sh | bash

set -e

echo ""
echo "  ================================================================"
echo "     ⚡ Skills08 — The Package Manager for AI Agent Skills         "
echo "  ================================================================"
echo ""

if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo "Error: Python 3 (>= 3.8) is required, but was not found in PATH." >&2
    exit 1
fi

PY_VER=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "[OK] Detected Python $PY_VER ($($PYTHON_CMD -c 'import sys; print(sys.executable)'))"

echo "-> Installing Skills08 from GitHub..."
$PYTHON_CMD -m pip install --upgrade --quiet "git+https://github.com/atharva081106/skills08.git"

echo "[OK] Skills08 installed successfully!"
echo ""
echo "Quick commands to get started:"
echo "  skills08 doctor                     # Verify your environment"
echo "  skills08 list                       # Browse 12 production skills"
echo "  skills08 install security-audit -s  # Install & sync across Cursor, Claude, Antigravity"
echo ""

