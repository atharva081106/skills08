"""
Atomic filesystem installer and lifecycle manager for Skills08.
"""

import os
import shutil
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Optional, Tuple

from .models import Candidate, InstalledSkill, FileHashRecord, PackageLock
from .catalog import Catalog
from .constants import (
    DEFAULT_PROJECT_SCOPE,
    DEFAULT_GLOBAL_SCOPE,
    LOCK_FILE_NAME
)

class Installer:
    """Installs, uninstalls, and tracks skills across project and global scopes."""

    def __init__(self, workspace_root: Optional[Path] = None, global_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path(".")).resolve()
        self.project_skills_root = (self.workspace_root / DEFAULT_PROJECT_SCOPE).resolve()
        
        if global_root:
            self.global_skills_root = global_root.resolve()
        else:
            self.global_skills_root = Path(os.path.expanduser(DEFAULT_GLOBAL_SCOPE)).resolve()

        self.catalog = Catalog()

    def get_target_root(self, scope: str = "project") -> Path:
        """Resolve and validate target installation root."""
        if scope.lower() == "project":
            return self.project_skills_root
        elif scope.lower() == "global":
            return self.global_skills_root
        else:
            raise ValueError(f"Invalid scope '{scope}'. Must be 'project' or 'global'.")

    def list_installed(self, scope: Optional[str] = None) -> List[InstalledSkill]:
        """List all skills installed in specified scope or both scopes."""
        results: List[InstalledSkill] = []

        scopes_to_check = []
        if scope is None or scope.lower() == "project":
            scopes_to_check.append(("project", self.project_skills_root))
        if scope is None or scope.lower() == "global":
            scopes_to_check.append(("global", self.global_skills_root))

        for sc_name, sc_root in scopes_to_check:
            if not sc_root.exists():
                continue
            for item in sorted(sc_root.iterdir()):
                if item.is_dir() and (item / "SKILL.md").exists():
                    files = [f for f in item.rglob("*") if f.is_file()]
                    
                    cand = self.catalog.get_by_name(item.name)
                    cid = cand.id if cand else None

                    results.append(InstalledSkill(
                        name=item.name,
                        scope=sc_name,
                        path=str(item),
                        manifest_id=cid,
                        files_count=len(files),
                        is_shadowed=False
                    ))

        # Mark shadowing if scanning both scopes
        if scope is None:
            proj_names = {s.name for s in results if s.scope == "project"}
            for s in results:
                if s.scope == "global" and s.name in proj_names:
                    s.is_shadowed = True

        return results

    def is_installed(self, skill_name: str, scope: str = "project") -> bool:
        """Check if skill is already installed in target scope."""
        target_root = self.get_target_root(scope)
        skill_dir = target_root / skill_name
        return skill_dir.exists() and (skill_dir / "SKILL.md").exists()

    def install(
        self,
        identifier: str,
        scope: str = "project",
        force: bool = False
    ) -> Tuple[bool, str]:
        """Atomically install a curated candidate package into target scope."""
        cand = self.catalog.find(identifier)
        if not cand:
            return False, f"Candidate '{identifier}' not found in catalog."

        if "Group B" in cand.tier:
            return False, (
                f"Candidate '{cand.name}' ({cand.id}) is deferred to Group B (v0.2+). "
                "Installation is disabled in Phase 1 per D7 recommendation REC-CAN-013."
            )

        pkg_path = self.catalog.get_package_path(cand.name)
        if not pkg_path:
            return False, f"Curated package directory not found for skill '{cand.name}'."

        target_root = self.get_target_root(scope)
        skill_dest = target_root / cand.name

        # Path traversal defense: rigorous verification using is_relative_to
        try:
            skill_dest_resolved = skill_dest.resolve()
            target_root_resolved = target_root.resolve()
            
            # Defense against escaping root or targeting root itself
            if not skill_dest_resolved.is_relative_to(target_root_resolved) or skill_dest_resolved == target_root_resolved:
                return False, f"Security violation: path traversal detected for destination '{skill_dest}'."
        except Exception as e:
            return False, f"Path resolution error: {e}"

        if skill_dest.exists() and not force:
            return False, f"Skill '{cand.name}' is already installed at {skill_dest}. Use --force to overwrite."

        # Atomic installation via staging
        target_root.mkdir(parents=True, exist_ok=True)
        staging_dir = target_root / f".skills08_staging_{cand.name}_{int(datetime.now().timestamp())}_{os.urandom(4).hex()}"

        try:
            shutil.copytree(pkg_path, staging_dir)

            # Generate or verify NOTICE.md attribution
            notice_path = staging_dir / "NOTICE.md"
            if not notice_path.exists():
                self._generate_notice(cand, notice_path)

            # Remove existing destination if force overwrite
            if skill_dest.exists() or skill_dest.is_symlink():
                self._safe_remove_path(skill_dest)

            # Atomic rename into destination
            staging_dir.rename(skill_dest)

            # Update lock record
            self._update_lock(cand, skill_dest, scope)

            return True, f"Successfully installed '{cand.name}' ({cand.id}) to {skill_dest} [{scope} scope]."

        except Exception as e:
            if staging_dir.exists() or staging_dir.is_symlink():
                self._safe_remove_path(staging_dir)
            return False, f"Installation failed: {e}"

    def uninstall(self, skill_name: str, scope: str = "project") -> Tuple[bool, str]:
        """Safely remove an installed skill from the target scope."""
        # Validate skill_name to prevent directory root deletion
        if not skill_name or skill_name.strip() in [".", "..", "/", "\\", ""]:
            return False, "Security violation: invalid skill name for uninstallation."

        target_root = self.get_target_root(scope)
        skill_dir = target_root / skill_name.strip()

        # Path traversal defense using is_relative_to
        try:
            skill_dir_resolved = skill_dir.resolve()
            target_root_resolved = target_root.resolve()
            if not skill_dir_resolved.is_relative_to(target_root_resolved) or skill_dir_resolved == target_root_resolved:
                return False, f"Security violation: path traversal detected for '{skill_dir}'."
        except Exception as e:
            return False, f"Path resolution error: {e}"

        if not skill_dir.exists() and not skill_dir.is_symlink():
            return False, f"Skill '{skill_name}' is not installed in {scope} scope at {skill_dir}."

        try:
            self._safe_remove_path(skill_dir)
            self._remove_from_lock(skill_name, scope)
            return True, f"Successfully uninstalled '{skill_name}' from {scope} scope."
        except Exception as e:
            return False, f"Uninstall failed: {e}"

    @staticmethod
    def _safe_remove_path(target_path: Path) -> None:
        """Safely remove a file, directory, symlink, or junction without following reparse points."""
        if not target_path.exists() and not target_path.is_symlink():
            return
        if target_path.is_symlink() or not target_path.is_dir():
            target_path.unlink(missing_ok=True)
        else:
            try:
                shutil.rmtree(target_path)
            except OSError:
                # Handle directory junctions or reparse points where rmtree fails
                try:
                    target_path.rmdir()
                except Exception:
                    target_path.unlink(missing_ok=True)

    def _generate_notice(self, candidate: Candidate, target_path: Path) -> None:
        """Generate standardized attribution notice fulfilling D3 legal obligations."""
        prov = candidate.provenance
        notice_content = f"""# Skills08 Package Attribution Notice

**Skill Name**: `{candidate.name}`  
**Candidate ID**: `{candidate.id}`  
**Upstream Repository**: `{prov.repository_url}`  
**Locked Commit SHA**: `{prov.commit_sha}`  
**Author / Copyright Holder**: `{prov.author}`  
**Declared License**: `{prov.declared_license}`  
**Legal Clearance Tier**: `{candidate.license_clearance}`  
**Operational Model**: `{candidate.operational_model}`  

---

## Intellectual Property & License Statement

This skill definition was audited and packaged under the **Skills08** local-first distribution platform.
Original copyright belongs to the upstream author cited above.

### Governing License
Distributed under the terms of the `{prov.declared_license}` license.

### Modifications Made by Skills08
- Standardized directory layout for Google Antigravity discovery paths (`.agents/skills/`).
- Enforced `{candidate.operational_model}` operational model.
- Companion script execution omitted or sanitized for Windows host compatibility.
- Frontmatter sanitized for Antigravity schema compliance.
- Attribution notice generated automatically on installation.
"""
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(notice_content)

    def _get_lock_path(self, scope: str) -> Path:
        target_root = self.get_target_root(scope)
        return target_root / LOCK_FILE_NAME

    def _update_lock(self, candidate: Candidate, skill_dir: Path, scope: str) -> None:
        """Record installed file hashes in lock file."""
        lock_path = self._get_lock_path(scope)
        locks: Dict[str, Any] = {}
        if lock_path.exists():
            try:
                with open(lock_path, "r", encoding="utf-8") as f:
                    locks = json.load(f)
            except Exception:
                locks = {}

        file_records: Dict[str, Any] = {}
        for fpath in skill_dir.rglob("*"):
            if fpath.is_file():
                rel = str(fpath.relative_to(skill_dir)).replace("\\", "/")
                data = fpath.read_bytes()
                sha = hashlib.sha256(data).hexdigest()
                file_records[rel] = {
                    "size_bytes": len(data),
                    "sha256": sha
                }

        locks[candidate.name] = {
            "candidate_id": candidate.id,
            "version": "0.1.0",
            "scope": scope,
            "install_timestamp": datetime.now(timezone.utc).isoformat(),
            "files": file_records
        }

        with open(lock_path, "w", encoding="utf-8") as f:
            json.dump(locks, f, indent=2)

    def _remove_from_lock(self, skill_name: str, scope: str) -> None:
        lock_path = self._get_lock_path(scope)
        if not lock_path.exists():
            return
        try:
            with open(lock_path, "r", encoding="utf-8") as f:
                locks = json.load(f)
            if skill_name in locks:
                del locks[skill_name]
                with open(lock_path, "w", encoding="utf-8") as f:
                    json.dump(locks, f, indent=2)
        except Exception:
            pass
