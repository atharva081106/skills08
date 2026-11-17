"""
Constants for Skills08 lifecycle management and discovery.
"""

from pathlib import Path

# Repository Root (determined dynamically from package location)
REPO_ROOT = Path(__file__).resolve().parent.parent.parent

# Discovery Roots
DEFAULT_PROJECT_SCOPE = ".agents/skills"
DEFAULT_GLOBAL_SCOPE = "~/.gemini/config/skills"

# Research and Manifest Baselines
MANIFEST_PATH = str(REPO_ROOT / "manifests" / "manifest.yaml")
PACKAGES_DIR = str(REPO_ROOT / "packages")
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
