"""
Tests for manifest loading, candidate metadata, and provenance traceability.
"""

import unittest
from pathlib import Path

from src.skills08.manifest import ManifestLoader
from src.skills08.constants import (
    MODEL_A_INSTRUCTION_ONLY,
    MODEL_NATIVE,
    MODEL_COMPANION,
    MODEL_SUBAGENT,
    MODEL_DEFERRED,
    TIER_1_STANDARD,
    TIER_2_CONDITIONAL,
    TIER_3_RESTRICTED,
    TIER_4_DEFERRED
)

class TestManifest(unittest.TestCase):

    def setUp(self):
        self.loader = ManifestLoader()
        self.candidates = self.loader.load()

    def test_candidate_count(self):
        """Verify exactly 13 candidates are loaded from manifest.yaml."""
        self.assertEqual(len(self.candidates), 13)

    def test_group_breakdown(self):
        """Verify 12 Group A and 1 Group B candidates."""
        group_a = [c for c in self.candidates if "Group A" in c.tier]
        group_b = [c for c in self.candidates if "Group B" in c.tier]
        self.assertEqual(len(group_a), 12)
        self.assertEqual(len(group_b), 1)
        self.assertEqual(group_b[0].id, "SKILL08-UI-004")
        self.assertEqual(group_b[0].name, "open-pencil")

    def test_provenance_integrity(self):
        """Verify all candidates have valid upstream provenance and locked commit SHAs."""
        for c in self.candidates:
            self.assertTrue(c.id.startswith("SKILL08-"))
            self.assertTrue(len(c.name) > 0)
            self.assertTrue(c.provenance.repository_url.startswith("https://github.com/"))
            self.assertEqual(len(c.provenance.commit_sha), 40, f"Candidate {c.id} commit SHA length != 40")
            self.assertTrue(len(c.provenance.author) > 0)
            self.assertIn(c.provenance.declared_license, ["MIT", "Apache-2.0", "CC-BY-4.0"])

    def test_legal_clearance_mapping(self):
        """Verify legal clearances align with Deliverable 3."""
        tier1_ids = {
            "SKILL08-SEC-001", "SKILL08-DOC-001", "SKILL08-UI-002",
            "SKILL08-FE-001", "SKILL08-SWE-001", "SKILL08-TST-001",
            "SKILL08-SWE-003", "SKILL08-FE-002"
        }
        tier2_ids = {"SKILL08-SWE-002", "SKILL08-UI-001"}
        tier3_ids = {"SKILL08-ARC-001", "SKILL08-UI-003"}
        tier4_ids = {"SKILL08-UI-004"}

        for c in self.candidates:
            if c.id in tier1_ids:
                self.assertEqual(c.license_clearance, TIER_1_STANDARD)
            elif c.id in tier2_ids:
                self.assertEqual(c.license_clearance, TIER_2_CONDITIONAL)
            elif c.id in tier3_ids:
                self.assertEqual(c.license_clearance, TIER_3_RESTRICTED)
            elif c.id in tier4_ids:
                self.assertEqual(c.license_clearance, TIER_4_DEFERRED)

    def test_operational_model_mapping(self):
        """Verify operational models match Deliverable 4 and 7."""
        native_ids = {"SKILL08-DOC-001", "SKILL08-SWE-001", "SKILL08-SWE-002", "SKILL08-SWE-003"}
        model_a_ids = {"SKILL08-ARC-001", "SKILL08-FE-001", "SKILL08-FE-002", "SKILL08-UI-001", "SKILL08-UI-002", "SKILL08-UI-003"}

        for c in self.candidates:
            if c.id in native_ids:
                self.assertEqual(c.operational_model, MODEL_NATIVE)
            elif c.id in model_a_ids:
                self.assertEqual(c.operational_model, MODEL_A_INSTRUCTION_ONLY)
            elif c.id == "SKILL08-SEC-001":
                self.assertEqual(c.operational_model, MODEL_COMPANION)
            elif c.id == "SKILL08-TST-001":
                self.assertEqual(c.operational_model, MODEL_SUBAGENT)
            elif c.id == "SKILL08-UI-004":
                self.assertEqual(c.operational_model, MODEL_DEFERRED)

if __name__ == "__main__":
    unittest.main()

