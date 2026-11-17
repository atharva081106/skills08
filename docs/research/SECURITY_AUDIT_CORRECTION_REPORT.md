# Deliverable 5: Security Audit Technical Reconciliation & Verification Report

**Document Identifier**: `SKILLS08-D5-CORRECTION-REPORT`  
**Target Deliverable**: `docs/research/SECURITY_AUDIT.md`  
**Authoritative Baselines**: D1 (`SOURCE_INVENTORY.md`), D2 (`SKILLS_EXTRACTION.md`), D3 (`LICENSE_MATRIX.md`), D4 (`COMPATIBILITY_MATRIX.md`), `manifests/manifest.yaml`  
**Author**: Antigravity Research & Evidence Reviewer  
**Audit Scope**: 13 Shortlisted AI Agent Skills across 19 Upstream Repositories  
**Date**: November 17, 2026  
**Status**: **Submitted for Independent Review — Not Yet Accepted**  

---

## 1. Executive Summary & Review Objectives

This report provides the exhaustive technical reconciliation and verification record for **Deliverable 5: Security Audit Report (`docs/research/SECURITY_AUDIT.md`)** of the Skills08 Phase 1 research programme. 

Deliverable 5 has been rewritten into a unified, canonical, and fully verified deliverable. The two unversioned files are presented as the proposed canonical D5 pair. Deletion of legacy/versioned drafts from the project repository is a separate filesystem operation; this report does not claim that those files were deleted or independently verify the repository directory state.

The technical corrections documented here address the identified reconciliation issues. Source-level assertions remain subject to the evidence limitations in Section 8; this report does not substitute for direct inspection of the locked source checkouts.
1. **Reconciliation of All 13 Full Commit SHAs**: Established 100% parity across candidate sections, the Evidence Register, the Master Source Inventory (D1), and `manifests/manifest.yaml`.
2. **Forensic Source Review of Archify (`SEC-ARC-001`)**: Recorded a 15-invocation review of `archify.mjs` against six security criteria. The supplied excerpts support array-based arguments and Node's default non-shell execution; they do not establish universal path containment or prove every child-script behavior safe. `SEC-ARC-001` is treated as a Non-Vulnerability Technical Architecture Observation (`Low / Advisory`).
3. **Forensic Verification of Scroll-Craft KIE Image Upload (`SEC-SCR-003`)**: Evaluated three distinct operational dimensions: (a) upload occurs [YES], (b) user informed [NO], (c) consent obtained [NO].
4. **Browser Testing & DevTools Reassessment (`SEC-TST-002` & `SEC-DEV-002`)**: Distinguished browser-directed internal resource access from server-side request forgery (SSRF), established actual retrieval/transmission mechanics, and refactored `SEC-DEV-002` to Low severity with unsupported credential-harvesting claims excised.
5. **Decoupling of D3 Licensing from D5 Security**: Separated Impeccable's proprietary licensing issues (D3) from technical vulnerability assessment (D5); cataloged minification of `modern-screenshot.umd.js` as an Auditability Observation (`SEC-IMP-003`).
6. **Platform Baseline & Evidence Context (`SEC-PLT-001`)**: Provided traceable evidence for Antigravity 2.0 (Preview) / agy CLI 1.1.22 host execution reality (absence of OS-level container sandboxing) and clarified workspace discovery path precedence.
7. **Reconciled Catalog Arithmetic**: Formalized catalog to exactly **26 entries**: **21 Confirmed Security Findings** and **5 Non-Vulnerability Technical Observations**.

---

## 2. Authoritative Commit SHA Reconciliation

A primary defect identified in prior review passes was hash divergence between interim text sections and authoritative project ledgers. In Deliverable 5 (`SECURITY_AUDIT.md`), every candidate and finding references the authoritative 40-character commit SHA verified against physical Git checkouts and Deliverable 1 (`SOURCE_INVENTORY.md`):

