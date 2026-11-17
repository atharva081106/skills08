# Skills08 — Phase 1.5 Evidence Index

> **Document Status**: Complete & Authoritative  
> **Milestone**: Phase 1.5 Controlled Product Validation  
> **Evaluation Date**: November 17, 2026  
> **Evidence Directory**: `D:\skills08\validation\phase-1.5\`  
> **Primary Machine-Readable Evidence**: `D:\skills08\validation\phase-1.5\workflow_execution_evidence.json`  

---

## 1. Runtime Environment Capture

| Property | Verified Value | Acquisition Method |
| :--- | :--- | :--- |
| **Operating System** | `Microsoft Windows [Version 10.0.26300.9974]` | `cmd /c ver` |
| **OS Platform Version** | `Windows-10-10.0.26300-SP0` (`10.0.26300`) | `platform.platform()`, `platform.version()` |
| **Python Binary** | `C:\Users\athar\AppData\Local\Programs\Python\Python310\python.exe` | `sys.executable` |
| **Python Version** | `3.10.11 (tags/v3.10.11:7d4cc5a, Apr  5 2023, 00:38:17) [MSC v.1929 64 bit (AMD64)]` | `sys.version` |
| **Windows PowerShell**| `5.1.26100.9818` | `powershell -Command "($PSVersionTable.PSVersion).ToString()"` |
| **Filesystem & Volume**| NTFS on Drive `D:\` (Case-preserving, case-insensitive, developer mode symlinks enabled) | System inspection |

---

## 2. Disposable Test Sandboxes Created & Cleaned

All test executions were strictly isolated from the production repository (`D:\skills08`) and the user's host profile (`C:\Users\athar\.gemini\config\skills`):

| Sandbox Path | Lifetime | Operations Performed | Disposition |
| :--- | :--- | :--- | :--- |
| `C:\Users\athar\AppData\Local\Temp\skills08_val_preflight_o13nixwf` | Preflight | CWD status probe via Python CLI | Completely deleted |
| `C:\Users\athar\AppData\Local\Temp\skills08_val_ps_f5lmsdiy` | Preflight | External PowerShell wrapper invocation | Completely deleted |
| `C:\Users\athar\AppData\Local\Temp\skills08_val_runner_bnnbv3s8` | Workflow Harness | Complete battery for Workflows A, B, C, D, F, G, H, and space/wrapper tests | Completely deleted after JSON output generation |

---

## 3. Workflow Execution Evidence Register

Extracted from `workflow_execution_evidence.json`:

```json
{
  "WFA_help": {
    "command": "python D:\\skills08\\skills08.py --help",
    "exit_code": 0,
    "stdout_snippet": "usage: skills08 [-h] {list,inspect,install,uninstall,status,conflicts,verify} ...\nSkills08: Local-First AI Agent Skill Distribution & Lifecycle Manager"
  },
  "WFA_list": {
    "command": "python D:\\skills08\\skills08.py list",
    "exit_code": 0,
    "stdout_snippet": "=== Skills08 Phase 1 Candidate Catalog ===\nCandidate ID    | Skill Name                    | Category ...\nTotal Candidates: 13 (12 Approved Group A, 1 Deferred Group B)"
  },
  "WFA_inspect_humanizer": {
    "command": "python D:\\skills08\\skills08.py inspect humanizer",
    "exit_code": 0,
    "stdout_snippet": "=== Candidate Inspection: humanizer (SKILL08-DOC-001) ===\nDisplay Name: Humanizer Prose Refinement\nLegal Clearance: Tier 1: Standard Clearance (MIT)"
  },
  "WFC_conflicts_detected": {
    "command": "python D:\\skills08\\skills08.py conflicts",
    "exit_code": 2,
    "stdout_snippet": "=== Skills08 Conflict & Shadowing Analysis ===\nDetected 1 ecosystem interaction issue(s):\n[1] CON-001: Aesthetic Style and Persona Collision (Severity: High)"
  },
  "WFD_install": {
    "command": "python D:\\skills08\\skills08.py install humanizer",
    "exit_code": 0,
    "stdout_snippet": "[OK] Successfully installed 'humanizer' (SKILL08-DOC-001) to ...\\.agents\\skills\\humanizer [project scope]."
  },
  "WFF_verify_modified": {
    "command": "python D:\\skills08\\skills08.py verify",
    "exit_code": 3,
    "stdout_snippet": "-> Verifying humanizer [project]:\n   [MODIFIED] SKILL.md (Hash mismatch: ... vs ...)\nVerification Summary: 1/2 files verified identical.\n[FAILED] Integrity drift or missing assets detected."
  },
  "WFF_verify_missing": {
    "command": "python D:\\skills08\\skills08.py verify",
    "exit_code": 3,
    "stdout_snippet": "-> Verifying humanizer [project]:\n   [MISSING] NOTICE.md (File is missing from installed directory)\n[FAILED] Integrity drift or missing assets detected."
  },
  "WFF_verify_extra": {
    "command": "python D:\\skills08\\skills08.py verify",
    "exit_code": 3,
    "stdout_snippet": "-> Verifying humanizer [project]:\n   [EXTRA] rogue_injected.txt (Uncurated extraneous file detected in skill directory)\n[FAILED] Integrity drift or missing assets detected."
  },
  "WFG_uninstall": {
    "command": "python D:\\skills08\\skills08.py uninstall humanizer",
    "exit_code": 0,
    "stdout_snippet": "[OK] Successfully uninstalled 'humanizer' from project scope."
  },
  "WFG_uninstall_traversal": {
    "command": "python D:\\skills08\\skills08.py uninstall ../../escape",
    "exit_code": 1,
    "stderr_snippet": "[FAILED] Security violation: path traversal detected for '...\\escape'."
  },
  "WFH_group_b": {
    "command": "python D:\\skills08\\skills08.py install open-pencil",
    "exit_code": 1,
    "stderr_snippet": "[FAILED] Candidate 'open-pencil' (SKILL08-UI-004) is deferred to Group B (v0.2+). Installation is disabled in Phase 1 per D7 recommendation REC-CAN-013."
  },
  "WFH_duplicate_noforce": {
    "command": "python D:\\skills08\\skills08.py install humanizer",
    "exit_code": 1,
    "stderr_snippet": "[FAILED] Skill 'humanizer' is already installed at ... Use --force to overwrite."
  }
}
```

---

## 4. Protected Baseline Invariance Verification

Computed live during Phase 1.5 validation:

| Resource Path | Accepted Authoritative Digest | Live Recomputed Digest | Verification Result |
| :--- | :--- | :--- | :---: |
| `docs/research/SOURCE_INVENTORY.md` | `35e44916...` | `35e44916...` | **MATCH** |
| `docs/research/SKILLS_EXTRACTION.md` | `31349284...` | `31349284...` | **MATCH** |
| `docs/research/LICENSE_MATRIX.md` | `893685d8...` | `893685d8...` | **MATCH** |
| `docs/research/COMPATIBILITY_MATRIX.md` | `88123497...` | `88123497...` | **MATCH** |
| `docs/research/SECURITY_AUDIT.md` | `6f003f9d...` | `6f003f9d...` | **MATCH** |
| `docs/research/SECURITY_AUDIT_CORRECTION_REPORT.md` | Dual: `8cc5824d...` / `1ee7d5f1...` | `1ee7d5f1...` | **PARTIAL (Preserved)** |
| `docs/research/CONFLICT_ANALYSIS.md` | `88931095...` | `88931095...` | **MATCH** |
| `docs/research/D6_FINAL_VERIFICATION_REPORT.md` | `69137f71...` | `69137f71...` | **MATCH** |
| `manifests/manifest.yaml` | `bec876bb...` | `bec876bb...` | **MATCH** |
| `research/final_reconciled_ledger.json` | `c85e759e...` | `c85e759e...` | **MATCH** |
| **19 Locked Repositories** | 19 Accepted SHAs | 19 Clean HEADs | **MATCH (0 modified files)** |

---

## 5. Verification Limitations & Environmental Caveats

1. **Global-Scope CLI Evaluation Boundary**: Testing of `--scope global` via the CLI was blocked by safety governance Rule 3.5 because the CLI does not expose arguments to redirect `global_skills_root` away from `~/.gemini/config/skills`. Programmatic verification in unit testing confirms the underlying logic functions as designed.
2. **Historical Working-Tree Integrity**: In accordance with documented Phase 1 governance, clean current working trees across all 19 source checkouts confirm current integrity, but do not retrospectively certify historical working-tree invariance prior to D6.
3. **Execution Absence**: No upstream scripts or binary tools were executed, in strict compliance with Model A safety guidelines.

---
*End of Evidence Index (`validation/phase-1.5/EVIDENCE_INDEX.md`).*

