# Skills08 — Operational Guide & CLI User Manual

> **Document Status**: Complete & Authoritative  
> **Milestone**: Phase 1 Completion — User Documentation & Operational Manual  
> **Target Host Platform**: Google Antigravity (Local-First AI Agent Distribution Platform)  
> **Operating Environment**: Windows 10/11 x64 (PowerShell 5.1 / PowerShell 7+) & Cross-Platform POSIX  

---

## 1. Overview

**Skills08** provides a lightweight, local-first lifecycle manager for installing, inspecting, verifying, and managing AI agent skills. Designed specifically for **Google Antigravity**, Skills08 eliminates manual copying, tracks dependencies, prevents collisions, enforces security boundaries, and cryptographically guarantees supply chain integrity.

Skills08 provides two native interfaces:
- **`python skills08.py <command>`**: Cross-platform Python CLI (Python 3.10+, zero external dependencies).
- **`.\skills08.ps1 <command>`**: Native Windows PowerShell wrapper for idiomatic command execution.

---

## 2. Command Reference

### 2.1 `list` — Browse Catalog
List all candidates in the Skills08 catalog, their categories, legal tiers, operational models, and installation status.

```powershell
.\skills08.ps1 list
# or
python skills08.py list
```

**Example Output**:
```
=== Skills08 Phase 1 Candidate Catalog ===

Candidate ID    | Skill Name                    | Category                            | Tier             | Operational Model                   | Installed
----------------+-------------------------------+-------------------------------------+------------------+-------------------------------------+----------
SKILL08-SEC-001 | security-audit                | Security                            | Group A (v0.1)   | Companion-File Guidance Mode        | No       
SKILL08-DOC-001 | humanizer                     | Documentation and Technical Writing | Group A (v0.1)   | Native Pure-Instruction             | No       
SKILL08-UI-001  | unslop                        | UI/UX and Design Systems            | Group A (v0.1)   | Model A (Instruction-Only)          | No       
SKILL08-UI-002  | hallmark                      | UI/UX and Design Systems            | Group A (v0.1)   | Model A (Instruction-Only)          | No       
SKILL08-FE-001  | design-taste-frontend         | Frontend Development                | Group A (v0.1)   | Model A (Instruction-Only)          | No       
SKILL08-SWE-001 | code-simplification           | Code Quality and Review             | Group A (v0.1)   | Native Pure-Instruction             | No       
SKILL08-SWE-002 | simplify-codebase             | Code Quality and Review             | Group A (v0.1)   | Native Pure-Instruction             | No       
SKILL08-TST-001 | browser-testing-with-devtools | Testing and Browser Automation      | Group A (v0.1)   | Native Subagent Dispatch            | No       
SKILL08-SWE-003 | debugging-and-error-recovery  | Software Engineering                | Group A (v0.1)   | Native Pure-Instruction             | No       
SKILL08-ARC-001 | archify                       | Architecture and System Design      | Group A (v0.1)   | Model A (Instruction-Only)          | No       
SKILL08-FE-002  | scroll-craft                  | Frontend Development                | Group A (v0.1)   | Model A (Instruction-Only)          | No       
SKILL08-UI-003  | impeccable                    | UI/UX and Design Systems            | Group A (v0.1)   | Model A (Instruction-Only)          | No       
SKILL08-UI-004  | open-pencil                   | UI/UX and Design Systems            | Group B (Future) | Deferred External Runtime (Group B) | No       

Total Candidates: 13 (12 Approved Group A, 1 Deferred Group B)
```

---

### 2.2 `inspect` — View Candidate Details
Examine deep metadata, author provenance, locked upstream commit SHA, license clearance, operational models, and security guidelines.

```powershell
.\skills08.ps1 inspect SKILL08-SEC-001
# or by name:
.\skills08.ps1 inspect security-audit
```

**Output Fields**:
- **Candidate ID & Name**: Unique identifier and canonical directory name.
- **Display Name & Category**: Human-readable title and domain.
- **Operational Model**: Execution tier (Native, Model A, Companion Guidance, Subagent Dispatch).
- **Legal Clearance**: License tier and copyright obligations.
- **Upstream Provenance**: Repository URL and exact locked 40-character commit SHA.
- **Security Guidelines**: D5 security audit constraints (e.g. Guidance Mode enforcement).
- **Adaptation Requirements**: D4/D7 packaging transformations applied.

---

### 2.3 `install` — Deploy Skill Package
Atomically deploy a curated skill package into the active workspace or global configuration.

```powershell
# Install to workspace project scope (.agents/skills/<name>/) [Default]
.\skills08.ps1 install humanizer

# Install to global user scope (~/.gemini/config/skills/<name>/)
.\skills08.ps1 install humanizer --scope global

# Force overwrite existing installation
.\skills08.ps1 install humanizer --force
```

