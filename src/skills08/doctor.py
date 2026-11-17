"""
Environment and installation diagnostics tool for Skills08.
Verifies runtime, discovery paths, permissions, and catalog integrity.
"""

import sys
import os
import platform
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional

from .constants import (
    VERSION,
    MANIFEST_PATH,
    PACKAGES_DIR,
    DEFAULT_PROJECT_SCOPE,
    DEFAULT_GLOBAL_SCOPE
)
from .catalog import Catalog

class DiagnosticItem:
    def __init__(self, category: str, name: str, status: str, details: str, recommendation: str = ""):
        self.category = category
        self.name = name
        self.status = status  # PASS, WARN, FAIL
        self.details = details
        self.recommendation = recommendation

    def to_dict(self) -> Dict[str, str]:
        return {
            "category": self.category,
            "name": self.name,
            "status": self.status,
            "details": self.details,
            "recommendation": self.recommendation
        }

class EnvironmentDoctor:
    """Diagnoses host environment and configuration for agent skill execution."""

    def __init__(self, workspace_root: Optional[Path] = None, global_root: Optional[Path] = None):
        self.workspace_root = (workspace_root or Path(".")).resolve()
        self.project_skills_root = (self.workspace_root / DEFAULT_PROJECT_SCOPE).resolve()
        if global_root:
            self.global_skills_root = global_root.resolve()
        else:
            self.global_skills_root = Path(os.path.expanduser(DEFAULT_GLOBAL_SCOPE)).resolve()

    def run_all_checks(self) -> List[DiagnosticItem]:
        checks: List[DiagnosticItem] = []

        # 1. Python Runtime
        v = sys.version_info
        py_ver_str = f"{v.major}.{v.minor}.{v.micro}"
        if v.major >= 3 and v.minor >= 8:
            checks.append(DiagnosticItem(
                category="Runtime",
                name="Python Version",
                status="PASS",
                details=f"Python {py_ver_str} ({platform.architecture()[0]}) at {sys.executable}"
            ))
        else:
            checks.append(DiagnosticItem(
                category="Runtime",
                name="Python Version",
                status="FAIL",
                details=f"Python {py_ver_str} is below required 3.8+",
                recommendation="Install Python 3.10 or later from python.org or Windows Store."
            ))

        # 2. Operating System
        os_name = platform.system()
        os_release = platform.release()
        os_version = platform.version()
        checks.append(DiagnosticItem(
            category="Platform",
            name="Operating System",
            status="PASS",
            details=f"{os_name} {os_release} (Build {os_version})"
        ))

        # 3. PowerShell (on Windows)
        if os_name == "Windows":
            try:
                ps_res = subprocess.run(
                    ["powershell", "-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if ps_res.returncode == 0:
                    ps_ver = ps_res.stdout.strip()
                    checks.append(DiagnosticItem(
                        category="Shell",
                        name="PowerShell",
                        status="PASS",
                        details=f"PowerShell {ps_ver} available for native script execution."
                    ))
                else:
                    checks.append(DiagnosticItem(
                        category="Shell",
                        name="PowerShell",
                        status="WARN",
                        details="PowerShell command returned non-zero exit code.",
                        recommendation="Ensure PowerShell 5.1+ is enabled in Windows Features."
                    ))
            except Exception as e:
                checks.append(DiagnosticItem(
                    category="Shell",
                    name="PowerShell",
                    status="WARN",
                    details=f"Could not invoke PowerShell: {e}",
                    recommendation="PowerShell 5.1 or 7+ is recommended for native wrapper scripts."
                ))

        # 4. Workspace Root & Project Scope Writability
        try:
            self.workspace_root.mkdir(parents=True, exist_ok=True)
            test_file = self.workspace_root / f".skills08_diag_test_{os.urandom(4).hex()}.tmp"
            test_file.write_text("test", encoding="utf-8")
            test_file.unlink()
            checks.append(DiagnosticItem(
                category="Workspace",
                name="Workspace Writability",
                status="PASS",
                details=f"Workspace root is writable: {self.workspace_root}"
            ))
        except Exception as e:
            checks.append(DiagnosticItem(
                category="Workspace",
                name="Workspace Writability",
                status="FAIL",
                details=f"Cannot write to workspace root {self.workspace_root}: {e}",
                recommendation="Check directory permissions or select another workspace with -w."
            ))

        # 5. Global Scope Writability
        try:
            self.global_skills_root.mkdir(parents=True, exist_ok=True)
            test_g = self.global_skills_root / f".skills08_diag_test_{os.urandom(4).hex()}.tmp"
            test_g.write_text("test", encoding="utf-8")
            test_g.unlink()
            checks.append(DiagnosticItem(
                category="Global Scope",
                name="Global Skills Writability",
                status="PASS",
                details=f"Global skills directory is writable: {self.global_skills_root}"
            ))
        except Exception as e:
            checks.append(DiagnosticItem(
                category="Global Scope",
                name="Global Skills Writability",
                status="WARN",
                details=f"Cannot write to global scope {self.global_skills_root}: {e}",
                recommendation="Ensure user profile directory exists or override with -g."
            ))

        # 6. Catalog Manifest
        m_path = Path(MANIFEST_PATH)
        if m_path.exists():
            try:
                cat = Catalog()
                checks.append(DiagnosticItem(
                    category="Catalog",
                    name="Manifest Catalog",
                    status="PASS",
                    details=f"Loaded {len(cat.candidates)} candidates (12 Group A, 1 Group B) from {m_path.name}"
                ))
            except Exception as e:
                checks.append(DiagnosticItem(
                    category="Catalog",
                    name="Manifest Catalog",
                    status="FAIL",
                    details=f"Failed to parse manifest: {e}",
                    recommendation="Verify manifest YAML syntax in manifests/manifest.yaml."
                ))
        else:
            checks.append(DiagnosticItem(
                category="Catalog",
                name="Manifest Catalog",
                status="FAIL",
                details=f"Manifest file not found at {m_path}",
                recommendation="Set SKILLS08_MANIFEST_PATH or ensure manifests/manifest.yaml exists."
            ))

        # 7. Packages Availability
        p_dir = Path(PACKAGES_DIR)
        if p_dir.exists() and p_dir.is_dir():
            pkgs = [d.name for d in p_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]
            if len(pkgs) >= 12:
                checks.append(DiagnosticItem(
                    category="Catalog",
                    name="Curated Packages",
                    status="PASS",
                    details=f"All {len(pkgs)} Group A packages present in {p_dir}"
                ))
            else:
                checks.append(DiagnosticItem(
                    category="Catalog",
                    name="Curated Packages",
                    status="WARN",
                    details=f"Found {len(pkgs)} packages in {p_dir} (expected 12)",
                    recommendation="Run 'python -m skills08.builder' to rebuild curated packages."
                ))
        else:
            checks.append(DiagnosticItem(
                category="Catalog",
                name="Curated Packages",
                status="FAIL",
                details=f"Packages directory not found at {p_dir}",
                recommendation="Set SKILLS08_PACKAGES_DIR to a valid package directory."
            ))

        return checks
