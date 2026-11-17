# Skills08 — Phase 1.5 Workflow Test Matrix

> **Document Status**: Complete & Authoritative  
> **Milestone**: Phase 1.5 Controlled Product Validation  
> **Execution Date**: November 17, 2026  
> **Validation Engineer**: Independent Product-Validation Engineer  
> **Host Platform**: Windows 11 Enterprise/Pro x64 (`Microsoft Windows [Version 10.0.26300.9974]`, `platform.version(): 10.0.26300`)  
> **Runtime**: Python 3.10.11 AMD64 | Windows PowerShell 5.1 (`5.1.26100.9818`)  
> **Overall Matrix Status**: **8 Workflows Evaluated: 7 PASS, 1 BLOCKED (Global Scope CLI Redirection)**  

---

## 1. Summary Workflow Execution Matrix

| Workflow ID | Workflow Domain | Preconditions | Tested Command / Operation | Expected Result | Actual Observed Result | Exit Code | Evaluation Status | Evidence Reference |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **WFA-01** | Initial Discovery: Help | Disposable directory created | `python D:\skills08\skills08.py --help` | Display usage, synopsis, and 7 available subcommands | Formatted help text displayed with 7 subcommands (`list`, `inspect`, `install`, `uninstall`, `status`, `conflicts`, `verify`) | `0` | **PASS** | `WFA_help` |
| **WFA-02** | Initial Discovery: Catalog List | Disposable directory created | `python D:\skills08\skills08.py list` | Display tabular catalog of 13 candidates with categories, tiers, models | Clean tabular list of 13 candidates rendered with accurate operational models and installation status | `0` | **PASS** | `WFA_list` |
| **WFA-03** | Initial Discovery: Inspect by Name | Catalog available | `python D:\skills08\skills08.py inspect humanizer` | Display full metadata, provenance, license, adaptation requirements | Complete metadata, Siqi Chen author, MIT license, prompt injection defense guidelines displayed | `0` | **PASS** | `WFA_inspect_humanizer` |
| **WFA-04** | Initial Discovery: Inspect by Candidate ID | Catalog available | `python D:\skills08\skills08.py inspect SKILL08-SEC-001` | Resolve ID to `security-audit` and display details | Candidate ID resolved to `security-audit`, Cloudflare author, MIT, Guidance Mode rules, and 17 companion assets listed | `0` | **PASS** | `WFA_inspect_id` |
| **WFB-01** | Skill Selection: General-Purpose | Candidate catalog available | `python D:\skills08\skills08.py inspect humanizer` | Understand prose refinement purpose and prompt injection defense | Clear description, no external scripts, safe prompt refinement | `0` | **PASS** | `WFA_inspect_humanizer` |
| **WFB-02** | Skill Selection: Development-Oriented | Candidate catalog available | `python D:\skills08\skills08.py inspect code-simplification` | Understand code review purpose and simplicity guidance | Clear description, Addy Osmani author, Native Pure-Instruction model | `0` | **PASS** | `WFB_inspect_dev` |
| **WFB-03** | Skill Selection: Security-Oriented | Candidate catalog available | `python D:\skills08\skills08.py inspect security-audit` | Understand Guidance Mode constraints on Windows | Prominently communicates Guidance Mode restriction: dynamic scripts disabled, findings route to `NEEDS-VALIDATION.md` | `0` | **PASS** | `WFB_inspect_sec` |
| **WFC-01** | Conflict Awareness: Clean Environment | 0 skills installed in disposable project | `python D:\skills08\skills08.py conflicts` | Report zero conflicts | Outputs `[PASS] No active conflicts, shadowing, or collisions detected in the current environment.` | `0` | **PASS** | `WFC_conflicts_empty` |
| **WFC-02** | Conflict Awareness: Overlapping Persona Co-installation | `unslop` and `hallmark` installed in disposable project | `python D:\skills08\skills08.py conflicts` | Detect aesthetic overlap cluster (`CON-001`) | Outputs `[1] CON-001: Aesthetic Style and Persona Collision (Severity: High)` with clear mitigation advice | `2` | **PASS** | `WFC_conflicts_detected` |
| **WFD-01** | Project-Scope Installation | Disposable project containing `user_code.py` | `python D:\skills08\skills08.py install humanizer` | Atomic install to `.agents/skills/humanizer/`, generate `NOTICE.md`, leave `user_code.py` untouched | Installed `SKILL.md`, `NOTICE.md`, created `skills08.lock.json`; `user_code.py` 100% untouched | `0` | **PASS** | `WFD_install`, `WFD_files` |
| **WFD-02** | Project-Scope Status | 1 skill installed in project scope | `python D:\skills08\skills08.py status` | Show 1 active project skill, unshadowed | Displays tabular status: `humanizer`, scope `project`, 2 files, `Shadowed: No` | `0` | **PASS** | `WFD_status` |
| **WFD-03** | Post-Install Verification | Freshly installed project skill | `python D:\skills08\skills08.py verify` | Verify SHA-256 match for installed files | Verifies `SKILL.md` and `NOTICE.md` match curated hashes; outputs `[PASS]` | `0` | **PASS** | `WFD_verify` |
| **WFE-01** | Global-Scope Behavior | Disposable environment evaluation | Evaluated CLI redirection parameters | Safe redirection to isolated test home | **BLOCKED**: The CLI lacks `--global-root` or `--home` redirection flags. Invoking `--scope global` directly targets the user's host `~/.gemini/config/skills`. Testing against live user directories is prohibited by Rule 3.5. | N/A | **BLOCKED** | `WFE_global_status` |
| **WFF-01** | Integrity Verification: Clean Baseline | Clean installation of `humanizer` | `python D:\skills08\skills08.py verify` | All files match | Reports `2/2 files verified identical. [PASS]` | `0` | **PASS** | `WFF_verify_clean` |
| **WFF-02** | Integrity Verification: Modified File | Tampered `SKILL.md` (appended line) | `python D:\skills08\skills08.py verify` | Detect bit-level drift, report hash mismatch | Reports `[MODIFIED] SKILL.md (Hash mismatch: ...)`, summary `1/2 files verified`, exit code 3 | `3` | **PASS** | `WFF_verify_modified` |
| **WFF-03** | Integrity Verification: Missing File | Deleted `NOTICE.md` | `python D:\skills08\skills08.py verify` | Detect missing asset | Reports `[MISSING] NOTICE.md (File is missing from installed directory)`, exit code 3 | `3` | **PASS** | `WFF_verify_missing` |
| **WFF-04** | Integrity Verification: Extra File Injection | Created `rogue_injected.txt` inside skill directory | `python D:\skills08\skills08.py verify` | Detect uncurated extra file | Reports `[EXTRA] rogue_injected.txt (Uncurated extraneous file detected in skill directory)`, exit code 3 | `3` | **PASS** | `WFF_verify_extra` |
| **WFF-05** | Integrity Verification: Targeted Skill | Specific skill name argument | `python D:\skills08\skills08.py verify humanizer` | Verify specified skill only | Scopes verification to `humanizer [project]` | `3` | **PASS** | `WFF_verify_specific` |
| **WFG-01** | Uninstallation: Clean Removal | Installed skill and unrelated `keep_me.txt` | `python D:\skills08\skills08.py uninstall humanizer` | Remove skill directory, update lockfile, leave `keep_me.txt` intact | Skill folder deleted, lockfile updated, `keep_me.txt` preserved | `0` | **PASS** | `WFG_uninstall`, `WFG_files_after` |
| **WFG-02** | Uninstallation: Repeated Execution | Already uninstalled skill | `python D:\skills08\skills08.py uninstall humanizer` | Graceful failure message | Reports `[FAILED] Skill 'humanizer' is not installed in project scope...`, exit code 1 | `1` | **PASS** | `WFG_uninstall_repeat` |
| **WFG-03** | Uninstallation: Traversal Rejection | Malicious path argument | `python D:\skills08\skills08.py uninstall ../../escape` | Security violation rejection | Reports `[FAILED] Security violation: path traversal detected...`, exit code 1 | `1` | **PASS** | `WFG_uninstall_traversal` |
| **WFG-04** | Uninstallation: Root Defense | Empty name argument | `python D:\skills08\skills08.py uninstall ""` | Security violation rejection | Reports `[FAILED] Security violation: invalid skill name for uninstallation.`, skills root protected | `1` | **PASS** | `WFG_uninstall_empty` |
| **WFH-01** | Failure & Recovery: Unknown Package | Unknown package name | `python D:\skills08\skills08.py install non-existent-skill` | Clear error message | Reports `[FAILED] Candidate 'non-existent-skill' not found in catalog.`, exit code 1 | `1` | **PASS** | `WFH_unknown` |
| **WFH-02** | Failure & Recovery: Deferred Candidate | Group B candidate (`open-pencil`) | `python D:\skills08\skills08.py install open-pencil` | Installation refusal with D7 reason | Reports `[FAILED] Candidate 'open-pencil' (SKILL08-UI-004) is deferred to Group B (v0.2+)...`, exit code 1 | `1` | **PASS** | `WFH_group_b` |
| **WFH-03** | Failure & Recovery: Duplicate Overwrite Protection | Skill already installed | `python D:\skills08\skills08.py install humanizer` | Rejection without `--force` | Reports `[FAILED] Skill 'humanizer' is already installed... Use --force to overwrite.`, exit code 1 | `1` | **PASS** | `WFH_install_duplicate_noforce` |
| **WFH-04** | Failure & Recovery: Force Recovery | Skill already installed | `python D:\skills08\skills08.py install humanizer --force` | Successful overwrite | Overwrites cleanly via atomic staging, updates lock record, exit code 0 | `0` | **PASS** | `WFH_install_duplicate_force` |
| **WFO-01** | Operational Reliability: Whitespace Path | Project path containing spaces (`project with spaces in name`) | `python D:\skills08\skills08.py install humanizer` | Handle spaces cleanly | Installed cleanly, verified with exit code 0 | `0` | **PASS** | `WFO_spaces_install` |
| **WFO-02** | Operational Reliability: PowerShell Wrapper | Native PowerShell execution | `powershell -File D:\skills08\skills08.ps1 install code-simplification` | Wrapper locates python and executes | Clean installation via PowerShell wrapper, exit code 0 | `0` | **PASS** | `WFO_ps_install` |