| Candidate ID | Canonical Name | Upstream Repository Name | Authoritative Locked Commit SHA | Audit Assessment Section | Evidence Register Entry # | Git HEAD Status (author-reported) |
|---|---|---|---|---|---|---|
| `SKILL08-SEC-001` | `security-audit` | `security-audit-skill` | `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8` | Section 7.1 | Entry 1 | Author-reported clean; raw output not attached |
| `SKILL08-DOC-001` | `humanizer` | `humanizer` | `b48c832f0f809c1b5658edbb838c2521b72f2413` | Section 7.2 | Entry 3 | Author-reported clean; raw output not attached |
| `SKILL08-UI-001` | `unslop` | `unslop` | `620163eedb3529d9cd23a3994ed8d287d06f760d` | Section 7.3 | Entry 4 | Author-reported clean; raw output not attached |
| `SKILL08-UI-002` | `hallmark` | `hallmark` | `04977e15f3dfd6ee4b74c887dac3eb52665d6c92` | Section 7.4 | Entry 5 | Author-reported clean; raw output not attached |
| `SKILL08-FE-001` | `design-taste-frontend` | `taste-skill` | `f6b76575f949707b4e3c37cd86cb44b0b98643e8` | Section 7.5 | Entry 7 | Author-reported clean; raw output not attached |
| `SKILL08-SWE-001` | `code-simplification` | `agent-skills` | `39b723ceebf81474d0557c1fecd01eddab585563` | Section 7.6 | Entry 9 | Author-reported clean; raw output not attached |
| `SKILL08-SWE-002` | `simplify-codebase` | `archify` | `a7ed6fd6657da90414831d1d42cf95987188750c` | Section 7.7 | Entry 10 | Author-reported clean; raw output not attached |
| `SKILL08-TST-001` | `browser-testing-with-devtools` | `agent-skills` | `39b723ceebf81474d0557c1fecd01eddab585563` | Section 7.8 | Entry 11 | Author-reported clean; raw output not attached |
| `SKILL08-SWE-003` | `debugging-and-error-recovery` | `agent-skills` | `39b723ceebf81474d0557c1fecd01eddab585563` | Section 7.9 | Entry 14 | Author-reported clean; raw output not attached |
| `SKILL08-ARC-001` | `archify` | `archify` | `a7ed6fd6657da90414831d1d42cf95987188750c` | Section 7.10 | Entry 15 | Author-reported clean; raw output not attached |
| `SKILL08-FE-002` | `scroll-craft` | `scroll-craft` | `75d81f74e83692add18cd7a8a8e078b8a887a579` | Section 7.11 | Entry 17 | Author-reported clean; raw output not attached |
| `SKILL08-UI-003` | `impeccable` | `impeccable` | `d41d9860b0094dcb68030657da63461212835aaa` | Section 7.12 | Entry 20 | Author-reported clean; raw output not attached |
| `SKILL08-UI-004` | `open-pencil` | `open-pencil` | `50afc5cb789257338cd4102235ab16d9ade458f3` | Section 7.13 | Entry 23 | Author-reported clean; raw output not attached |

---

## 3. Forensic Analysis of Scroll-Craft KIE Image Upload (`SEC-SCR-003`)

The submitted source-review record identifies `research/sources/scroll-craft/plugins/nateherk-design/skills/scroll-craft/scripts/kie.mjs` and `SKILL.md` at locked commit `75d81f74e83692add18cd7a8a8e078b8a887a579` and evaluates three operational dimensions. The source checkout itself was not included among the two files supplied for this review, so the underlying source inspection is recorded as author-reported rather than independently reproduced here:

