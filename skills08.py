#!/usr/bin/env python3
"""
Skills08 Portable Root Entrypoint
"""

import sys
from pathlib import Path

# Add src to sys.path and remove root directory to prevent self-import shadowing
root_dir = Path(__file__).resolve().parent
src_dir = root_dir / "src"

root_str = str(root_dir)
for p in list(sys.path):
    if p in [root_str, "", "."]:
        sys.path.remove(p)

if "skills08" in sys.modules and sys.modules["skills08"].__file__ == __file__:
    del sys.modules["skills08"]

if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from skills08.cli import main

if __name__ == "__main__":
    sys.exit(main())

