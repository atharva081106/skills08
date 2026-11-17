"""
Tests for full-fledged Skills08 features:
- CLI workspace-root and global-root redirection (FND-001)
- Scope filtering on status and conflicts (FND-003)
- Catalog search by keyword, category, and tier
- Skill scaffolding (new / init-skill)
- Skill packaging and checksum calculation (pack)
- Environment diagnostics (doctor)
- Agent workspace initialization (agent-init)
- Update and re-installation lifecycle
"""

import unittest
import tempfile
import shutil
import json
import subprocess
import sys
from pathlib import Path

from src.skills08.catalog import Catalog
from src.skills08.installer import Installer
from src.skills08.scaffold import SkillScaffolder
from src.skills08.packager import SkillPackager
from src.skills08.doctor import EnvironmentDoctor
from src.skills08.agent_config import AgentConfigManager
from src.skills08.constants import (
    EXIT_SUCCESS,
    EXIT_ERROR,
    EXIT_CONFLICT,
    EXIT_VERIFICATION_FAILED
)

class TestFullFledgedFeatures(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="skills08_full_test_")
        self.workspace = Path(self.temp_dir) / "workspace"
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.global_dir = Path(self.temp_dir) / "global_skills"
        self.global_dir.mkdir(parents=True, exist_ok=True)

        self.installer = Installer(
            workspace_root=self.workspace,
            global_root=self.global_dir
        )

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_cli_workspace_root_flag(self):
        """Verify -w / --workspace-root redirects installation to target workspace (FND-001)."""
        target_ws = Path(self.temp_dir) / "custom_target_ws"
        target_ws.mkdir(parents=True, exist_ok=True)

        res = subprocess.run(
            [sys.executable, "skills08.py", "-w", str(target_ws), "install", "humanizer"],
            capture_output=True,
            text=True
        )
        self.assertEqual(res.returncode, EXIT_SUCCESS, f"Install failed: {res.stderr}")

        installed_skill = target_ws / ".agents" / "skills" / "humanizer" / "SKILL.md"
        self.assertTrue(installed_skill.exists(), "Skill was not installed into specified -w workspace root.")

    def test_cli_global_root_flag(self):
        """Verify -g / --global-root redirects global installation cleanly (FND-001 / Workflow E)."""
        target_gl = Path(self.temp_dir) / "custom_global_root"
        target_gl.mkdir(parents=True, exist_ok=True)

        res = subprocess.run(
            [sys.executable, "skills08.py", "-g", str(target_gl), "install", "code-simplification", "--scope", "global"],
            capture_output=True,
            text=True
        )
        self.assertEqual(res.returncode, EXIT_SUCCESS, f"Global install failed: {res.stderr}")

        installed_skill = target_gl / "code-simplification" / "SKILL.md"
        self.assertTrue(installed_skill.exists(), "Skill was not installed into specified -g global root.")

    def test_catalog_search(self):
        """Verify search finds matching skills across keywords, categories, and tiers."""
        catalog = self.installer.catalog

        # 1. Search by name substring
        res_hum = catalog.search("human")
        self.assertTrue(any(c.name == "humanizer" for c in res_hum))

        # 2. Search by description keyword
        res_sec = catalog.search("vulnerability")
        self.assertTrue(any(c.name == "security-audit" for c in res_sec))

        # 3. Search with category filter
        res_fe = catalog.search("", category="Frontend")
        self.assertTrue(len(res_fe) >= 1)
        self.assertTrue(all("Frontend" in c.category for c in res_fe))

        # 4. Search with tier filter
        res_ga = catalog.search("", tier="Group A")
        self.assertEqual(len(res_ga), 12)

    def test_status_scope_filter(self):
        """Verify status --scope filters results strictly to specified scope (FND-003)."""
        # Install into project scope
        self.installer.install("humanizer", scope="project")
        # Install into global scope
        self.installer.install("code-simplification", scope="global")

        proj_only = self.installer.list_installed(scope="project")
        self.assertEqual(len(proj_only), 1)
        self.assertEqual(proj_only[0].name, "humanizer")

        glob_only = self.installer.list_installed(scope="global")
        self.assertEqual(len(glob_only), 1)
        self.assertEqual(glob_only[0].name, "code-simplification")

        both = self.installer.list_installed()
        self.assertEqual(len(both), 2)

    def test_update_installed_skills(self):
        """Verify update re-installs and updates existing skills safely."""
        # Install initial skill
        self.installer.install("humanizer", scope="project")

        # Mutate a file to simulate local drift
        skill_file = self.workspace / ".agents" / "skills" / "humanizer" / "SKILL.md"
        skill_file.write_text("Modified locally", encoding="utf-8")

        # Run update
        success, msg, count = self.installer.update("humanizer", scope="project")
        self.assertTrue(success, f"Update failed: {msg}")
        self.assertEqual(count, 1)

        # Content should be restored to catalog version
        restored = skill_file.read_text(encoding="utf-8")
        self.assertIn("Humanizer", restored)

    def test_scaffolding_validation_and_creation(self):
        """Verify skill scaffolding validates names and produces standard Antigravity structure."""
        # 1. Invalid names rejected
        invalid_names = ["Invalid_Name", "name with spaces", "UPPERCASE", "a", "-leading", "trailing-"]
        for bad_name in invalid_names:
            valid, err = SkillScaffolder.validate_name(bad_name)
            self.assertFalse(valid, f"Expected '{bad_name}' to be rejected")

        # 2. Valid name accepted
        valid, _ = SkillScaffolder.validate_name("react-state-helper")
        self.assertTrue(valid)

        # 3. Create scaffold
        dest = Path(self.temp_dir) / "scaffold_test"
        success, msg, created = SkillScaffolder.scaffold(
            name="react-state-helper",
            destination_dir=dest,
            description="Assists with React state management",
            author="Test Author"
        )
        self.assertTrue(success)
        self.assertTrue((created / "SKILL.md").exists())
        self.assertTrue((created / "examples" / "sample.md").exists())
        self.assertTrue((created / "references" / "spec.md").exists())

        # Verify frontmatter
        content = (created / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\nname: react-state-helper\n"))

    def test_packager_validation_and_packaging(self):
        """Verify packager creates valid .tar.gz bundle with checksum."""
        # Create a sample skill to pack
        skill_dir = Path(self.temp_dir) / "my-test-skill"
        SkillScaffolder.scaffold("my-test-skill", Path(self.temp_dir))

        # Validate directory
        is_valid, issues = SkillPackager.validate_skill_dir(skill_dir)
        self.assertTrue(is_valid, f"Validation issues: {issues}")

        # Pack into archive
        out_dir = Path(self.temp_dir) / "dist"
        success, msg, meta = SkillPackager.pack(skill_dir, output_dir=out_dir)
        self.assertTrue(success, f"Pack failed: {msg}")

        archive_path = Path(meta["archive_path"])
        self.assertTrue(archive_path.exists())
        self.assertGreater(meta["archive_size_bytes"], 0)
        self.assertEqual(len(meta["archive_sha256"]), 64)
        self.assertIn("SKILL.md", meta["files"])

    def test_doctor_diagnostics(self):
        """Verify EnvironmentDoctor returns valid diagnostic items."""
        doctor = EnvironmentDoctor(
            workspace_root=self.workspace,
            global_root=self.global_dir
        )
        checks = doctor.run_all_checks()
        self.assertGreater(len(checks), 5)

        categories = {c.category for c in checks}
        self.assertIn("Runtime", categories)
        self.assertIn("Platform", categories)
        self.assertIn("Workspace", categories)
        self.assertIn("Catalog", categories)

        statuses = {c.status for c in checks}
        self.assertNotIn("FAIL", statuses, "Doctor reported unexpected FAIL in test environment.")

    def test_agent_init_workspace(self):
        """Verify agent-init configures workspace for Antigravity and coding agents."""
        target_ws = Path(self.temp_dir) / "agent_ws_test"
        target_ws.mkdir(parents=True, exist_ok=True)

        success, msg, data = AgentConfigManager.init_workspace(target_ws)
        self.assertTrue(success)

        agents_dir = target_ws / ".agents"
        self.assertTrue(agents_dir.exists())
        self.assertTrue((agents_dir / "skills").exists())
        self.assertTrue((agents_dir / "skills.json").exists())
        self.assertTrue((agents_dir / ".gitignore").exists())
        self.assertTrue((agents_dir / "README.md").exists())

        config = json.loads((agents_dir / "skills.json").read_text(encoding="utf-8"))
        self.assertIn("Google Antigravity", config["supported_agents"])

    def test_cli_json_output_mode(self):
        """Verify CLI commands support --json cleanly for machine integration."""
        res = subprocess.run(
            [sys.executable, "skills08.py", "list", "--json"],
            capture_output=True,
            text=True
        )
        self.assertEqual(res.returncode, EXIT_SUCCESS)
        data = json.loads(res.stdout)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 13)

    def test_multi_agent_sync_projection(self):
        """Verify sync projects skills to Cursor, Claude, Copilot, Windsurf, Cline, and Gemini."""
        self.installer.install("humanizer", scope="project")
        success, msg, data = AgentConfigManager.sync_all_agents(self.workspace)
        self.assertTrue(success, f"Sync failed: {msg}")

        # 1. Cursor .mdc rule
        cursor_mdc = self.workspace / ".cursor" / "rules" / "humanizer.mdc"
        self.assertTrue(cursor_mdc.exists())
        self.assertIn("description:", cursor_mdc.read_text(encoding="utf-8"))

        # 2. Claude Code mirror & CLAUDE.md
        claude_skill = self.workspace / ".claude" / "skills" / "humanizer" / "SKILL.md"
        self.assertTrue(claude_skill.exists())
        claude_md = self.workspace / "CLAUDE.md"
        self.assertTrue(claude_md.exists())
        self.assertIn("BEGIN SKILLS08 MANAGED BLOCK", claude_md.read_text(encoding="utf-8"))

        # 3. GitHub Copilot
        copilot_file = self.workspace / ".github" / "copilot-instructions.md"
        self.assertTrue(copilot_file.exists())
        self.assertIn("BEGIN SKILLS08 MANAGED BLOCK", copilot_file.read_text(encoding="utf-8"))

        # 4. Windsurf
        windsurf_file = self.workspace / ".windsurfrules"
        self.assertTrue(windsurf_file.exists())

        # 5. Cline / Roo Code
        cline_file = self.workspace / ".clinerules"
        self.assertTrue(cline_file.exists())

        # 6. Gemini & Universal AGENTS.md
        self.assertTrue((self.workspace / "GEMINI.md").exists())
        self.assertTrue((self.workspace / "AGENTS.md").exists())

    def test_multi_agent_sync_preserves_user_rules(self):
        """Verify sync updates only managed block and preserves custom user instructions."""
        claude_md = self.workspace / "CLAUDE.md"
        claude_md.write_text("# Custom Developer Rule\n- Do not break the build\n", encoding="utf-8")

        self.installer.install("humanizer", scope="project")
        AgentConfigManager.sync_all_agents(self.workspace)

        content = claude_md.read_text(encoding="utf-8")
        self.assertIn("# Custom Developer Rule", content)
        self.assertIn("- Do not break the build", content)
        self.assertIn("BEGIN SKILLS08 MANAGED BLOCK", content)

    def test_cli_sync_command(self):
        """Verify CLI sync command updates workspace projections via subprocess."""
        self.installer.install("code-simplification", scope="project")

        res = subprocess.run(
            [sys.executable, "skills08.py", "-w", str(self.workspace), "sync", "--json"],
            capture_output=True,
            text=True
        )
        self.assertEqual(res.returncode, EXIT_SUCCESS, f"CLI sync failed: {res.stderr}")
        data = json.loads(res.stdout)
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["installed_skills_count"], 1)
        self.assertEqual(data["data"]["synced_counts"]["cursor"], 1)

if __name__ == "__main__":
    unittest.main()