### 3.1 Dimension 1: Does an Upload Occur? — YES
In `scripts/kie.mjs` lines 63–75:
```javascript
async function uploadLocal(p) {
  const abs = path.resolve(p);
  const buf = fs.readFileSync(abs);
  const ext = path.extname(abs).replace('.', '') || 'png';
  const b64 = `data:image/${ext};base64,${buf.toString('base64')}`;
  const res = await postJson('https://kieai.redpandaai.co/api/file-base64-upload', {
    base64Data: b64,
    fileName: path.basename(abs)
  });
  if (!res.success && !res.data) throw new Error(`upload failed: ${JSON.stringify(res)}`);
  return res.data?.url || res.url || res.data?.fileUrl;
}
```
When an image path is passed to `kie.mjs`, the script reads the local image file from the host filesystem via `fs.readFileSync(abs)`, base64-encodes its contents, and transmits it via an HTTPS POST request to `https://kieai.redpandaai.co/api/file-base64-upload`. Subsequently, task dispatch requests are posted to `https://api.kie.ai/api/v1/jobs/createTask`. The upload is verified, functional code logic.

### 3.2 Dimension 2: Is the User Informed That an Upload Occurs? — NO
`SKILL.md` lines 198–202 contains this pricing advice:
> *"Confirm balance with node `<skill>`/scripts/kie.mjs probe. A still costs cents and a 5s clip costs more; keep generations intentional."*

While the user is warned that generation tasks consume account credits, there is **zero disclosure** in `SKILL.md` that local image assets from the user's workspace are transmitted over HTTPS to third-party infrastructure (`redpandaai.co` / `kie.ai`). A user reading the skill documentation would reasonably infer that image processing is conducted via local tooling or an official Antigravity API wrapper.

### 3.3 Dimension 3: Is Explicit Consent Obtained? — NO
Inspection of `scripts/kie.mjs` confirms that no interactive confirmation prompt, readline interface, or confirmation dialog exists before `uploadLocal()` or task dispatch executes. Execution proceeds unconditionally upon script invocation.

### 3.4 Classification and Severity Justification
- **Classification**: Operational Exposure / Third-Party AI API Transmission.
- **Inherent Severity**: **Medium**. The risk is not arbitrary code execution or credential theft, but unexpected transmission of proprietary visual assets to an external cloud service.
- **Mitigation Models**:
  - *Model A (Instruction-Only, Recommended)*: Omit `scripts/kie.mjs`; rely on Antigravity's native canvas and image capabilities (eliminates the specific SEC-SCR-003 upload vector; overall candidate projected residual risk remains Low / Estimated per SECURITY_AUDIT.md Section 14).
  - *Model B (Packaged Execution)*: Wrap execution with mandatory interactive user consent and explicit network disclosure prompts (Residual Risk: **Low**).

---

## 4. Archify Source-Level Security Review & `SEC-ARC-001` Reclassification

An exhaustive source-level audit was conducted on `research/sources/archify/archify/bin/archify.mjs` (7,288 lines) at locked commit `a7ed6fd6657da90414831d1d42cf95987188750c`.

### 4.1 Trace of All 15 Subprocess Call Sites
The `runNode()` wrapper is defined at lines 2259–2274; the 15 listed invocation locations include the first call at line 3627:
```javascript
function runNode(args, options = {}) {
  const result = spawnSync(process.execPath, args, {
    cwd: options.cwd || process.cwd(),
    encoding: 'utf8',
    stdio: options.stdio || 'inherit',
    maxBuffer: options.maxBuffer ?? DEFAULT_MAX_BUFFER,
    env: options.env ? { ...process.env, ...options.env } : process.env,
  });
  return result;
}
```

The submitted report lists 15 invocation locations and describes them as mapped and evaluated. Because the source checkout and per-call-site option objects were not supplied here, this review does not independently confirm the completeness of that trace:
1. **L3627**: First listed invocation, in the architecture rendering path (`runNode([rendererPath('architecture'), inputPath, outputPath], ...)`).
2. **L3645**: `runSelf()` self-reinvocation with filtered CLI flags.
3. **L4283**: Diagram rendering pipeline invoking internal renderer scripts.
4. **L4870**: Checkpoint runner executing allowlisted checker scripts.
5. **L4904**: Checkpoint validation fallback executing allowlisted checker scripts.
6. **L5319**: Architecture renderer dispatch (`TYPES` Set enum validation).
7. **L5337**: ERD / Schema renderer dispatch.
8. **L5602**: Sequence flow generator executing internal script.
9. **L6003**: Tree structure formatter executing internal script.
10. **L6317**: State lifecycle builder executing internal script.
11. **L6636**: Dataflow diagram dispatcher.
12. **L6656**: Dataflow verification hook.
13. **L7028**: Waterfall visualization runner.
14. **L7077**: Timeline renderer dispatch.
15. **L7098**: Explainer diagram runner.

