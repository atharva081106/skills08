# Skills08

> **Powering Every AI Agent with Better Skills.**

Skills08 is an open-source, local-first AI agent skill distribution and lifecycle management platform. It provides a curated, verified, and supply-chain-hardened catalog of cognitive skills targeting **Google Antigravity** on Windows and cross-platform environments.

---

## Key Capabilities (Phase 1 Complete)

- **Curated & Audited Catalog**: 12 approved candidate skills across Security, Engineering, Frontend, and Documentation, audited for intellectual property provenance, compatibility, and host safety.
- **Model A Pure-Instruction Standard**: Eliminates process injection, bash stop hook failures, and loopback port zombie daemons on Windows by prioritizing cognitive prompt playbooks over unvetted binary scripts.
- **Dual-Scope Deployment**: Seamless project-level (`.agents/skills/`) and global configuration (`~/.gemini/config/skills/`) deployment with deterministic precedence and shadowing detection.
- **Deterministic Cryptographic Verification**: Every installed skill asset is cryptographically verified against SHA-256 baseline digests (`skills08.lock.json`).
- **Conflict & Collision Prevention**: Built-in static analysis detects cross-repository duplicate names, dual-scope shadowing, and aesthetic persona overlap before collisions occur.
- **Zero External Telemetry & Zero Upstream Execution**: Local-first operation; zero third-party code is executed during cataloging, installation, or verification.

---

## Quickstart

Skills08 provides two native interfaces: a cross-platform Python CLI and a native Windows PowerShell wrapper.

### Windows PowerShell:
```powershell
# Browse candidate catalog
.\skills08.ps1 list

# Inspect candidate metadata, legal clearance, and security guidelines
.\skills08.ps1 inspect security-audit

# Install skill to workspace (.agents/skills/<name>/)
.\skills08.ps1 install humanizer

# Check active skills and detect scope shadowing
.\skills08.ps1 status

# Scan for ecosystem conflicts and aesthetic persona overlaps
.\skills08.ps1 conflicts

# Verify cryptographic integrity of installed skills
.\skills08.ps1 verify

# Cleanly remove an installed skill
.\skills08.ps1 uninstall humanizer
```

### Python CLI (Cross-Platform):
```bash
python skills08.py list
python skills08.py inspect SKILL08-SEC-001
python skills08.py install security-audit --scope project
python skills08.py verify
```

---

## Approved Phase 1 Candidate Catalog (Group A / v0.1)

| Candidate ID | Skill Name | Category | Operational Model | Upstream Author |
| :--- | :--- | :--- | :--- | :--- |
| **SKILL08-SEC-001** | `security-audit` | Security | Companion Guidance Mode | Dan Jones / Cloudflare, Inc. |
| **SKILL08-DOC-001** | `humanizer` | Documentation | Native Pure-Instruction | Siqi Chen |
| **SKILL08-UI-001** | `unslop` | UI/UX & Design | Model A (Instruction-Only) | Damir Sota |
| **SKILL08-UI-002** | `hallmark` | UI/UX & Design | Model A (Instruction-Only) | Hassan El Mghari |
| **SKILL08-FE-001** | `design-taste-frontend` | Frontend Development | Model A (Instruction-Only) | Leonxlnx |
| **SKILL08-SWE-001** | `code-simplification` | Code Quality | Native Pure-Instruction | Addy Osmani |
| **SKILL08-SWE-002** | `simplify-codebase` | Code Quality | Native Pure-Instruction | tt-a1i |
| **SKILL08-TST-001** | `browser-testing-with-devtools` | Testing | Native Subagent Dispatch | Addy Osmani |
| **SKILL08-SWE-003** | `debugging-and-error-recovery` | Engineering | Native Pure-Instruction | Addy Osmani |
| **SKILL08-ARC-001** | `archify` | Architecture | Model A (Instruction-Only) | tt-a1i |
| **SKILL08-FE-002** | `scroll-craft` | Frontend Development | Model A (Instruction-Only) | Nate Herk |
| **SKILL08-UI-003** | `impeccable` | UI/UX & Design | Model A (Instruction-Only) | Paul Bakaus |

*Note: Candidate `SKILL08-UI-004` (`open-pencil`) is deferred to Group B (v0.2+) due to external Bun toolchain and MCP daemon requirements.*

---

## Documentation & Verification Register

- **Phase 1 Master Completion Report**: [`docs/PHASE_1_COMPLETION_REPORT.md`](./docs/PHASE_1_COMPLETION_REPORT.md)
- **System Architecture**: [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md)
- **CLI User Manual & Operational Guide**: [`docs/OPERATIONAL_GUIDE.md`](./docs/OPERATIONAL_GUIDE.md)
- **Testing & Validation Report**: [`docs/TESTING_AND_VALIDATION_REPORT.md`](./docs/TESTING_AND_VALIDATION_REPORT.md) (27/27 Tests Passed)
- **Security & Limitations**: [`docs/SECURITY_AND_LIMITATIONS.md`](./docs/SECURITY_AND_LIMITATIONS.md)
- **Protected-Baseline Integrity Report**: [`docs/PROTECTED_BASELINE_INTEGRITY_REPORT.md`](./docs/PROTECTED_BASELINE_INTEGRITY_REPORT.md) (100% Invariance Certified)
- **Phase 1 Recommendations (D7)**: [`docs/research/PHASE_1_RECOMMENDATIONS.md`](./docs/research/PHASE_1_RECOMMENDATIONS.md)
- **Upstream Research Baselines**:
  - [D1: Source Inventory](./docs/research/SOURCE_INVENTORY.md)
  - [D2: Skills Extraction](./docs/research/SKILLS_EXTRACTION.md)
  - [D3: License Matrix](./docs/research/LICENSE_MATRIX.md)
  - [D4: Compatibility Matrix](./docs/research/COMPATIBILITY_MATRIX.md)
  - [D5: Security Audit](./docs/research/SECURITY_AUDIT.md) & [Correction Report](./docs/research/SECURITY_AUDIT_CORRECTION_REPORT.md)
  - [D6: Conflict Analysis](./docs/research/CONFLICT_ANALYSIS.md) & [Verification Report](./docs/research/D6_FINAL_VERIFICATION_REPORT.md)

---

## Automated Test Suite

Run the full verification test suite directly:
```bash
python tests/run_all_tests.py
```

Results: **27 tests executed, 27 passed (100.0% pass rate), 0 failures, 0 errors**.
