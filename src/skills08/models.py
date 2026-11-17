"""
Data models for Skills08 candidates, packages, conflicts, and verification.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any

@dataclass
class CandidateProvenance:
    repository_url: str
    commit_sha: str
    source_file_path: str
    author: str
    declared_license: str
    inventory_status: str

@dataclass
class Candidate:
    id: str
    name: str
    display_name: str
    category: str
    tier: str
    description: str
    status: str
    operational_model: str
    provenance: CandidateProvenance
    supporting_files: List[str] = field(default_factory=list)
    adaptation_requirements: str = ""
    license_clearance: str = ""
    security_guidelines: str = ""

@dataclass
class InstalledSkill:
    name: str
    scope: str
    path: str
    manifest_id: Optional[str] = None
    files_count: int = 0
    is_shadowed: bool = False

@dataclass
class ConflictIssue:
    conflict_id: str
    name: str
    severity: str
    category: str
    description: str
    affected_skills: List[str]
    mitigation: str

@dataclass
class FileHashRecord:
    relative_path: str
    size_bytes: int
    sha256: str

@dataclass
class PackageLock:
    skill_name: str
    candidate_id: str
    version: str
    scope: str
    install_timestamp: str
    files: Dict[str, FileHashRecord]

@dataclass
class VerificationItem:
    relative_path: str
    expected_hash: str
    actual_hash: Optional[str]
    status: str  # MATCH, MODIFIED, MISSING, EXTRA
    details: str = ""