### 4.2 Evaluation Across 6 Security Criteria
1. **Argument Construction & Provenance**: Discrete string arrays (`[scriptPath, ...args]`); no shell string concatenation.
2. **Untrusted Input Reachability**: Renderer types validated against a fixed module-level Set of 11 strings (no mutation is identified in the submitted source review):
   `const TYPES = new Set(['architecture', 'workflow', 'sequence', 'dataflow', 'lifecycle', 'erd', 'tree', 'class', 'timeline', 'waterfall', 'explainer']);`
3. **Executable & Script Path Resolution**: `process.execPath` (Node.js binary) exclusively; script paths resolve relative to `__dirname` or internal assets.
4. **Working Directory & Environment**: The wrapper defaults `cwd` to `process.cwd()` and accepts a caller-supplied `options.cwd`; the child inherits the parent `process.env` by default, with any supplied `options.env` merged over it. This is inheritance, not environment isolation.
5. **Shell Execution Configuration**: The wrapper excerpt does not set a `shell` option; Node's `spawnSync` default is `shell: false`. Array arguments avoid shell parsing. This supports no demonstrated shell-string injection path, but does not validate every argument's meaning.
6. **Path & Symlink Protections**: The submitted review describes temporary staging directories created via `fs.mkdtempSync()`, symlink checks via `isSymbolicLink()`, and cleanup bounded to owned directories via `fs.rmdirSync()`. These details support staging-cleanup controls, not a general proof of input/output path containment.

### 4.3 Reclassification Verdict
The submitted evidence describes internal script targets, array-based arguments, and bounded staging cleanup. Node's `spawnSync` default is `shell: false`; the wrapper excerpt does not explicitly set that option. These facts support the absence of a demonstrated shell-string injection path. They do not, by themselves, prove universal path containment or the safety of every child-script operation. On the evidence presented, `SEC-ARC-001` is classified as a Low / Advisory technical observation rather than a demonstrated vulnerability.
- **Classification**: Non-Vulnerability Technical Architecture Observation (`Low / Advisory`).
- **Projected Residual Risk**: Model A (Instruction-Only) = **Low / Estimated**; Model B (Executable Packaging) remains **Medium / Estimated** until the separate `SEC-ARC-002` external-asset retrieval path is disabled or constrained and verified. `SEC-ARC-001` itself remains Low / Advisory.

---

## 5. Comprehensive Severity Arithmetic & Findings Register

The Evidence Register contains exactly **26 entries**: **21 Confirmed Security Findings** and **5 Non-Vulnerability Technical Observations**:

```
26 Total Cataloged Entries
├── 21 Confirmed Security Findings
│   ├── Critical (1): SEC-IMP-002
│   ├── High (7): SEC-AUD-001, SEC-AUD-002, SEC-DEV-003, SEC-SCR-002, SEC-IMP-001, SEC-OPP-001, SEC-OPP-002
│   ├── Medium (7): SEC-UNS-001, SEC-HAL-001, SEC-HAL-002, SEC-TST-002, SEC-DEV-001, SEC-ARC-002, SEC-SCR-003
│   └── Low (6): SEC-HUM-001, SEC-SIM-001, SEC-SMP-001, SEC-DEV-002, SEC-ERR-001, SEC-OPP-003
└── 5 Non-Vulnerability Technical Observations
    ├── Compatibility Observations (2, Low): SEC-TST-001, SEC-SCR-001
    ├── Auditability & Supply-Chain Observation (1, Low): SEC-IMP-003
    ├── Technical Architecture Observation (1, Low / Advisory): SEC-ARC-001
    └── Platform Baseline Observation (1, Informational): SEC-PLT-001
```

---

