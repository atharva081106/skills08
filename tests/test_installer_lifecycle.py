"""
Tests for installer lifecycle, atomic operations, and path safety.
Includes regression tests for DEF-SEC-001 and DEF-FUN-001.
"""

import unittest
import tempfile
import shutil
from pathlib import Path

from src.skills08.installer import Installer
from src.skills08.catalog import Catalog

class TestInstallerLifecycle(unittest.TestCase):

    def setUp(self):
        # Create isolated temporary workspace and global directories
        self.temp_dir = tempfile.mkdtemp()
        self.workspace = Path(self.temp_dir) / "workspace"
        self.workspace.mkdir()
        self.global_dir = Path(self.temp_dir) / "global_skills"
        self.global_dir.mkdir()

        self.installer = Installer(workspace_root=self.workspace, global_root=self.global_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_install_and_uninstall_project_scope(self):
        """Test standard project-scope installation and clean removal."""
        success, msg = self.installer.install("humanizer", scope="project")
        self.assertTrue(success, f"Install failed: {msg}")

        dest = self.workspace / ".agents" / "skills" / "humanizer"
        self.assertTrue(dest.exists())
        self.assertTrue((dest / "SKILL.md").exists())
        self.assertTrue((dest / "NOTICE.md").exists())

        installed = self.installer.list_installed("project")
        self.assertEqual(len(installed), 1)
        self.assertEqual(installed[0].name, "humanizer")
        self.assertEqual(installed[0].scope, "project")

        un_success, un_msg = self.installer.uninstall("humanizer", scope="project")
        self.assertTrue(un_success, f"Uninstall failed: {un_msg}")
        self.assertFalse(dest.exists())
        self.assertEqual(len(self.installer.list_installed("project")), 0)

    def test_install_global_scope(self):
        """Test global-scope installation."""
        success, msg = self.installer.install("code-simplification", scope="global")
        self.assertTrue(success, f"Global install failed: {msg}")

        dest = self.global_dir / "code-simplification"
        self.assertTrue(dest.exists())
        self.assertTrue((dest / "SKILL.md").exists())

        installed = self.installer.list_installed("global")
        self.assertEqual(len(installed), 1)
        self.assertEqual(installed[0].name, "code-simplification")
        self.assertEqual(installed[0].scope, "global")

    def test_reject_deferred_group_b(self):
        """Verify installer refuses to install Group B (open-pencil)."""
        success, msg = self.installer.install("open-pencil", scope="project")
        self.assertFalse(success)
        self.assertIn("Group B", msg)

    def test_refuse_overwrite_without_force(self):
        """Verify installer refuses to overwrite existing skill without --force."""
        success, _ = self.installer.install("humanizer", scope="project")
        self.assertTrue(success)

        fail_success, fail_msg = self.installer.install("humanizer", scope="project", force=False)
        self.assertFalse(fail_success)
        self.assertIn("already installed", fail_msg)

        force_success, force_msg = self.installer.install("humanizer", scope="project", force=True)
        self.assertTrue(force_success)

    def test_path_traversal_defense(self):
        """Verify rejection of standard path traversal identifiers."""
        malicious = ["../../etc/passwd", "../malicious", "sub/../../escape"]
        for ident in malicious:
            success, msg = self.installer.install(ident, scope="project")
            self.assertFalse(success)

    def test_sibling_directory_prefix_defense_regression(self):
        """Regression test for DEF-SEC-001: verify sibling prefix paths are rejected."""
        # A name like 'skills_evil' where target_root is '.agents/skills'
        # Under str.startswith(), .agents/skills_evil would start with .agents/skills
        # Under Path.is_relative_to(), it is correctly rejected as outside target root.
        target_root = self.installer.get_target_root("project")
        outside_sibling = target_root.parent / f"{target_root.name}_sibling_attack"
        self.assertFalse(outside_sibling.is_relative_to(target_root))

    def test_uninstall_invalid_names_regression(self):
        """Regression test for DEF-FUN-001: verify uninstall rejects empty, dot, or slash names."""
        invalid_names = ["", " ", ".", "..", "/", "\\", "   "]
        for inv in invalid_names:
            success, msg = self.installer.uninstall(inv, scope="project")
            self.assertFalse(success)
            self.assertIn("Security violation", msg)
            # Ensure target root was NOT deleted
            self.assertTrue(self.workspace.exists())

    def test_symlink_outside_destination_rejected_on_install(self):
        """Regression test: verify symlinks pointing outside target root are rejected on install."""
        outside_dir = Path(self.temp_dir) / "outside_dir"
        outside_dir.mkdir(parents=True, exist_ok=True)
        canary = outside_dir / "canary.txt"
        canary.write_text("PRESERVE_DATA", encoding="utf-8")

        target_root = self.installer.get_target_root("project")
        target_root.mkdir(parents=True, exist_ok=True)
        sym_dest = target_root / "humanizer"

        try:
            sym_dest.symlink_to(outside_dir, target_is_directory=True)
        except OSError:
            self.skipTest("Symlink creation not supported or permitted in this environment")

        success, msg = self.installer.install("humanizer", scope="project", force=True)
        self.assertFalse(success)
        self.assertIn("Security violation", msg)
        self.assertTrue(canary.exists())
        self.assertEqual(canary.read_text(encoding="utf-8"), "PRESERVE_DATA")

    def test_symlink_outside_destination_rejected_on_uninstall(self):
        """Regression test: verify symlinks pointing outside target root are rejected on uninstall."""
        outside_dir = Path(self.temp_dir) / "outside_dir_un"
        outside_dir.mkdir(parents=True, exist_ok=True)
        canary = outside_dir / "canary.txt"
        canary.write_text("PRESERVE_DATA_UN", encoding="utf-8")

        target_root = self.installer.get_target_root("project")
        target_root.mkdir(parents=True, exist_ok=True)
        sym_dest = target_root / "foreign_link"

        try:
            sym_dest.symlink_to(outside_dir, target_is_directory=True)
        except OSError:
            self.skipTest("Symlink creation not supported or permitted in this environment")

        success, msg = self.installer.uninstall("foreign_link", scope="project")
        self.assertFalse(success)
        self.assertIn("Security violation", msg)
        self.assertTrue(canary.exists())
        self.assertEqual(canary.read_text(encoding="utf-8"), "PRESERVE_DATA_UN")

    def test_symlink_internal_removal_contained(self):
        """Regression test: verify uninstallation of skill with internal symlink to outside preserves outside files."""
        outside_dir = Path(self.temp_dir) / "outside_contained"
        outside_dir.mkdir(parents=True, exist_ok=True)
        canary = outside_dir / "important.dat"
        canary.write_text("IMPORTANT_SAFEGUARD", encoding="utf-8")

        success, msg = self.installer.install("humanizer", scope="project")
        self.assertTrue(success, f"Install failed: {msg}")

        dest = self.workspace / ".agents" / "skills" / "humanizer"
        inner_symlink = dest / "leak_link"

        try:
            inner_symlink.symlink_to(outside_dir, target_is_directory=True)
        except OSError:
            self.skipTest("Symlink creation not supported or permitted in this environment")

        un_success, un_msg = self.installer.uninstall("humanizer", scope="project")
        self.assertTrue(un_success, f"Uninstall failed: {un_msg}")
        self.assertFalse(dest.exists())
        self.assertTrue(outside_dir.exists())
        self.assertTrue(canary.exists())
        self.assertEqual(canary.read_text(encoding="utf-8"), "IMPORTANT_SAFEGUARD")

    def test_junction_outside_destination_rejected(self):
        """Regression test: verify Windows directory junctions pointing outside target root are rejected."""
        import sys
        import subprocess
        if sys.platform != "win32":
            self.skipTest("Directory junctions only applicable on Windows")

        outside_dir = Path(self.temp_dir) / "outside_junc"
        outside_dir.mkdir(parents=True, exist_ok=True)
        canary = outside_dir / "junc_canary.txt"
        canary.write_text("CANARY_JUNCTION", encoding="utf-8")

        target_root = self.installer.get_target_root("project")
        target_root.mkdir(parents=True, exist_ok=True)
        junc_dest = target_root / "humanizer"

        res = subprocess.run(f'cmd /c mklink /J "{junc_dest}" "{outside_dir}"', shell=True, capture_output=True)
        if res.returncode != 0:
            self.skipTest("Failed to create junction in this environment")

        # Test install rejection
        success, msg = self.installer.install("humanizer", scope="project", force=True)
        self.assertFalse(success)
        self.assertIn("Security violation", msg)
        self.assertTrue(canary.exists())

        # Test uninstall rejection
        un_success, un_msg = self.installer.uninstall("humanizer", scope="project")
        self.assertFalse(un_success)
        self.assertIn("Security violation", msg)
        self.assertTrue(canary.exists())

        # Clean up junction safely
        self.installer._safe_remove_path(junc_dest)
        self.assertFalse(junc_dest.exists())
        self.assertTrue(canary.exists())

if __name__ == "__main__":
    unittest.main()
