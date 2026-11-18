"""
Tests to cryptographically verify that all protected baselines remain bit-for-bit identical.
"""

import unittest
import hashlib
from pathlib import Path

class TestProtectedBaselines(unittest.TestCase):

    AUTHORITATIVE_BASELINES = {
        "docs/research/SOURCE_INVENTORY.md": {
            "size": 43135,
            "sha256": "35e44916130808628231576c62d61fbb107feefd53bf3eef0fa8d551590e094e"
        },
        "docs/research/SKILLS_EXTRACTION.md": {
            "size": 53934,
            "sha256": "313492848a0f284ef20adfc9ccee48ee313b0d5a8d3f943b590b5d43c89ec3da"
        },
        "docs/research/LICENSE_MATRIX.md": {
            "size": 68780,
            "sha256": "893685d83f2f8c371ce480248a7aeea2a424cd9dbdb1dc6d48a3750dfd9eed0b"
        },
        "docs/research/COMPATIBILITY_MATRIX.md": {
            "size": 54963,
            "sha256": "88123497c2793adaa8415026e3d7c0a1841d4b4a94cd8e392b2d785d3d8fa9ef"
        },
        "docs/research/SECURITY_AUDIT.md": {
            "size": 188774,
            "sha256": "6f003f9d87f6ea3e8c91df12c97fea80790fc50b12c28b1ad447027373270bfe"
        },
        "docs/research/SECURITY_AUDIT_CORRECTION_REPORT.md": {
            "size": 19014,
            "sha256": "1ee7d5f16c39e369d0d781ac0a3d627f3d18119771e341d05c982c857aa4742e"
        },
        "manifests/manifest.yaml": {
            "size": 21192,
            "sha256": "bec876bbe54ee20ba155b0252eeec54694bb9ebb8870b389c2cea6db00073d59"
        },
        "research/final_reconciled_ledger.json": {
            "size": 1565430,
            "sha256": "c85e759e5b947ea07f0908708a1b6473e8e133a891cf8d2bb3bc90493d9b41ec"
        },
        "docs/research/CONFLICT_ANALYSIS.md": {
            "size": 137798,
            "sha256": "88931095b80378451dd76b015098bb64e5089327923c32f38f6b26d4560b5ad2"
        },
        "docs/research/D6_FINAL_VERIFICATION_REPORT.md": {
            "size": 19052,
            "sha256": "69137f71c6c04e091ddb9b528aabc355eabda4b792d9723cf0eed60ca14f0a4a"
        }
    }

    AUTHORITATIVE_REPO_SHAS = {
        "Soup": "deb9f0af0a4bbb5da11b30293a2efdcf82611df1",
        "agent-skills": "39b723ceebf81474d0557c1fecd01eddab585563",
        "antigravity-skills": "2ee2cf79b99035fbdabdfe0b1057034195e7571e",
        "archify": "a7ed6fd6657da90414831d1d42cf95987188750c",
        "awesome-design-md": "fcc70284932276d085f01ef9f83edde90b1258cb",
        "awesome-playwright": "3ef7191de074e66df322348337cf3ba9a0f83c5e",
        "ecc": "d2ef2680594f9a17526a6e1a2e18b3d242c5d17b",
        "free-for-dev": "a6d2501c4d2566a3f518f08e51a23923edf65734",
        "hallmark": "04977e15f3dfd6ee4b74c887dac3eb52665d6c92",
        "humanizer": "b48c832f0f809c1b5658edbb838c2521b72f2413",
        "hyperframes": "ead110aab9e4b43befdbe21001deac168c09e04b",
        "impeccable": "d41d9860b0094dcb68030657da63461212835aaa",
        "open-design": "84dd08b5709bfa4bf4108ece8424d15e4062c982",
        "open-pencil": "50afc5cb789257338cd4102235ab16d9ade458f3",
        "public-apis": "d6dab92da95c003e82e5b32c623bd2ad9d6a017f",
        "scroll-craft": "75d81f74e83692add18cd7a8a8e078b8a887a579",
        "security-audit-skill": "c1c8a8c1471069fb0e188eeaff69b8e8db6564a8",
        "taste-skill": "f6b76575f949707b4e3c37cd86cb44b0b98643e8",
        "unslop": "620163eedb3529d9cd23a3994ed8d287d06f760d"
    }

    def test_protected_files_integrity(self):
        """Verify that all 10 protected deliverable files remain bit-for-bit unchanged."""
        for rel_path, expected in self.AUTHORITATIVE_BASELINES.items():
            p = Path(rel_path)
            self.assertTrue(p.exists(), f"Protected file {rel_path} is missing!")
            data = p.read_bytes()
            actual_size = len(data)
            actual_sha = hashlib.sha256(data).hexdigest()

            # Direct match
            if actual_size == expected["size"] and actual_sha == expected["sha256"]:
                continue

            # Check if git cross-platform checkout translated line endings (CRLF vs LF)
            crlf_data = data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
            if len(crlf_data) == expected["size"] and hashlib.sha256(crlf_data).hexdigest() == expected["sha256"]:
                continue

            lf_data = data.replace(b"\r\n", b"\n")
            if len(lf_data) == expected["size"] and hashlib.sha256(lf_data).hexdigest() == expected["sha256"]:
                continue

            self.assertEqual(
                actual_size,
                expected["size"],
                f"Size mismatch on protected file {rel_path}: expected {expected['size']}, got {actual_size}"
            )
            self.assertEqual(
                actual_sha,
                expected["sha256"],
                f"SHA-256 mismatch on protected file {rel_path}: expected {expected['sha256']}, got {actual_sha}"
            )

    def test_19_repositories_head_commits(self):
        """Verify that all 19 source checkouts point to their exact accepted commit SHAs."""
        sources_dir = Path("research/sources")
        if not sources_dir.exists():
            self.skipTest("research/sources directory is not present in repository checkout (gitignored)")

        for repo_name, exp_sha in self.AUTHORITATIVE_REPO_SHAS.items():
            git_dir = sources_dir / repo_name / ".git"
            self.assertTrue(git_dir.exists(), f"Git directory missing for {repo_name}")

            head_file = git_dir / "HEAD"
            self.assertTrue(head_file.exists())
            head_content = head_file.read_text(encoding="utf-8").strip()

            actual_sha = ""
            if head_content.startswith("ref:"):
                ref_path = git_dir / head_content.split(":", 1)[1].strip()
                if ref_path.exists():
                    actual_sha = ref_path.read_text(encoding="utf-8").strip()
                else:
                    # check packed-refs
                    packed = git_dir / "packed-refs"
                    if packed.exists():
                        for line in packed.read_text(encoding="utf-8").splitlines():
                            if head_content.split(":", 1)[1].strip() in line:
                                actual_sha = line.split()[0]
                                break
            else:
                actual_sha = head_content

            self.assertEqual(
                actual_sha,
                exp_sha,
                f"Commit SHA mismatch on repository {repo_name}: expected {exp_sha}, got {actual_sha}"
            )

if __name__ == "__main__":
    unittest.main()

