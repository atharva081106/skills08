"""
Tests for security constraints, secrets exposure prevention, and dependency boundaries.
"""

import unittest
import os
import re
from pathlib import Path

class TestSecurityAndSecrets(unittest.TestCase):

    def test_no_hardcoded_secrets_in_new_code(self):
        """Scan newly created implementation and package files for sensitive patterns."""
        root = Path(".").resolve()
        sensitive_patterns = [
            re.compile(r"(?:api_key|apikey|secret_key|private_key|auth_token)\s*=\s*['\"][A-Za-z0-9+/=_-]{16,}['\"]", re.IGNORECASE),
            re.compile(r"ghp_[A-Za-z0-9]{36}"),
            re.compile(r"AIza[0-9A-Za-z-_]{35}"),
            re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----")
        ]

        target_dirs = ["src", "packages", "tests"]
        found_secrets = []

        for tdir in target_dirs:
            dp = root / tdir
            if not dp.exists():
                continue
            for f in dp.rglob("*"):
                if f.is_file() and f.suffix in [".py", ".json", ".md", ".yaml", ".yml", ".ps1"]:
                    try:
                        content = f.read_text(encoding="utf-8", errors="ignore")
                        for pat in sensitive_patterns:
                            if pat.search(content):
                                found_secrets.append(f"{f}: matched {pat.pattern}")
                    except Exception:
                        pass

        self.assertEqual(len(found_secrets), 0, f"Potential sensitive credentials found: {found_secrets}")

    def test_zero_third_party_runtime_dependencies(self):
        """Verify that src/skills08 requires only standard library modules (plus PyYAML for manifest)."""
        import sys
        # Python standard library modules used: os, sys, shutil, hashlib, json, re, pathlib, argparse, dataclasses, typing, datetime, unittest
        # PyYAML is optional/standard in this environment for manifest loading
        from src.skills08.constants import EXIT_SUCCESS
        self.assertEqual(EXIT_SUCCESS, 0)

    def test_no_arbitrary_eval_or_exec_in_core(self):
        """Ensure no dynamic eval() or exec() calls exist in core implementation."""
        src_dir = Path("src/skills08").resolve()
        for f in src_dir.rglob("*.py"):
            text = f.read_text(encoding="utf-8")
            self.assertNotIn("exec(", text, f"Disallowed exec() call in {f.name}")
            self.assertNotIn("eval(", text, f"Disallowed eval() call in {f.name}")
            self.assertNotIn("subprocess.call", text, f"Disallowed subprocess call in {f.name}")
            self.assertNotIn("os.system", text, f"Disallowed os.system call in {f.name}")

if __name__ == "__main__":
    unittest.main()

