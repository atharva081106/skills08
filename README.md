# Skills08

> **Powering Every AI Coding Agent with Better Skills.**  
> An open-source, local-first AI agent skill distribution, scaffolding, and lifecycle management platform.

[![Tests](https://img.shields.io/badge/tests-50%20passed%20%28100%25%29-brightgreen)](#automated-test-suite)
[![Python](https://img.shields.io/badge/python-3.8%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11%20%7C%20Linux%20%7C%20macOS-lightgrey)](#compatibility)

---

## What is Skills08?

Skills08 is a comprehensive, supply-chain-hardened distribution, authoring, and lifecycle manager for AI agent skills. It enables developers, engineering teams, and coding agents to discover, install, verify, author, and synchronize cognitive skills across their entire stack.

### Universal Coding Agent Support
Skills installed or synchronized with Skills08 are automatically projected into the native configuration formats required by **every major AI coding agent**:

| Coding Agent | Discovery Location | Projection Format |
| :--- | :--- | :--- |
| **Google Antigravity** | `.agents/skills/<name>/` | Native `SKILL.md` with YAML frontmatter |
| **Cursor** | `.cursor/rules/<name>.mdc` & `.cursorrules` | Modern Cursor Rules + `.cursorrules` fallback |
| **Claude Code** | `CLAUDE.md` & `.claude/skills/` | Project instructions block + modular skills mirror |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Workspace custom instructions |
| **Windsurf** | `.windsurfrules` | Cascade agent memory & instructions block |
| **Cline / Roo Code** | `.clinerules` | Extension guidelines and runbook rules |
| **Gemini CLI** | `GEMINI.md` | Gemini Code Assist instructions |
| **Universal Agents** | `AGENTS.md` | Cross-platform agent standard (OpenHands, Devin, etc.) |

---

## Key Capabilities

- **Curated & Audited Catalog**: 12 production-ready skills spanning Security, Code Quality, UI/UX Design, Architecture, and Testing, fully audited for IP provenance, compatibility, and safety.
- **Universal Multi-Agent Sync (`skills08 sync`)**: Automatically bridges installed skills into Cursor, Claude Code, GitHub Copilot, Windsurf, Cline, and Antigravity with safe delimiter protection that preserves your custom developer instructions.
- **Model A Safe-Instruction Standard**: Eliminates process injection, unhandled bash hooks, and zombie daemon ports on Windows by utilizing cognitive prompt instructions and companion guidance mode rather than unvetted binary scripts.
- **Arbitrary Workspace Redirection (`-w` / `--workspace-root`)**: Install, verify, sync, or inspect skills in any target repository from anywhere on your system without changing directories.
- **Global User Scope (`-g` / `--global-root`)**: Deploy user-wide skills with deterministic Antigravity project-scope precedence and shadowing detection.
- **Skill Scaffolding (`skills08 new`)**: Instant scaffolding of compliant custom skills with standard frontmatter, instruction workflows, examples, and reference guides.
- **Packaging & Bundling (`skills08 pack`)**: Validates and packs skill directories into `.tar.gz` distribution archives with SHA-256 cryptographic manifests.
- **Deterministic Cryptographic Verification (`skills08 verify`)**: Verifies installed files against known SHA-256 digests (`skills08.lock.json`) to detect local drift or tampering.
- **Conflict & Shadowing Analysis (`skills08 conflicts`)**: Proactively identifies cross-repository naming collisions, dual-scope shadowing, and aesthetic persona overlap.
- **System Doctor (`skills08 doctor`)**: Self-diagnostics for Python runtimes, PowerShell environments, directory writability, and catalog integrity.
- **Zero Third-Party Runtime Dependencies**: Built entirely using Python's standard library (with pure-Python fallback YAML parsing).

---

## Installation & Setup

### Option 1: Install via Pip (Recommended for Global CLI)
```bash
# Clone the repository
git clone https://github.com/atharva081106/skills08.git
cd skills08

# Install in editable mode (provides 'skills08' command globally)
pip install -e .
```

### Option 2: Windows Native PowerShell (Zero Installation)
```powershell
# Run directly with the included PowerShell wrapper
.\skills08.ps1 doctor
.\skills08.ps1 list
```

### Option 3: Direct Python Runner
```bash
python skills08.py list
```

---

## CLI Command Reference

| Command | Arguments / Flags | Description |
| :--- | :--- | :--- |
| **`list`** | `[-c CAT] [-t TIER] [--json]` | List all candidate skills in the catalog with status and clearance. |
| **`search`** | `<query> [-c CAT] [-t TIER] [--json]` | Search catalog by keyword, name, description, category, or tier. |
| **`inspect`** / **`info`** | `<identifier> [--json]` | View detailed metadata, upstream commit SHA, author, and security rules. |
| **`install`** | `<name> [--scope project\|global] [-f] [-s] [-w PATH] [-g PATH]` | Atomically install a skill into workspace or global scope. |
| **`uninstall`** | `<name> [--scope project\|global] [-w PATH] [-g PATH]` | Cleanly remove an installed skill and update the lock registry. |
| **`update`** | `[name] [--scope project\|global] [-w PATH]` | Refresh and re-verify installed skill(s) against the latest catalog. |
| **`sync`** | `[-a AGENTS] [-w PATH] [--json]` | Synchronize active skills across Cursor, Claude, Copilot, Windsurf, Cline, and Gemini. |
| **`status`** | `[--scope project\|global] [--json] [-w PATH]` | Show active skills, file counts, and shadowing across scopes. |
| **`conflicts`** | `[--scope project\|global] [--json] [-w PATH]` | Scan environment for lexical collisions, shadowing, and persona overlap. |
| **`verify`** | `[name] [--scope project\|global] [-V] [--json] [-w PATH]` | Cryptographically verify SHA-256 file hashes of installed skills. |
| **`new`** | `<name> [-d DESC] [-c CAT] [-a AUTHOR] [-t PATH]` | Scaffold a new compliant agent skill template directory with `SKILL.md`. |
| **`pack`** | `<directory> [-o OUT_DIR] [-n NAME] [--json]` | Validate a skill directory and package into a `.tar.gz` bundle with checksum. |
| **`doctor`** | `[-w PATH] [-g PATH] [--json]` | Run comprehensive diagnostics on Python, shell, paths, and catalog. |
| **`agent-init`** | `[-t TARGET_DIR] [-a AGENTS] [--json]` | Initialize workspace with multi-agent configuration and discovery structure. |

---

## Quickstart Tutorial

### 1. Initialize a Project for Coding Agents
```bash
skills08 agent-init -w "D:\Projects\MyApp"
```

### 2. Search and Install Skills
```bash
# Search for design or security skills
skills08 search "security"
skills08 search "frontend"

# Install into your project workspace
skills08 install security-audit -w "D:\Projects\MyApp"
skills08 install code-simplification -w "D:\Projects\MyApp"
```

### 3. Verify Active Skills
```bash
skills08 status -w "D:\Projects\MyApp"
skills08 verify -w "D:\Projects\MyApp"
```

### 4. Author a Custom Skill for Your Team
```bash
skills08 new api-design-guidelines \
  -d "Enforces RESTful API conventions and OpenAPI 3.1 schemas" \
  -c "Architecture" \
  -w "D:\Projects\MyApp"
```

---

## Approved Skills Catalog (Group A / v0.1)

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

## Automated Test Suite

Skills08 includes a comprehensive automated regression, security, lifecycle, and compatibility test suite.

```bash
python tests/run_all_tests.py
```

### Verified Test Results:
- **Total Tests Run**: 50
- **Passed**: 50 (100.0%)
- **Failures / Errors**: 0
- **Test Modules**:
  1. `test_manifest.py`: Manifest schema, 13 candidate constraints, provenance commit SHAs.
  2. `test_catalog_and_packages.py`: Package completeness, companion markdown preservation, script omission.
  3. `test_conflicts.py`: Cross-repository collisions, scope shadowing, aesthetic overlap detection.
  4. `test_installer_lifecycle.py`: Atomic installation, force overwrites, path traversal defenses, junction/symlink security.
  5. `test_verifier_integrity.py`: SHA-256 detection of modified, extra, or missing assets.
  6. `test_security_and_secrets.py`: Zero credentials, zero third-party runtime dependencies, zero arbitrary `eval`/`exec`.
  7. `test_windows_compatibility.py`: Spaces, Unicode paths, normalized slash separators, exit codes.
  8. `test_protected_baselines.py`: Invariant verification of all research baselines and 19 locked git checkouts.
  9. `test_full_fledged_features.py`: Redirection flags (`-w`, `-g`), search, scaffolding, packaging, doctor, update, and JSON outputs.

---

## Documentation & Evidence Register

- **Phase 1 Master Completion Report**: [`docs/PHASE_1_COMPLETION_REPORT.md`](./docs/PHASE_1_COMPLETION_REPORT.md)
- **Phase 1.5 Validation Report**: [`validation/phase-1.5/PRODUCT_VALIDATION_REPORT.md`](./validation/phase-1.5/PRODUCT_VALIDATION_REPORT.md)
- **Findings Register**: [`validation/phase-1.5/FINDINGS_REGISTER.md`](./validation/phase-1.5/FINDINGS_REGISTER.md)
- **System Architecture**: [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md)
- **CLI User Manual**: [`docs/OPERATIONAL_GUIDE.md`](./docs/OPERATIONAL_GUIDE.md)
- **Security & Limitations**: [`docs/SECURITY_AND_LIMITATIONS.md`](./docs/SECURITY_AND_LIMITATIONS.md)
- **Research Baselines**:
  - [D1: Source Inventory](./docs/research/SOURCE_INVENTORY.md)
  - [D2: Skills Extraction](./docs/research/SKILLS_EXTRACTION.md)
  - [D3: License Matrix](./docs/research/LICENSE_MATRIX.md)
  - [D4: Compatibility Matrix](./docs/research/COMPATIBILITY_MATRIX.md)
  - [D5: Security Audit](./docs/research/SECURITY_AUDIT.md) & [Correction Report](./docs/research/SECURITY_AUDIT_CORRECTION_REPORT.md)
  - [D6: Conflict Analysis](./docs/research/CONFLICT_ANALYSIS.md) & [Verification Report](./docs/research/D6_FINAL_VERIFICATION_REPORT.md)
  - [D7: Phase 1 Recommendations](./docs/research/PHASE_1_RECOMMENDATIONS.md)

---

## License

Distributed under the MIT License. See [`LICENSE`](./LICENSE) for details.
Original upstream skills retain the copyrights of their respective authors as documented in each package's `NOTICE.md`.
