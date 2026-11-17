# Skills08 — Phase 1.5 Findings & Observations Register

> **Document Status**: Complete & Authoritative  
> **Milestone**: Phase 1.5 Controlled Product Validation  
> **Evaluation Date**: November 17, 2026  
> **Auditor**: Independent Product-Validation Engineer  
> **Classification Framework**: P0 (Critical), P1 (High), P2 (Medium), P3 (Low), OBSERVATION  
> **Summary**: 0 P0, 0 P1, 1 P2, 2 P3, 4 OBSERVATIONS  

---

## 1. Classification Taxonomy

- **P0 — Critical**: Demonstrable behavior creating immediate severe data loss, arbitrary remote code execution, or critical host security compromise.
- **P1 — High**: Significant safety, correctness, or operational defect preventing core functionality in supported environments.
- **P2 — Medium**: Meaningful usability, isolation, or reliability friction that hinders typical administrative or test workflows.
- **P3 — Low**: Minor documentation, presentation, syntactic, or convenience defect.
- **OBSERVATION**: Relevant architectural trade-off, environmental constraint, or documented governance limitation (not a defect).

---

## 2. Confirmed Defect Register

### FND-001: CLI Lacks Redirection Arguments for Global and Workspace Roots
- **Severity**: **P2 (Medium)**
- **Category**: Usability / Isolation & Testability
- **Affected Component**: `src/skills08/cli.py` (lines 186–232)
- **Reproduction Conditions**:
  1. Invoke `python skills08.py install <skill> --scope global` from any terminal or test harness.
  2. Attempt to redirect the installation to an isolated temporary directory via command-line arguments (e.g. `--global-root` or `--home`).
- **Expected Behavior**: The CLI should provide an optional flag (e.g. `--global-root <path>` or `--workspace <path>`) enabling operators and automated test harnesses to direct installation to an isolated directory without mutating the user's live system home (`~/.gemini/config/skills`).
- **Actual Behavior**: The CLI parser does not accept `--global-root` or `--workspace`. Line 232 instantiates `Installer()` with default parameters, hardcoding `global_skills_root` to `Path(os.path.expanduser("~/.gemini/config/skills"))`.
- **Supporting Evidence**:
  - `skills08 --help` and `skills08 install --help` expose only `--scope {project,global}` and `--force`.
  - In unit testing, `Installer(global_root=...)` supports redirection programmatically, but this capability is not exposed through the CLI entrypoint.
  - Workflow E was marked **BLOCKED** during Phase 1.5 validation because testing `--scope global` via the CLI would directly write to the user's host Antigravity configuration directory.
- **Impact**: Operators cannot test global-scope installations in sandboxed or CI/CD test runners without modifying real user profiles or ambient environment variables.
- **Confidence**: 100% (Confirmed via static code inspection and live CLI parameter parsing).
- **Recommended Future Action (Phase 2)**: Add `--workspace-root` and `--global-root` arguments to `build_parser()` in `src/skills08/cli.py` and pass them to `Installer(workspace_root=..., global_root=...)`.

---

### FND-002: `README.md` Stale Test Count and Invariance Claim Overstatement
- **Severity**: **P3 (Low)**
- **Category**: Documentation Accuracy & Governance Consistency
- **Affected Component**: `README.md` (lines 84, 86)
- **Reproduction Conditions**: Inspect `README.md` lines 84 and 86.
- **Expected Behavior**: `README.md` should accurately cite the 37-test validation suite and disclose the 9 PASS / 1 PARTIAL baseline score.
- **Actual Behavior**:
  - Line 84 states: `[`docs/TESTING_AND_VALIDATION_REPORT.md`](./docs/TESTING_AND_VALIDATION_REPORT.md) (27/27 Tests Passed)`. This references the early pre-remediation draft of the test suite before Windows compatibility (4 tests) and symlink/junction regressions (6 tests) were added.
  - Line 86 states: `[`docs/PROTECTED_BASELINE_INTEGRITY_REPORT.md`](./docs/PROTECTED_BASELINE_INTEGRITY_REPORT.md) (100% Invariance Certified)`. This makes an unqualified invariance claim, overlooking the preserved D5 Correction Report dual-baseline discrepancy (PARTIAL).
- **Supporting Evidence**:
  - `tests/test_report.json` and `docs/TESTING_AND_VALIDATION_REPORT.md` record 37 passing tests.
  - `docs/PROTECTED_BASELINE_INTEGRITY_REPORT.md` and `docs/FINAL_PROTECTED_BASELINE_VERIFICATION.md` evaluate baselines as **9 PASS, 1 PARTIAL**.
