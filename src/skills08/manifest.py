"""
Manifest loader and validator for Skills08.
Includes built-in pure Python standard-library parser with PyYAML fallback.
"""

import re
from pathlib import Path
from typing import List, Dict, Any, Optional

from .models import Candidate, CandidateProvenance
from .constants import (
    MANIFEST_PATH,
    MODEL_A_INSTRUCTION_ONLY,
    MODEL_NATIVE,
    MODEL_COMPANION,
    MODEL_SUBAGENT,
    MODEL_DEFERRED,
    TIER_1_STANDARD,
    TIER_2_CONDITIONAL,
    TIER_3_RESTRICTED,
    TIER_4_DEFERRED
)

def _parse_yaml_builtin(text: str) -> Dict[str, Any]:
    """Pure standard-library parser for manifests/manifest.yaml (no PyYAML required)."""
    candidates = []
    blocks = re.split(r'\n\s*-\s+id:\s*', text)
    if len(blocks) < 2:
        return {'candidates': []}
    
    for block in blocks[1:]:
        lines = block.splitlines()
        first_line = lines[0].strip()
        cand = {
            'id': first_line,
            'upstream_provenance': {},
            'compatibility': {},
            'operational_requirements': {'supporting_files': []},
            'distribution_metadata': {}
        }
        
        curr_obj = cand
        multiline_key = None
        multiline_indent = 0
        multiline_lines = []
        
        for line in lines[1:]:
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            
            indent = len(line) - len(line.lstrip())
            
            if multiline_key is not None:
                if indent > multiline_indent:
                    multiline_lines.append(stripped)
                    continue
                else:
                    curr_obj[multiline_key] = ' '.join(multiline_lines)
                    multiline_key = None
                    multiline_lines = []

            if line.strip().endswith(':'):
                k = line.strip()[:-1].strip()
                if k in cand:
                    curr_obj = cand[k]
                elif k == 'supporting_files':
                    curr_obj = cand['operational_requirements']['supporting_files']
                continue

            if stripped.startswith('- ') and isinstance(curr_obj, list):
                curr_obj.append(stripped[2:].strip())
                continue

            if ':' in stripped:
                k, v = stripped.split(':', 1)
                k = k.strip()
                v = v.strip()
                if v in ['>-', '>']:
                    multiline_key = k
                    multiline_indent = indent
                    multiline_lines = []
                else:
                    if isinstance(curr_obj, dict):
                        curr_obj[k] = v
        
        if multiline_key is not None and isinstance(curr_obj, dict):
            curr_obj[multiline_key] = ' '.join(multiline_lines)
            
        candidates.append(cand)
    return {'candidates': candidates}