**Safety Guarantees**:
- **Atomic Staging**: Package files are extracted to a temporary staging folder before atomic rename into place, preventing corrupt or half-written skills.
- **Path Traversal Defense**: All destination paths are verified to reside strictly within `.agents/skills/` or `~/.gemini/config/skills/`.
- **Automatic Attribution**: Generates a standard `NOTICE.md` containing upstream provenance and licensing terms in the installed directory.
- **Integrity Lock Record**: Automatically records file sizes and SHA-256 hashes in `skills08.lock.json`.
- **Group B Rejection**: Refuses to install deferred candidates (`open-pencil`) in v0.1.

---

### 2.4 `uninstall` — Clean Skill Removal
Safely remove an installed skill from the project or global scope without touching adjacent project files.

```powershell
# Remove from project scope
.\skills08.ps1 uninstall humanizer

# Remove from global scope
.\skills08.ps1 uninstall humanizer --scope global
```

---

### 2.5 `status` — Inspect Environment
Display installed skills across both project and global scopes, count files, and detect scope shadowing.

```powershell
.\skills08.ps1 status
```

**Example Output**:
```
=== Skills08 Workspace & Global Status ===

Workspace Root:       D:\skills08
Project Scope Path:   D:\skills08\.agents\skills
Global Scope Path:    C:\Users\athar\.gemini\config\skills

Skill Name  | Scope   | Files | Shadowed | Path                                
------------+---------+-------+----------+-------------------------------------
humanizer   | project | 2     | No       | D:\skills08\.agents\skills\humanizer

Total Active Skills: 1
```

---

### 2.6 `conflicts` — Scan Ecosystem Interactions
Run a static scan of the active environment to identify potential conflicts, collisions, and shadowing.

```powershell
.\skills08.ps1 conflicts
```

**Evaluated Conditions**:
1. **Dual-Scope Shadowing (`CON-005`)**: Flags when a project skill overrides a global skill of identical name.
2. **Cross-Repository Lexical Collisions (`CON-011`)**: Alerts if unnamespaced packages collide with the 5 known multi-repo duplicate names (`architecture-decision-records`, `design-taste-frontend`, `frontend-slides`, `hallmark`, `hyperframes`).
3. **Aesthetic Persona Overlap (`CON-001`)**: Emits advisory recommendations if multiple design skills (`unslop`, `hallmark`, `design-taste-frontend`, `impeccable`) are co-installed, suggesting workflow-phase scoping per D7 `REC-SYS-006`.

---

### 2.7 `verify` — Cryptographic Integrity Audit
Audit installed skills against the curated package catalog to verify that files have not been modified, corrupted, or injected with uncurated content.

```powershell
.\skills08.ps1 verify
```

**Status Indicators**:
- `[PASS]`: File matches curated baseline SHA-256 digest exactly.
- `[MODIFIED]`: File content has drifted from the curated baseline.
- `[MISSING]`: A required skill file has been deleted.
- `[EXTRA]`: An unexpected or unauthorized file was added to the skill folder.

---

## 3. Recommended Workflows

### 3.1 Standard Web Development Setup
For a clean, high-velocity frontend engineering workspace:
```powershell
# 1. Prose refinement
.\skills08.ps1 install humanizer

# 2. Code simplification heuristics
.\skills08.ps1 install code-simplification

# 3. Automated browser testing via Antigravity browser subagent
.\skills08.ps1 install browser-testing-with-devtools

# 4. Systematic debugging methodology
.\skills08.ps1 install debugging-and-error-recovery

# 5. Verify integrity
.\skills08.ps1 verify
```

### 3.2 Security Audit Guidance Workflow (`security-audit`)
1. Install `security-audit`:
   ```powershell
   .\skills08.ps1 install security-audit
   ```
2. The skill operates in **Guidance Mode** on Windows:
   - Dynamic target code execution and test runner invocations are disabled.
   - The agent uses Antigravity's read-only `research` subagent to analyze static source trees.
   - Dynamic validation checks are emitted to `NEEDS-VALIDATION.md` for manual execution in an external sandbox.

### 3.3 Managing Frontend Design Personas
When elevating UI quality, install design skills based on your project phase:
- **Design System Formulation**: Use `design-taste-frontend` to formulate Tailwind tokens and typography scales.
- **Component Construction**: Use `hallmark` for pixel-level micro-polish and responsive states.
- **Pre-Commit Code Review**: Use `unslop` to strip generic AI gradients and tropes.
- **Holistic UX Direction**: Use `impeccable` to guide user flow, copywriting, and emotional resonance.

---

## 4. Exit Codes & Scripting

The Skills08 CLI returns deterministic exit codes suitable for automated CI/CD pipelines and pre-commit hooks:

| Exit Code | Constant | Meaning |
| :---: | :--- | :--- |
| **0** | `EXIT_SUCCESS` | Command completed successfully. |
| **1** | `EXIT_ERROR` | General operational error (missing candidate, path error, invalid arguments). |
| **2** | `EXIT_CONFLICT` | Conflict scan detected active ecosystem issues or shadowing. |
| **3** | `EXIT_VERIFICATION_FAILED` | Integrity verification detected modified, missing, or extra files. |

---
*End of Operational Guide (`docs/OPERATIONAL_GUIDE.md`).*