---

## 2. Workflow Validation Analysis

### 2.1 Workflow Success Rate
- **Total Workflows Formally Evaluated**: 28 distinct test scenarios across Workflows A through H and operational variants.
- **Scenarios Passing**: 27 scenarios (96.4%).
- **Scenarios Blocked**: 1 scenario (Workflow E — Global-Scope CLI Testing, 3.6%).
- **Scenarios Failing**: 0 scenarios (0.0%).

### 2.2 Deep Dive on Blocked Workflow E
- **Technical Barrier**: `src/skills08/cli.py` initializes `Installer()` on line 232 with no arguments. `Installer.__init__` binds `self.global_skills_root` unconditionally to `~/.gemini/config/skills`. The CLI argparse parser has no `--global-root` or `--home` option.
- **Safety Policy Enforcement**: Governance Rule 3.5 forbids mutating live user directories (`C:\Users\athar\.gemini\config\skills`). Under Workflow E's explicit instruction (*"If the application does not support safe redirection, mark the workflow BLOCKED and explain why. Do not modify environment variables globally or alter user settings to force the test."*), the workflow was marked **BLOCKED**.
- **Unit Test Contrast**: In unit testing (`tests/test_installer_lifecycle.py`), programmatic instantiation `Installer(global_root=temp_dir)` works cleanly (PASS). The limitation is strictly confined to the user-facing CLI.

---
*End of Workflow Test Matrix (`validation/phase-1.5/WORKFLOW_TEST_MATRIX.md`).*

