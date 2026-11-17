"""
Tests for cryptographic integrity verifier.
"""

import unittest
import tempfile
import shutil
from pathlib import Path

from src.skills08.installer import Installer
from src.skills08.verifier import IntegrityVerifier

class TestVerifierIntegrity(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.workspace = Path(self.temp_dir) / "workspace"
        self.workspace.mkdir()
        self.global_dir = Path(self.temp_dir) / "global_skills"
        self.global_dir.mkdir()

        self.installer = Installer(workspace_root=self.workspace, global_root=self.global_dir)
        self.verifier = IntegrityVerifier(self.installer)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_verify_clean_install(self):
        """Verify that a freshly installed skill matches curated hashes 100%."""
        success, _ = self.installer.install("humanizer", scope="project")
        self.assertTrue(success)

        items = self.verifier.verify_skill("humanizer", scope="project")
        self.assertTrue(len(items) > 0)
        for it in items:
            self.assertEqual(it.status, "MATCH")

    def test_detect_modified_file(self):
        """Verify that modifying file content triggers MODIFIED status."""
        self.installer.install("humanizer", scope="project")
        skill_file = self.workspace / ".agents" / "skills" / "humanizer" / "SKILL.md"

        # Tamper with file
        skill_file.write_text("TAMPERED CONTENT", encoding="utf-8")

        items = self.verifier.verify_skill("humanizer", scope="project")
        modified_items = [it for it in items if it.status == "MODIFIED"]
        self.assertEqual(len(modified_items), 1)
        self.assertEqual(modified_items[0].relative_path, "SKILL.md")

    def test_detect_missing_file(self):
        """Verify that deleting a required file triggers MISSING status."""
        self.installer.install("security-audit", scope="project")
        target_file = self.workspace / ".agents" / "skills" / "security-audit" / "ATTACK-CLASSES.md"
        target_file.unlink()

        items = self.verifier.verify_skill("security-audit", scope="project")
        missing_items = [it for it in items if it.status == "MISSING"]
        self.assertEqual(len(missing_items), 1)
        self.assertEqual(missing_items[0].relative_path, "ATTACK-CLASSES.md")

    def test_detect_extra_file(self):
        """Verify that adding an unexpected file triggers EXTRA status."""
        self.installer.install("humanizer", scope="project")
        extra_file = self.workspace / ".agents" / "skills" / "humanizer" / "unauthorized_script.py"
        extra_file.write_text("print('rogue')", encoding="utf-8")

        items = self.verifier.verify_skill("humanizer", scope="project")
        extra_items = [it for it in items if it.status == "EXTRA"]
        self.assertEqual(len(extra_items), 1)
        self.assertEqual(extra_items[0].relative_path, "unauthorized_script.py")

if __name__ == "__main__":
    unittest.main()

