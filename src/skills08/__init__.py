"""
Skills08: Local-First AI Agent Skill Distribution & Lifecycle Manager.
Empowering every AI coding agent with verified, high-quality skills.
"""

from .constants import VERSION
from .catalog import Catalog
from .installer import Installer
from .verifier import IntegrityVerifier
from .conflicts import ConflictDetector
from .scaffold import SkillScaffolder
from .packager import SkillPackager
from .doctor import EnvironmentDoctor
from .agent_config import AgentConfigManager

__version__ = VERSION
__author__ = "Skills08 Project"
__license__ = "MIT"

__all__ = [
    "Catalog",
    "Installer",
    "IntegrityVerifier",
    "ConflictDetector",
    "SkillScaffolder",
    "SkillPackager",
    "EnvironmentDoctor",
    "AgentConfigManager",
    "__version__"
]
