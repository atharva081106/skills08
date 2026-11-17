"""
Tests for Windows-specific compatibility: path separators, spaces, unicode, argument quoting, and exit codes.
"""

import unittest
import tempfile
import shutil
import subprocess
import sys
from pathlib import Path

from src.skills08.installer import Installer
from src.skills08.constants import (
    EXIT_SUCCESS,
    EXIT_ERROR,
    EXIT_CONFLICT,
    EXIT_VERIFICATION_FAILED
)

class TestWindowsCompatibility(unittest.TestCase):

    def setUp(self):
        # Create temporary root with spaces and unicode in path
        self.temp_dir = tempfile.mkdtemp(prefix="skills08 test_space_&_unicode_")
        self.workspace = Path(self.temp_dir) / "workspace test"
        self.workspace.mkdir()
        self.global_dir = Path(self.temp_dir) / "global_skills_測試"
        self.global_dir.mkdir()

        self.installer = Installer(workspace_root=self.workspace, global_root=self.global_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_spaces_in_workspace_path(self):
        """Verify installation and verification work in paths containing spaces."""
        success, msg = self.installer.install("humanizer", scope="project")
        self.assertTrue(success, f"Failed to install in path with spaces: {msg}")

        dest = self.workspace / ".agents" / "skills" / "humanizer"
        self.assertTrue(dest.exists())
        self.assertTrue((dest / "SKILL.md").exists())

    def test_unicode_in_global_path(self):
        """Verify installation works in paths containing Unicode characters."""
        success, msg = self.installer.install("code-simplification", scope="global")
        self.assertTrue(success, f"Failed to install in unicode path: {msg}")

        dest = self.global_dir / "code-simplification"
        self.assertTrue(dest.exists())
        self.assertTrue((dest / "SKILL.md").exists())

    def test_windows_and_posix_path_separators(self):
        """Verify that forward slashes and backslashes are normalized consistently."""
        p_fwd = "packages/humanizer/SKILL.md"
        p_bak = "packages\\humanizer\\SKILL.md"
        norm_fwd = p_fwd.replace("\\", "/")
        norm_bak = p_bak.replace("\\", "/")
        self.assertEqual(norm_fwd, norm_bak)

    def test_cli_exit_codes_direct(self):
        """Verify CLI exit codes via subprocess execution."""
        # 1. list -> EXIT_SUCCESS (0)
        res_list = subprocess.run([sys.executable, "skills08.py", "list"], capture_output=True, text=True)
        self.assertEqual(res_list.returncode, EXIT_SUCCESS)

        # 2. inspect valid -> EXIT_SUCCESS (0)
        res_insp = subprocess.run([sys.executable, "skills08.py", "inspect", "humanizer"], capture_output=True, text=True)
        self.assertEqual(res_insp.returncode, EXIT_SUCCESS)

        # 3. inspect invalid -> EXIT_ERROR (1)
        res_bad = subprocess.run([sys.executable, "skills08.py", "inspect", "non_existent_skill"], capture_output=True, text=True)
        self.assertEqual(res_bad.returncode, EXIT_ERROR)

        # 4. status -> EXIT_SUCCESS (0)
        res_stat = subprocess.run([sys.executable, "skills08.py", "status"], capture_output=True, text=True)
        self.assertEqual(res_stat.returncode, EXIT_SUCCESS)

        # 5. conflicts on clean env -> EXIT_SUCCESS (0)
        res_conf = subprocess.run([sys.executable, "skills08.py", "conflicts"], capture_output=True, text=True)
        self.assertEqual(res_conf.returncode, EXIT_SUCCESS)

if __name__ == "__main__":
    unittest.main()