class ManifestLoader:
    """Loads and validates candidates from the authoritative manifest.yaml."""

    def __init__(self, manifest_path: Optional[str] = None):
        self.manifest_path = Path(manifest_path) if manifest_path else Path(MANIFEST_PATH)

    def load(self) -> List[Candidate]:
        if not self.manifest_path.exists():
            raise FileNotFoundError(f"Authoritative manifest not found at {self.manifest_path}")

        raw_text = self.manifest_path.read_text(encoding="utf-8")
        
        data = None
        try:
            import yaml
            data = yaml.safe_load(raw_text)
        except Exception:
            data = None

        if not data or not isinstance(data, dict):
            data = _parse_yaml_builtin(raw_text)

        candidates: List[Candidate] = []
        raw_candidates = data.get("candidates", [])

        for raw in raw_candidates:
            prov_data = raw.get("upstream_provenance", {})
            prov = CandidateProvenance(
                repository_url=prov_data.get("repository_url", ""),
                commit_sha=prov_data.get("commit_sha", ""),
                source_file_path=prov_data.get("source_file_path", ""),
                author=prov_data.get("author", ""),
                declared_license=prov_data.get("declared_license", ""),
                inventory_status=prov_data.get("inventory_status", "")
            )

            cid = raw.get("id", "")
            cname = raw.get("name", "")
            comp = raw.get("compatibility", {})
            op_req = raw.get("operational_requirements", {})

            # Map operational model based on D4/D7 determinations
            if cid in ["SKILL08-DOC-001", "SKILL08-SWE-001", "SKILL08-SWE-002", "SKILL08-SWE-003"]:
                op_model = MODEL_NATIVE
            elif cid in ["SKILL08-ARC-001", "SKILL08-FE-001", "SKILL08-FE-002", "SKILL08-UI-001", "SKILL08-UI-002", "SKILL08-UI-003"]:
                op_model = MODEL_A_INSTRUCTION_ONLY
            elif cid == "SKILL08-SEC-001":
                op_model = MODEL_COMPANION
            elif cid == "SKILL08-TST-001":
                op_model = MODEL_SUBAGENT
            elif cid == "SKILL08-UI-004":
                op_model = MODEL_DEFERRED
            else:
                op_model = MODEL_NATIVE

            # Map legal tier from D3
            if cid in ["SKILL08-SEC-001", "SKILL08-DOC-001", "SKILL08-UI-002", "SKILL08-FE-001", "SKILL08-SWE-001", "SKILL08-TST-001", "SKILL08-SWE-003", "SKILL08-FE-002"]:
                lic_tier = TIER_1_STANDARD
            elif cid in ["SKILL08-SWE-002", "SKILL08-UI-001"]:
                lic_tier = TIER_2_CONDITIONAL
            elif cid in ["SKILL08-ARC-001", "SKILL08-UI-003"]:
                lic_tier = TIER_3_RESTRICTED
            elif cid == "SKILL08-UI-004":
                lic_tier = TIER_4_DEFERRED
            else:
                lic_tier = TIER_1_STANDARD

            supporting = op_req.get("supporting_files", []) or []

            cand = Candidate(
                id=cid,
                name=cname,
                display_name=raw.get("display_name", cname),
                category=raw.get("category", ""),
                tier=raw.get("tier", ""),
                description=raw.get("description", ""),
                status=comp.get("status", "Unknown"),
                operational_model=op_model,
                provenance=prov,
                supporting_files=supporting,
                adaptation_requirements=comp.get("adaptation_requirements", ""),
                license_clearance=lic_tier,
                security_guidelines=self._get_security_summary(cid)
            )
            candidates.append(cand)

        return candidates

    def _get_security_summary(self, candidate_id: str) -> str:
        summaries = {
            "SKILL08-SEC-001": "Guidance Mode Mandatory on Windows. Full audit execution & target scripts disabled. Static exploration only via research subagent.",
            "SKILL08-DOC-001": "Pure prompt with built-in prompt injection defense. Lowest residual risk.",
            "SKILL08-UI-001": "Model A pure instruction. scripts/snapshot.mjs omitted to eliminate web egress and API token requirements.",
            "SKILL08-UI-002": "Model A pure instruction. scripts/sloplint.mjs omitted to avoid Node.js file modification risks.",
            "SKILL08-FE-001": "Model A pure instruction. scripts/gate.mjs and shell stop hooks omitted to eliminate loopback port 7600/7601 binding and bash syntax crashes.",
            "SKILL08-SWE-001": "Pure prompt. Read-only code analysis instructions; lowest residual risk.",
            "SKILL08-SWE-002": "Pure prompt. Read-only refactoring instructions; bundled local MIT license.",
            "SKILL08-TST-001": "Chrome DevTools Protocol via Antigravity native browser subagent. Controlled host-managed browser session.",
            "SKILL08-SWE-003": "Pure prompt. Hypothesis-driven debugging guidelines; lowest residual risk.",
            "SKILL08-ARC-001": "Model A pure instruction. bin/archify.mjs omitted to neutralize 15 spawnSync call sites and process execution risks.",
            "SKILL08-FE-002": "Model A pure instruction. scripts/kie.mjs omitted to eliminate unsanitized image upload vector (SEC-SCR-003); frontmatter sanitized.",
            "SKILL08-UI-003": "Model A pure instruction fallback. Shell launcher and non-distributable font binaries omitted; locked to pure instruction playbooks.",
            "SKILL08-UI-004": "Deferred to Group B (v0.2+). Requires external Bun runtime and local MCP server daemons."
        }
        return summaries.get(candidate_id, "Standard static instruction guidelines.")