- **Impact**: Minor confusion for external users reading `README.md` before reading the detailed audit reports. Core software behavior is unaffected.
- **Confidence**: 100% (Verifiable by comparing `README.md` with audit deliverables).
- **Recommended Future Action (Phase 2)**: In the next documentation revision, update `README.md` line 84 to `(37/37 Tests Passed)` and line 86 to `(9 PASS, 1 PARTIAL — Dual-Baseline Disclosed)`.

---

### FND-003: `status` and `conflicts` Subcommands Lack Scope Filtering Options
- **Severity**: **P3 (Low)**
- **Category**: Usability / CLI Consistency
- **Affected Component**: `src/skills08/cli.py` (lines 96–136, 212–216)
- **Reproduction Conditions**:
  1. Run `python skills08.py status --scope project`.
  2. Run `python skills08.py conflicts --scope project`.
- **Expected Behavior**: Commands should accept an optional `--scope {project,global}` parameter to allow users to inspect only their active workspace or only global skills.
- **Actual Behavior**: `status` and `conflicts` reject `--scope` with `unrecognized arguments: --scope project` (exit code 2). Both commands always scan both project and global scopes concurrently.
- **Supporting Evidence**:
  - `build_parser()` in `cli.py` defines `p_status` and `p_conflicts` with zero sub-arguments.
- **Impact**: Minor user inconvenience when working in multi-user or shared environments where a user only wishes to audit the local repository.
- **Confidence**: 100% (Confirmed via CLI argument definition).
- **Recommended Future Action (Phase 2)**: Add optional `--scope` argument to `status` and `conflicts` subparsers.

---

## 3. Observations & Architectural Trade-offs

### OBS-001: Model A Pure-Instruction Mode Strips Execution Scripts
- **Category**: Architectural Design Trade-off
- **Observation**:
  Skills that originally included executable binaries, Node.js scripts, or shell utilities (e.g., `archify`, `scroll-craft`, `unslop`, `design-taste-frontend`, `hallmark`, `impeccable`) function purely as cognitive prompt playbooks under Model A. For example, `archify` omits `bin/archify.mjs` (which invoked 15 `spawnSync` subprocesses), directing the AI agent to emit ADR markdown directly.
- **Safety Assessment**: This is an intentional, highly effective security control for Phase 1. It completely eliminates arbitrary subprocess execution, loopback port zombies (ports 7600/7601 in `taste-skill`), and Windows environment script incompatibilities.
- **User Experience Note**: Users expecting automated command-line script execution from installed skills must be aware that Skills08 currently provides cognitive agent instructions rather than standalone executables.

---

### OBS-002: Windows Privilege Boundary on Symbolic Link Creation
- **Category**: Operating System Security & Privilege Architecture
- **Observation**:
  On Windows, creating symbolic links via `os.symlink` or `Path.symlink_to` requires either Windows Developer Mode enabled or the user account having `SeCreateSymbolicLinkPrivilege`.
- **Safety Assessment**: Skills08's installation routine copies files using standard file I/O and does NOT create symbolic links. Furthermore, its defense engine (`Installer._safe_remove_path` and `Path.is_relative_to`) defends against adversarial symlinks and directory junctions without requiring elevated privileges. On restricted corporate Windows environments where Developer Mode is disabled, adversarial attempts to create symlinks fail at the OS level before reaching the application.

---

### OBS-003: Historical Working-Tree Integrity Limitation Preserved
- **Category**: Governance Limitation
- **Observation**:
  All 19 source checkouts in `research/sources/` currently point to their accepted commit SHAs with 100% clean working trees (0 staged, 0 unstaged, 0 untracked). However, because recursive working-tree digests were not recorded in pre-D6 session logs, 100% historical working-tree integrity across all intermediate sessions cannot be retrospectively certified.
- **Safety Assessment**: Retained in the permanent record as a documented limitation; does not affect current software safety or curated package validity.

---

### OBS-004: D5 Correction Report Dual-Baseline Status Preserved as PARTIAL
- **Category**: Governance Limitation
- **Observation**:
  The on-disk version of `docs/research/SECURITY_AUDIT_CORRECTION_REPORT.md` is 19,014 bytes (`1ee7d5f1...`), reflecting the authorized Prompt 6 clarification (+126 bytes over the historical 18,888-byte baseline `8cc5824d...`).
- **Safety Assessment**: Formally retained as PARTIAL under dual-baseline governance. Baseline Gate 16 is rated PARTIAL, preventing uncertified upgrades.

---
*End of Findings & Observations Register (`validation/phase-1.5/FINDINGS_REGISTER.md`).*

