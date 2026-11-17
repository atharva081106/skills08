"""
Cryptographic integrity verifier for installed Skills08 packages.
"""

import hashlib
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from .models import VerificationItem, InstalledSkill
from .installer import Installer
from .catalog import Catalog
from .constants import LOCK_FILE_NAME

class IntegrityVerifier:
    """Verifies file hashes and structural integrity of installed skills."""

    def __init__(self, installer: Optional[Installer] = None):
        self.installer = installer or Installer()
        self.catalog = self.installer.catalog

    def verify_skill(self, skill_name: str, scope: str = "project") -> List[VerificationItem]:
        """Verify integrity of a single installed skill."""
        target_root = self.installer.get_target_root(scope)
        skill_dir = target_root / skill_name
        items: List[VerificationItem] = []

        if not skill_dir.exists():
            items.append(VerificationItem(
                relative_path="",
                expected_hash="",
                actual_hash=None,
                status="MISSING",
                details=f"Skill directory not found at {skill_dir}"
            ))
            return items

        pkg_path = self.catalog.get_package_path(skill_name)
        if not pkg_path:
            items.append(VerificationItem(
                relative_path="",
                expected_hash="",
                actual_hash=None,
                status="UNKNOWN",
                details=f"No baseline package found for '{skill_name}'"
            ))
            return items

        # Read expected package files
        expected_files: Dict[str, str] = {}
        for f in pkg_path.rglob("*"):
            if f.is_file():
                rel = str(f.relative_to(pkg_path)).replace("\\", "/")
                expected_files[rel] = hashlib.sha256(f.read_bytes()).hexdigest()

        # Check installed files
        installed_files: Dict[str, str] = {}
        for f in skill_dir.rglob("*"):
            if f.is_file():
                rel = str(f.relative_to(skill_dir)).replace("\\", "/")
                # Ignore NOTICE.md if generated dynamically
                installed_files[rel] = hashlib.sha256(f.read_bytes()).hexdigest()

        # Compare expected vs installed
        for rel_path, exp_hash in expected_files.items():
            if rel_path not in installed_files:
                items.append(VerificationItem(
                    relative_path=rel_path,
                    expected_hash=exp_hash,
                    actual_hash=None,
                    status="MISSING",
                    details="Required file missing from installed skill directory."
                ))
            else:
                act_hash = installed_files[rel_path]
                if act_hash == exp_hash:
                    items.append(VerificationItem(
                        relative_path=rel_path,
                        expected_hash=exp_hash,
                        actual_hash=act_hash,
                        status="MATCH",
                        details="Cryptographic hash matches curated baseline."
                    ))
                else:
                    items.append(VerificationItem(
                        relative_path=rel_path,
                        expected_hash=exp_hash,
                        actual_hash=act_hash,
                        status="MODIFIED",
                        details="File content has drifted from curated baseline."
                    ))

        # Check for extra uncurated files
        for rel_path, act_hash in installed_files.items():
            if rel_path not in expected_files and rel_path != "NOTICE.md":
                items.append(VerificationItem(
                    relative_path=rel_path,
                    expected_hash="",
                    actual_hash=act_hash,
                    status="EXTRA",
                    details="Uncurated or unexpected file present in skill directory."
                ))

        return items

    def verify_all(self, scope: Optional[str] = None) -> Dict[str, List[VerificationItem]]:
        """Verify all installed skills in the specified scope."""
        installed = self.installer.list_installed(scope)
        results: Dict[str, List[VerificationItem]] = {}

        for skill in installed:
            key = f"{skill.name} [{skill.scope}]"
            results[key] = self.verify_skill(skill.name, skill.scope)

        return results

