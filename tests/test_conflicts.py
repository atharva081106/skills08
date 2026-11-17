"""
Tests for conflict detection engine and shadowing checks.
"""

import unittest
from pathlib import Path

from src.skills08.conflicts import ConflictDetector
from src.skills08.models import InstalledSkill
from src.skills08.constants import CROSS_REPO_COLLISIONS, AESTHETIC_OVERLAP_CLUSTER

class TestConflicts(unittest.TestCase):

    def setUp(self):
        self.detector = ConflictDetector()

    def test_cross_repo_collisions_coverage(self):
        """Verify that all 5 cross-repository collision names from D6 are detected."""
        for name in CROSS_REPO_COLLISIONS.keys():
            issue = self.detector.check_cross_repo_collision(name)
            self.assertIsNotNone(issue, f"Collision not detected for {name}")
            self.assertEqual(issue.conflict_id, "CON-011")
            self.assertEqual(issue.severity, "Medium")

    def test_benign_names_do_not_collide(self):
        """Verify that non-colliding names return None."""
        benign = ["humanizer", "security-audit", "code-simplification", "debugging-and-error-recovery"]
        for name in benign:
            issue = self.detector.check_cross_repo_collision(name)
            self.assertIsNone(issue)

    def test_scope_shadowing_detection(self):
        """Verify detection of dual-scope shadowing (CON-005)."""
        proj_skills = [
            InstalledSkill(name="humanizer", scope="project", path="/proj/humanizer", files_count=2),
            InstalledSkill(name="security-audit", scope="project", path="/proj/security-audit", files_count=18)
        ]
        glob_skills = [
            InstalledSkill(name="humanizer", scope="global", path="/glob/humanizer", files_count=2),
            InstalledSkill(name="archify", scope="global", path="/glob/archify", files_count=5)
        ]

        issues = self.detector.detect_scope_shadowing(proj_skills, glob_skills)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].conflict_id, "CON-005")
        self.assertIn("humanizer", issues[0].name)
        self.assertEqual(issues[0].affected_skills, ["humanizer"])

    def test_aesthetic_overlap_detection(self):
        """Verify advisory warning when multiple design skills are installed (CON-001)."""
        # Single aesthetic skill -> No conflict
        skills_single = [InstalledSkill(name="unslop", scope="project", path="/p/unslop", files_count=5)]
        self.assertIsNone(self.detector.detect_aesthetic_overlap(skills_single))

        # Multiple aesthetic skills -> CON-001 advisory
        skills_multi = [
            InstalledSkill(name="unslop", scope="project", path="/p/unslop", files_count=5),
            InstalledSkill(name="hallmark", scope="project", path="/p/hallmark", files_count=4),
            InstalledSkill(name="impeccable", scope="project", path="/p/impeccable", files_count=8)
        ]
        issue = self.detector.detect_aesthetic_overlap(skills_multi)
        self.assertIsNotNone(issue)
        self.assertEqual(issue.conflict_id, "CON-001")
        self.assertEqual(issue.severity, "Medium")
        self.assertIn("unslop", issue.affected_skills)
        self.assertIn("hallmark", issue.affected_skills)
        self.assertIn("impeccable", issue.affected_skills)

if __name__ == "__main__":
    unittest.main()

