"""
Skill packager and bundle creator for Skills08.
Validates skill structure and exports standard tar.gz bundles with cryptographic checksums.
"""

import os
import tarfile
import hashlib
import re
from pathlib import Path
from typing import Tuple, List, Dict, Any, Optional

class SkillPackager:
    """Validates and packages agent skills into distributable archives."""

    FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

    @classmethod
    def validate_skill_dir(cls, skill_dir: Path) -> Tuple[bool, List[str]]:
        """
        Validate whether a directory meets the standard agent skill layout.
        Returns (is_valid, list_of_errors_or_warnings).
        """
        issues = []
        if not skill_dir.exists():
            return False, [f"Directory does not exist: {skill_dir}"]
        if not skill_dir.is_dir():
            return False, [f"Path is not a directory: {skill_dir}"]

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            return False, [f"Missing required 'SKILL.md' at {skill_md}"]

        content = skill_md.read_text(encoding="utf-8", errors="replace")
        match = cls.FRONTMATTER_PATTERN.match(content)
        if not match:
            issues.append("SKILL.md is missing standard YAML frontmatter ('---' header).")
        else:
            fm_text = match.group(1)
            if "name:" not in fm_text:
                issues.append("YAML frontmatter missing required 'name' field.")
            if "description:" not in fm_text:
                issues.append("YAML frontmatter missing required 'description' field.")

        # Check for dangerous or unintended binaries
        dangerous_extensions = {".exe", ".dll", ".bat", ".cmd", ".vbs", ".ps1"}
        for f in skill_dir.rglob("*"):
            if f.is_file() and f.suffix.lower() in dangerous_extensions:
                issues.append(f"Potentially dangerous executable script found: {f.name}")

        is_valid = len([i for i in issues if "missing required" in i.lower()]) == 0
        return is_valid, issues

    @classmethod
    def pack(
        cls,
        skill_dir: Path,
        output_dir: Optional[Path] = None,
        archive_name: Optional[str] = None
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Package a validated skill directory into a .tar.gz bundle.
        Returns (success, message, metadata).
        """
        is_valid, issues = cls.validate_skill_dir(skill_dir)
        if not is_valid:
            return False, f"Validation failed: {'; '.join(issues)}", {}

        skill_name = skill_dir.name
        out_dir = output_dir or skill_dir.parent
        out_dir.mkdir(parents=True, exist_ok=True)

        target_archive = out_dir / (archive_name or f"{skill_name}.tar.gz")

        try:
            # Build tar.gz deterministically
            file_hashes: Dict[str, Dict[str, Any]] = {}
            total_uncompressed_bytes = 0

            with tarfile.open(target_archive, "w:gz") as tar:
                for item in sorted(skill_dir.rglob("*")):
                    if item.is_file():
                        rel = str(item.relative_to(skill_dir)).replace("\\", "/")
                        data = item.read_bytes()
                        sha = hashlib.sha256(data).hexdigest()
                        size = len(data)
                        total_uncompressed_bytes += size
                        file_hashes[rel] = {
                            "sha256": sha,
                            "size_bytes": size
                        }

                        # Add with normalized arcname
                        arcname = f"{skill_name}/{rel}"
                        tar.add(item, arcname=arcname)

            archive_bytes = target_archive.read_bytes()
            archive_sha256 = hashlib.sha256(archive_bytes).hexdigest()

            metadata = {
                "skill_name": skill_name,
                "archive_path": str(target_archive.resolve()),
                "archive_name": target_archive.name,
                "archive_sha256": archive_sha256,
                "archive_size_bytes": len(archive_bytes),
                "uncompressed_size_bytes": total_uncompressed_bytes,
                "files_count": len(file_hashes),
                "files": file_hashes,
                "warnings": [i for i in issues if "Potentially dangerous" in i]
            }

            return True, f"Successfully packaged '{skill_name}' to {target_archive.name}", metadata

        except Exception as e:
            return False, f"Packaging failed: {e}", {}