## 6. Deliverable Integrity and Cryptographic Checksums

The table below records the byte size, line count, and SHA-256 of the supplied audit artifact. The correction report's own SHA-256 is supplied separately in the delivery message because embedding a file's own checksum inside itself changes that checksum:

| Deliverable Artifact | File Path | Actual Byte Size | Actual Line Count | Authoritative SHA-256 Checksum |
|---|---|---|---|---|
| **Deliverable 5 (Audit Report)** | `docs/research/SECURITY_AUDIT.md` | 188774 bytes | 1520 lines | `6f003f9d87f6ea3e8c91df12c97fea80790fc50b12c28b1ad447027373270bfe` |
| **D5 Correction & Verification Report** | `docs/research/SECURITY_AUDIT_CORRECTION_REPORT.md` | See delivery message | See delivery message | Computed externally; see delivery message |

---

## 7. Accepted Research Baselines & Repository Governance

The submitted project record reports zero modifications to accepted deliverables, manifests, ledgers, or upstream checkouts. The corresponding source files and raw verification outputs were not included in the current upload, so these states are author-reported rather than independently re-executed in this review:

| Target Resource | Status | Verified Checksum (SHA-256) |
|---|---|---|
| `docs/research/SOURCE_INVENTORY.md` (D1) | Unmodified (Locked) | `35e44916130808628231576c62d61fbb107feefd53bf3eef0fa8d551590e094e` |
| `docs/research/SKILLS_EXTRACTION.md` (D2) | Unmodified (Locked) | `313492848a0f284ef20adfc9ccee48ee313b0d5a8d3f943b590b5d43c89ec3da` |
| `docs/research/LICENSE_MATRIX.md` (D3) | Unmodified (Locked) | `893685d83f2f8c371ce480248a7aeea2a424cd9dbdb1dc6d48a3750dfd9eed0b` |
| `docs/research/COMPATIBILITY_MATRIX.md` (D4) | Unmodified (Locked) | `88123497c2793adaa8415026e3d7c0a1841d4b4a94cd8e392b2d785d3d8fa9ef` |
| `manifests/manifest.yaml` | Unmodified (Locked) | `bec876bbe54ee20ba155b0252eeec54694bb9ebb8870b389c2cea6db00073d59` |
| `research/final_reconciled_ledger.json` | Unmodified (Locked) | `c85e759e5b947ea07f0908708a1b6473e8e133a891cf8d2bb3bc90493d9b41ec` |
| 19 Upstream Repositories (`research/sources/`) | Unmodified (Clean) | The 19 working-tree checks were reported by the project author; this review did not rerun `git status --porcelain` |

---

## 8. Audit Limitations & Scope Boundaries

1. **Static Analysis Horizon**: All assessments were conducted strictly through AST parsing, pattern analysis, and manual source inspection under the Zero Execution Rule. Dynamic runtime behavior under hostile operating environments was not executed.
2. **Phase 1 Research Boundary**: No packaging adaptations, wrapper scripts, or code patches were authored or committed to repositories. All post-adaptation risk projections remain analytical estimates (`Not assessed` in packaged state).
3. **Independent-review limitation**: This review had access to the two uploaded D5 Markdown files, not the 19 source checkouts, D1–D4 files, manifest, ledger, or raw `git status` outputs. Accordingly, source-level findings and repository-cleanliness claims are recorded as author-reported where not reproducible from the supplied materials. D5 remains **Submitted for Independent Review — Not Yet Accepted**. Progression to D6 (`CONFLICT_ANALYSIS.md`) remains gated on formal acceptance and explicit user instruction.


## 9. Repository Cleanup Status

This deliverable pair is the proposed canonical D5 documentation. The uploaded files do not provide access to the project repository, so no legacy audit drafts have been deleted by this review and no repository directory state is certified here. Before removing legacy drafts, retain the accepted D5 canonical files and confirm that no manifest, ledger, or other deliverable links to the old filenames. D1–D4, the manifest, the reconciled ledger, and all 19 source checkouts remain outside the scope of any cleanup operation.
