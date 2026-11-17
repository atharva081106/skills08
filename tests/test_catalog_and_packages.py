"""
Tests for package catalog, asset completeness, and Model A adaptation.
"""

import unittest
from pathlib import Path

from src.skills08.catalog import Catalog

class TestCatalogAndPackages(unittest.TestCase):

    def setUp(self):
        self.catalog = Catalog()

    def test_all_group_a_have_packages(self):
        """Verify that all 12 Group A candidates have curated packages in packages/."""
        group_a = self.catalog.get_group_a()
        self.assertEqual(len(group_a), 12)

        for cand in group_a:
            self.assertTrue(
                self.catalog.has_package(cand.name),
                f"Curated package missing for Group A candidate {cand.name} ({cand.id})"
            )
            pkg_path = self.catalog.get_package_path(cand.name)
            self.assertIsNotNone(pkg_path)
            self.assertTrue((pkg_path / "SKILL.md").exists())
            self.assertTrue((pkg_path / "NOTICE.md").exists())

    def test_group_b_has_no_active_package(self):
        """Verify that Group B (open-pencil) is deferred and has no active package."""
        group_b = self.catalog.get_group_b()
        self.assertEqual(len(group_b), 1)
        self.assertEqual(group_b[0].name, "open-pencil")
        self.assertFalse(self.catalog.has_package("open-pencil"))

    def test_model_a_script_omissions(self):
        """Verify that script-bearing skills omit dangerous scripts under Model A."""
        # archify should not have bin/archify.mjs
        archify_pkg = self.catalog.get_package_path("archify")
        self.assertFalse((archify_pkg / "bin").exists())

        # scroll-craft should not have scripts/kie.mjs
        scroll_pkg = self.catalog.get_package_path("scroll-craft")
        self.assertFalse((scroll_pkg / "scripts").exists())

        # unslop should not have scripts/snapshot.mjs
        unslop_pkg = self.catalog.get_package_path("unslop")
        self.assertFalse((unslop_pkg / "scripts").exists())

        # hallmark should not have scripts/sloplint.mjs
        hallmark_pkg = self.catalog.get_package_path("hallmark")
        self.assertFalse((hallmark_pkg / "scripts").exists())

        # design-taste-frontend should not have scripts/gate.mjs
        taste_pkg = self.catalog.get_package_path("design-taste-frontend")
        self.assertFalse((taste_pkg / "scripts").exists())

        # impeccable should not have scripts/impeccable or assets/fonts
        imp_pkg = self.catalog.get_package_path("impeccable")
        self.assertFalse((imp_pkg / "scripts").exists())
        self.assertFalse((imp_pkg / "assets").exists())

    def test_companion_assets_preserved(self):
        """Verify that essential markdown references and playbooks are preserved."""
        # security-audit must have companion playbooks
        sec_pkg = self.catalog.get_package_path("security-audit")
        self.assertTrue((sec_pkg / "ATTACK-CLASSES.md").exists())
        self.assertTrue((sec_pkg / "report-schema.json").exists())

        # simplify-codebase must have dedicated LICENSE file
        scb_pkg = self.catalog.get_package_path("simplify-codebase")
        self.assertTrue((scb_pkg / "LICENSE").exists())

        # unslop must have references
        unslop_pkg = self.catalog.get_package_path("unslop")
        self.assertTrue((unslop_pkg / "references").exists())

        # impeccable must have reference playbooks
        imp_pkg = self.catalog.get_package_path("impeccable")
        self.assertTrue((imp_pkg / "reference").exists())

if __name__ == "__main__":
    unittest.main()

