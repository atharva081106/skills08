"""
Constants for Skills08 lifecycle management and discovery.
"""

import os
from pathlib import Path

# Version Information
VERSION = "0.2.0"

# Repository Root (determined dynamically from package location)
REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Discovery Roots
DEFAULT_PROJECT_SCOPE = ".agents/skills"
DEFAULT_GLOBAL_SCOPE = "~/.gemini/config/skills"

# Dynamic Resolution for Manifest and Packages (Env -> Repo -> Package Data)
def _resolve_manifest_path() -> str:
    env_val = os.environ.get("SKILLS08_MANIFEST_PATH")
    if env_val and Path(env_val).exists():
        return str(Path(env_val).resolve())
    repo_manifest = REPO_ROOT / "manifests" / "manifest.yaml"
    if repo_manifest.exists():
        return str(repo_manifest)
    pkg_manifest = Path(__file__).resolve().parent / "data" / "manifest.yaml"
    if pkg_manifest.exists():
        return str(pkg_manifest)
    return str(repo_manifest)

def _resolve_packages_dir() -> str:
    env_val = os.environ.get("SKILLS08_PACKAGES_DIR")
    if env_val and Path(env_val).exists():
        return str(Path(env_val).resolve())
    repo_pkgs = REPO_ROOT / "packages"
    if repo_pkgs.exists():
        return str(repo_pkgs)
    pkg_pkgs = Path(__file__).resolve().parent / "packages"
    if pkg_pkgs.exists():
        return str(pkg_pkgs)
    return str(repo_pkgs)

# Research and Manifest Baselines
MANIFEST_PATH = _resolve_manifest_path()
PACKAGES_DIR = _resolve_packages_dir()
LOCK_FILE_NAME = "skills08.lock.json"

# Operational Models
MODEL_A_INSTRUCTION_ONLY = "Model A (Instruction-Only)"
MODEL_NATIVE = "Native Pure-Instruction"
MODEL_COMPANION = "Companion-File Guidance Mode"
MODEL_SUBAGENT = "Native Subagent Dispatch"
MODEL_DEFERRED = "Deferred External Runtime (Group B)"

# Clearance Tiers from D3
TIER_1_STANDARD = "Tier 1: Standard Clearance (MIT)"
TIER_2_CONDITIONAL = "Tier 2: Conditional Clearance"
TIER_3_RESTRICTED = "Tier 3: Restricted Clearance (Apache-2.0)"
TIER_4_DEFERRED = "Tier 4: Deferred Clearance"

# Known Cross-Repository Collisions from D6 (Section 4.1)
CROSS_REPO_COLLISIONS = {
    "architecture-decision-records": ["antigravity-skills", "ecc"],
    "design-taste-frontend": ["taste-skill", "open-design"],
    "frontend-slides": ["ecc", "open-design"],
    "hallmark": ["hallmark", "open-design"],
    "hyperframes": ["hyperframes", "open-design"]
}

# Aesthetic Overlap Persona Cluster (CON-001)
AESTHETIC_OVERLAP_CLUSTER = [
    "unslop",
    "hallmark",
    "design-taste-frontend",
    "impeccable"
]

# Exit Codes
EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_CONFLICT = 2
EXIT_VERIFICATION_FAILED = 3
EXIT_NOT_FOUND = 4
EXIT_INVALID_ARGS = 5
