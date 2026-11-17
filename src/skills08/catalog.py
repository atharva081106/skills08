"""
Catalog manager for Skills08 candidate packages.
"""

from pathlib import Path
from typing import List, Dict, Optional

from .models import Candidate
from .manifest import ManifestLoader
from .constants import PACKAGES_DIR

class Catalog:
    """Manages index of available and installable candidate packages."""

    def __init__(self, packages_dir: str = PACKAGES_DIR, manifest_path: Optional[str] = None):
        loader = ManifestLoader(manifest_path) if manifest_path else ManifestLoader()
        self.candidates = loader.load()
        self.candidates_by_id: Dict[str, Candidate] = {c.id: c for c in self.candidates}
        self.candidates_by_name: Dict[str, Candidate] = {c.name: c for c in self.candidates}
        self.packages_dir = Path(packages_dir)

    def get_by_id(self, candidate_id: str) -> Optional[Candidate]:
        return self.candidates_by_id.get(candidate_id)

    def get_by_name(self, name: str) -> Optional[Candidate]:
        return self.candidates_by_name.get(name)

    def find(self, identifier: str) -> Optional[Candidate]:
        """Find candidate by either ID or skill name."""
        return self.get_by_id(identifier) or self.get_by_name(identifier)

    def get_group_a(self) -> List[Candidate]:
        """Return 12 approved Group A candidates for v0.1 launch."""
        return [c for c in self.candidates if "Group A" in c.tier]

    def get_group_b(self) -> List[Candidate]:
        """Return deferred Group B candidates."""
        return [c for c in self.candidates if "Group B" in c.tier]

    def has_package(self, skill_name: str) -> bool:
        """Check if a curated package exists in packages/<skill_name>/."""
        pkg_path = self.packages_dir / skill_name
        return pkg_path.exists() and (pkg_path / "SKILL.md").exists()

    def get_package_path(self, skill_name: str) -> Optional[Path]:
        pkg_path = self.packages_dir / skill_name
        if pkg_path.exists():
            return pkg_path
        return None

