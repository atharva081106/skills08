"""
Conflict detection engine based on accepted Deliverable 6 taxonomy.
"""

from pathlib import Path
from typing import List, Dict, Optional, Tuple

from .models import ConflictIssue, InstalledSkill
from .constants import (
    CROSS_REPO_COLLISIONS,
    AESTHETIC_OVERLAP_CLUSTER,
    DEFAULT_PROJECT_SCOPE,
    DEFAULT_GLOBAL_SCOPE
)

class ConflictDetector:
    """Detects potential naming, shadowing, and capability conflicts."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path(".")

    def check_cross_repo_collision(self, skill_name: str) -> Optional[ConflictIssue]:
        """Check if skill name matches one of the 5 cross-repo collisions (CON-011)."""
        if skill_name in CROSS_REPO_COLLISIONS:
            sources = CROSS_REPO_COLLISIONS[skill_name]
            return ConflictIssue(
                conflict_id="CON-011",
                name=f"Cross-Repository Lexical Collision: {skill_name}",
                severity="Medium",
                category="Naming & Discovery",
                description=f"Skill name '{skill_name}' appears across multiple distinct upstream repositories ({', '.join(sources)}). Flat installation without namespacing causes collisions.",
                affected_skills=[skill_name],
                mitigation="Install canonical single-origin package curated by Skills08."
            )
        return None

    def detect_scope_shadowing(
        self,
        project_skills: List[InstalledSkill],
        global_skills: List[InstalledSkill]
    ) -> List[ConflictIssue]:
        """Detect dual-scope shadowing between project and global installations (CON-005)."""
        issues: List[ConflictIssue] = []
        global_names = {s.name: s for s in global_skills}

        for p_skill in project_skills:
            if p_skill.name in global_names:
                g_skill = global_names[p_skill.name]
                issues.append(ConflictIssue(
                    conflict_id="CON-005",
                    name=f"Dual-Scope Shadowing: {p_skill.name}",
                    severity="Medium",
                    category="Antigravity Platform Precedence",
                    description=(
                        f"Skill '{p_skill.name}' is installed in both Project Scope ({p_skill.path}) "
                        f"and Global Scope ({g_skill.path}). Antigravity prioritizes Project Scope; "
                        f"global configuration is shadowed in this workspace."
                    ),
                    affected_skills=[p_skill.name],
                    mitigation="Project scope override is intentional in Antigravity. Verify that workspace configuration meets expectations."
                ))
        return issues

    def detect_aesthetic_overlap(self, installed_skills: List[InstalledSkill]) -> Optional[ConflictIssue]:
        """Detect co-installation of competing aesthetic persona skills (CON-001)."""
        installed_names = {s.name for s in installed_skills}
        overlap = [name for name in AESTHETIC_OVERLAP_CLUSTER if name in installed_names]

        if len(overlap) > 1:
            return ConflictIssue(
                conflict_id="CON-001",
                name="Aesthetic Persona & Design Token Incompatibility",
                severity="Medium",
                category="Capability Overlap & Token Collision",
                description=(
                    f"Multiple competing frontend design skills are simultaneously active: {', '.join(overlap)}. "
                    "Unscoped co-loading may introduce conflicting styling heuristics and prompt bloat."
                ),
                affected_skills=overlap,
                mitigation=(
                    "Follow D7 REC-SYS-006: Scope skills by workflow phase — "
                    "'unslop' for pre-commit critique, 'hallmark' for component micro-polish, "
                    "'design-taste-frontend' for design system tokens, 'impeccable' for holistic UX direction."
                )
            )
        return None

    def scan_environment(
        self,
        project_skills: List[InstalledSkill],
        global_skills: List[InstalledSkill]
    ) -> List[ConflictIssue]:
        """Comprehensive scan across installed scopes."""
        all_issues: List[ConflictIssue] = []

        # 1. Check shadowing
        all_issues.extend(self.detect_scope_shadowing(project_skills, global_skills))

        # 2. Check aesthetic cluster in project
        aes_proj = self.detect_aesthetic_overlap(project_skills)
        if aes_proj:
            all_issues.append(aes_proj)

        # 3. Check for collisions in installed list
        for s in project_skills + global_skills:
            col = self.check_cross_repo_collision(s.name)
            if col and not any(i.name == col.name for i in all_issues):
                all_issues.append(col)

        return all_issues

