# Deliverable 3: Legal & License Compliance Matrix (LICENSE_MATRIX.md)

**Document Identifier**: `SKILLS08-D3-LICENSE-MATRIX`  
**Version**: 1.0.0 (Research Deliverable)  
**Status**: Submitted for Review — Not Yet Accepted  
**Verification Target**: Google Antigravity (Initial Release Baseline)  
**Host Environment**: Windows 10/11 x64 (PowerShell 5.1)  
**Authoritative Evidence Baseline**: 19 Upstream Shallow Git Clones at Locked Commits (`research/sources/`)  
**Companion Deliverables**:
- [SOURCE_INVENTORY.md](file:///d:/skills08/docs/research/SOURCE_INVENTORY.md) (Accepted Deliverable 1)
- [SKILLS_EXTRACTION.md](file:///d:/skills08/docs/research/SKILLS_EXTRACTION.md) (Accepted Deliverable 2)
- [COMPATIBILITY_MATRIX.md](file:///d:/skills08/docs/research/COMPATIBILITY_MATRIX.md) (Accepted Deliverable 4)
- [manifest.yaml](file:///d:/skills08/manifests/manifest.yaml) (Accepted Master Manifest)

> [!CAUTION]
> **No Redistribution Authorization**: This document records research findings and compliance analyses only. It does **not** grant authorization for physical skill distribution, copying, installation, or runtime deployment. All candidates remain classified as provisional research candidates in `manifests/manifest.yaml`.

---

## 1. Executive Summary

### 1.1. Overall Licensing Position
The Skills08 project establishes a curated, local-first skill distribution mechanism for Google Antigravity and compatible coding agents. Deliverable 3 establishes the authoritative legal, copyright, attribution, and redistribution baseline for all 19 acquired upstream repositories and the 13 candidate skills shortlisted in `manifests/manifest.yaml`.

Every legal determination in this report is anchored directly in the physical file contents of the locked shallow checkouts in `research/sources/`. The investigation reveals that while the collection is predominantly governed by standard permissive open-source licenses, critical asset-level variations, notice obligations, non-commercial restrictions, and uncredited third-party bundles preclude blanket or automated redistribution.

### 1.2. Reconciled Repository-Level License Totals
Across the 19 acquired upstream repositories, physical inspection of root legal files, manifests, and package declarations establishes the following authoritative primary license distribution:

$$\text{Total Repositories} = 11 \text{ (MIT)} + 5 \text{ (Apache-2.0)} + 1 \text{ (CC0-1.0)} + 1 \text{ (CC-BY-4.0)} + 1 \text{ (Unlicensed)} = 19$$

```
====================================================================================================
AUTHORITATIVE PRIMARY REPOSITORY LICENSE DISTRIBUTION (19 Repositories)
====================================================================================================
License Family           SPDX Identifier  Count  Repository Names & IDs
----------------------------------------------------------------------------------------------------
MIT License              MIT                11   01: agent-skills, 02: antigravity-skills,
                                                 04: awesome-design-md, 06: ecc, 08: hallmark,
                                                 09: humanizer, 13: open-pencil (REUSE root/editor),
                                                 14: public-apis, 15: scroll-craft,
                                                 16: security-audit-skill, 18: taste-skill
----------------------------------------------------------------------------------------------------
Apache License 2.0       Apache-2.0          5   03: archify, 10: hyperframes, 11: impeccable,
                                                 12: open-design, 17: Soup
----------------------------------------------------------------------------------------------------
Creative Commons         CC0-1.0             1   05: awesome-playwright (Public Domain Dedication)
                         CC-BY-4.0           1   19: unslop (Attribution 4.0 International)
----------------------------------------------------------------------------------------------------
Unlicensed / Unknown     None                1   07: free-for-dev (Redistribution rights unestablished)
====================================================================================================
TOTAL ACQUIRED SOURCES                      19   100% Mathematically Reconciled
====================================================================================================
```

*Reconciliation Note*: Repository 17 (`Soup`, `MakazhanAlpamys/Soup`) is governed by Apache License 2.0 accompanied by a root `NOTICE` file. An earlier draft typographical error that listed `Soup` under the MIT total has been formally corrected.

### 1.3. Four Candidate Redistribution Clearance Tiers
Redistribution clearance cannot be conferred based solely on a repository's root license. Shortlisted candidates bundle instruction markdown files, companion reference playbooks, execution scripts, data schemas, vector brand marks, and embedded fonts. Evaluating all candidate assets establishes four distinct clearance tiers:

1. **Tier 1: Standard Permissive Licence — No Additional Licensing Blocker Identified (8 Candidates)**:
   - Candidates governed by standard permissive licenses (MIT) where physical inspection of the defined candidate distribution bundle identified no conflicting third-party licenses, reciprocal copyleft terms, or unresolved encumbrances.
   - **Candidate Scope Boundary**: This classification applies strictly to the reviewed candidate distribution scope, not to every file that might ever be included in the candidate's upstream repository or directory tree. An upstream repository's MIT license does not automatically establish the provenance or licensing of every embedded or bundled third-party component (as demonstrated by the asset-level analyses of `archify` and `impeccable`). Within the reviewed candidate packaging boundaries, no additional licensing blockers were identified.
   - *Candidates*: `SKILL08-SEC-001` (`security-audit`), `SKILL08-DOC-001` (`humanizer`), `SKILL08-UI-002` (`hallmark`), `SKILL08-FE-001` (`design-taste-frontend`), `SKILL08-SWE-001` (`code-simplification`), `SKILL08-TST-001` (`browser-testing-with-devtools`), `SKILL08-SWE-003` (`debugging-and-error-recovery`), `SKILL08-FE-002` (`scroll-craft`).
2. **Tier 2: Conditional Clearance — Scope, Provenance, or Modification Conditions (2 Candidates)**:
   - Candidates where redistribution is legally viable, but subject to specific unresolved scope/provenance questions or mandatory affirmative statutory change disclosures.
   - *Candidates*:
     - `SKILL08-SWE-002` (`simplify-codebase`): Governed by a local MIT license, but held conditionally pending formal confirmation of contributor provenance and reference playbook scope.
     - `SKILL08-UI-001` (`unslop`): Governed by CC-BY-4.0; requires creator attribution and mandatory Section 3(a)(1)(B) modification disclosures if adapted for packaging.
3. **Tier 3: Restricted Clearance — Mandatory Physical Excision, Module Sanitization, or Unresolved Evidence (2 Candidates)**:
   - Candidates that **cannot be redistributed in their unmodified upstream form** due to uncredited third-party scripts, embedded non-commercial / copyleft data assets, or unverified upstream provenance.
   - *Candidates*:
     - `SKILL08-UI-003` (`impeccable`): Governed by Apache-2.0. Unmodified upstream is not distributable. Candidate is held under Tier 3 restricted clearance pending resolution of external `ehmo` evidence: the original `ehmo` repository was not cloned, and statutory MIT notice preservation remains unresolved. Attribution in `NOTICE.md` alone does not satisfy the statutory MIT notice obligation, and the candidate's reference playbooks (`reference/ios.md`, `reference/android.md`) must not be redistributed until the notice and derivative rights are verified or excluded following legal assessment. Additionally mandates physically excising the `scripts/` directory (containing uncredited `modern-screenshot.umd.js`) and applying Apache Section 4(b) modification notices to altered files.
     - `SKILL08-ARC-001` (`archify`): Governed by Apache-2.0. Unmodified upstream is not distributable. Bundles vector brand marks carrying `CC-BY-NC-SA-4.0` (Vue.js) and `CC-BY-SA` (Rust, Jenkins). Deleting `generated-brand-marks.mjs` breaks Node.js ESM module loading; safe v0.1 distribution mandates replacing/sanitizing `generated-brand-marks.mjs` with a valid module exporting an empty or permissive-only array (preserving import resolution), bundling `NOTICE` / `THIRD_PARTY_NOTICES.md` / SIL OFL notices, applying Apache Section 4(b) modification notices, and performing runtime validation.
4. **Tier 4: Deferred Clearance — Operationally Blocked (1 Candidate)**:
   - Candidate whose underlying license is verified and permissive (MIT), but whose distribution is deferred due to external runtime architecture.
   - *Candidate*: `SKILL08-UI-004` (`open-pencil`) (deferred to Group B for v0.2+ due to desktop application dependencies).

### 1.4. Fundamental Distinction: Licensing Clearance vs. Technical Readiness
Licensing clearance establishes whether the legal copyright, license grant, attribution, and downstream terms permit Skills08 to package and distribute an asset. Licensing clearance **does not equate to technical compatibility, runtime safety, or operational release approval**:
- A skill may be legally clear under MIT (e.g. `security-audit`) while its companion dynamic test scripts remain technically unverified (`[Requires Runtime Validation]`) or restricted by operational release policy (Guidance Mode).
- A skill may be technically compatible with Antigravity (e.g. `impeccable` in fallback mode) while requiring physical file excision and statutory notice preservation before it can be legally redistributed.
- Deliverable 3 establishes **legal distribution eligibility only**. Actual packaging, file copying, and redistribution remain strictly prohibited until subsequent project phases authorize deployment.

---

## 2. Repository-Level Licence Inventory (All 19 Repositories)

The table below catalogs all 19 acquired repositories, their locked commit checkouts, root legal files, primary SPDX classifications, declared copyright holders, file metrics, and verified redistribution conditions.

| ID | Repository Name | Upstream Remote URL | Locked Commit SHA | Root Legal Files & Exact Paths | Primary SPDX | Declared Copyright Holder(s) | Redistribution Conditions & Legal Observations |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **01** | `agent-skills` | `https://github.com/addyosmani/agent-skills.git` | `39b723ceebf81474d0557c1fecd01eddab585563` | `LICENSE` (1,068 B) | **MIT** | Copyright (c) 2025 Addy Osmani | **Permitted**. Retain original copyright notice and MIT permission text in all copies. |
| **02** | `antigravity-skills` | `https://github.com/rmyndharis/antigravity-skills.git` | `2ee2cf79b99035fbdabdfe0b1057034195e7571e` | `LICENSE` (1,127 B)<br>`package.json` (`"license": "MIT"`) | **MIT** | Copyright (c) 2024 Seth Hobson<br>Copyright (c) 2026 Yudhi Armyndharis | **Permitted**. Retain copyright notices and MIT text. Manifest declares MIT. |
| **03** | `archify` | `https://github.com/tt-a1i/archify.git` | `a7ed6fd6657da90414831d1d42cf95987188750c` | `LICENSE` (11,358 B)<br>`LICENSE-MIT` (1,102 B)<br>`NOTICE` (1,340 B)<br>`THIRD_PARTY_NOTICES.md` (5,669 B) | **Apache-2.0** | Copyright (c) 2026 tt-a1i (Archify)<br>Copyright (c) 2025 Cocoon AI | **Restricted / Permitted with Conditions**. Apache-2.0 core with historical MIT code. Mandatory Section 4(d) `NOTICE` retention. Vector brand marks carry CC-BY-NC-SA and CC-BY-SA terms requiring module sanitization (preserving ESM import path) and post-sanitization runtime validation. Section 4(b) modification notices mandatory. |
| **04** | `awesome-design-md` | `https://github.com/voltagent/awesome-design-md.git` | `fcc70284932276d085f01ef9f83edde90b1258cb` | `LICENSE` (1,087 B) | **MIT** | Copyright (c) 2026 VoltAgent | **Permitted**. Retain VoltAgent copyright notice and MIT text. |
| **05** | `awesome-playwright` | `https://github.com/mxschmitt/awesome-playwright.git` | `3ef7191de074e66df322348337cf3ba9a0f83c5e` | `LICENSE` (7,169 B) | **CC0-1.0** | Public Domain Dedication (Oliver Stenbom / mxschmitt) | **Permitted**. Unrestricted worldwide public domain dedication. No legal attribution required by law. |
| **06** | `ecc` | `https://github.com/affaan-m/ecc.git` | `d2ef2680594f9a17526a6e1a2e18b3d242c5d17b` | `LICENSE` (1,071 B)<br>`package.json` (`"license": "MIT"`) | **MIT** | Copyright (c) 2026 Affaan Mustafa | **Permitted**. Retain Affaan Mustafa copyright notice and MIT text. |
| **07** | `free-for-dev` | `https://github.com/jixserver/free-for-dev.git` | `a6d2501c4d2566a3f518f08e51a23923edf65734` | **NO LEGAL FILE FOUND** | **None** | *None declared* (`jixserver`) | **BLOCKED / PROHIBITED**. Outdated fork containing no license file or notice. Rights unestablished. All rights reserved by default. |
| **08** | `hallmark` | `https://github.com/Nutlope/hallmark.git` | `04977e15f3dfd6ee4b74c887dac3eb52665d6c92` | `LICENSE` (1,078 B) | **MIT** | Copyright (c) 2026 Hallmark contributors | **Permitted**. Retain Hallmark contributors copyright notice and MIT text. Candidate folder contains identical local `LICENSE`. |
| **09** | `humanizer` | `https://github.com/blader/humanizer.git` | `b48c832f0f809c1b5658edbb838c2521b72f2413` | `LICENSE` (1,087 B)<br>`package.json` (`"license": "MIT"`) | **MIT** | Copyright (c) 2025 Siqi Chen | **Permitted**. Retain Siqi Chen copyright notice and MIT text. `SKILL.md` frontmatter explicitly declares MIT. |
| **10** | `hyperframes` | `https://github.com/heygen-com/hyperframes.git` | `ead110aab9e4b43befdbe21001deac168c09e04b` | `LICENSE` (10,763 B) | **Apache-2.0** | Copyright (c) 2026 HeyGen | **Permitted with Conditions**. Apache-2.0 terms apply. Retain Apache license and copyright notice. |
| **11** | `impeccable` | `https://github.com/pbakaus/impeccable.git` | `d41d9860b0094dcb68030657da63461212835aaa` | `LICENSE` (10,957 B)<br>`NOTICE.md` (514 B)<br>`package.json` (`"license": "Apache-2.0"`) | **Apache-2.0** | Copyright (c) Paul Bakaus<br>NOTICE: Derived from `ehmo` (MIT) | **Restricted / Permitted with Conditions**. Apache-2.0 core. Unmodified upstream not distributable. Candidate reference files remain unverified pending resolution of external ehmo MIT notice and derivative rights; reference files must not be redistributed until resolved or excluded. scripts/ directory must be physically excised. Mandatory Section 4(b) modification notices on altered files. |
| **12** | `open-design` | `https://github.com/nexu-io/open-design.git` | `84dd08b5709bfa4bf4108ece8424d15e4062c982` | `LICENSE` (11,497 B) | **Apache-2.0** | Copyright 2026 Open Design contributors | **Permitted with Conditions**. Apache-2.0 terms apply. Retain Apache license and copyright notice. |
| **13** | `open-pencil` | `https://github.com/open-pencil/open-pencil.git` | `50afc5cb789257338cd4102235ab16d9ade458f3` | `LICENSE` (1,121 B)<br>`REUSE.toml` (1,963 B)<br>`LICENSES/Apache-2.0.txt` (11,560 B)<br>`LICENSES/MIT.txt` (1,121 B) | **MIT** (Core/Skills)<br>*(Cloud: Apache-2.0)* | Copyright (c) 2026 Danila Poyarkov and OpenPencil contributors | **Permitted**. Governed by REUSE specification: editor, tools, and skills are MIT; Cloud portal is Apache-2.0. Local skill folder is clean MIT. |
| **14** | `public-apis` | `https://github.com/public-apis/public-apis.git` | `d6dab92da95c003e82e5b32c623bd2ad9d6a017f` | `LICENSE` (1,089 B) | **MIT** | Copyright (c) 2022 public-apis | **Permitted**. Retain public-apis copyright notice and MIT text. |
| **15** | `scroll-craft` | `https://github.com/nateherkai/scroll-craft.git` | `75d81f74e83692add18cd7a8a8e078b8a887a579` | `LICENSE` (1,087 B) | **MIT** | Copyright (c) 2026 Nate Herk | **Permitted**. Retain Nate Herk copyright notice and MIT text. |
| **16** | `security-audit-skill` | `https://github.com/cloudflare/security-audit-skill.git` | `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8` | `LICENSE` (1,099 B) | **MIT** | Copyright (c) 2025-2026 Cloudflare, Inc. | **Permitted**. Retain Cloudflare, Inc. copyright notice and MIT text. |
| **17** | `Soup` | `https://github.com/MakazhanAlpamys/Soup.git` | `deb9f0af0a4bbb5da11b30293a2efdcf82611df1` | `LICENSE` (11,560 B)<br>`NOTICE` (65 B) | **Apache-2.0** | Copyright 2026 Makazhan Alpamys and the Soup contributors | **Permitted with Conditions**. Apache-2.0 terms apply. Mandatory retention of root `NOTICE` file under Section 4(d). |
| **18** | `taste-skill` | `https://github.com/leonxlnx/taste-skill.git` | `f6b76575f949707b4e3c37cd86cb44b0b98643e8` | `LICENSE` (1,086 B) | **MIT** | Copyright (c) 2026 Leonxlnx | **Permitted**. Retain Leonxlnx copyright notice and MIT text. |
| **19** | `unslop` | `https://github.com/heydamir/unslop.git` | `620163eedb3529d9cd23a3994ed8d287d06f760d` | `LICENSE` (19,053 B) | **CC-BY-4.0** | Damir Sokolovsky (`@heydamir`) | **Permitted with Conditions**. Creative Commons Attribution 4.0 International. Attribution, license link, and affirmative Section 3(a)(1)(B) modification disclosures mandatory. |

---

## 3. Candidate-Level Licence Matrix (All 13 Candidates)

The table below catalogs all 13 candidates from `manifests/manifest.yaml`. Every candidate ID, canonical skill name, and repository-relative source path matches the accepted manifest and physical repository checkouts exactly.

```
==================================================================================================================================================
CANDIDATE-LEVEL LICENCE & COMPLIANCE MATRIX (13 Shortlisted Candidates)
==================================================================================================================================================
Candidate Identifier Canonical Skill Name           Exact Repository-Relative Source Path & Repository   Governing Licence   Clearance Tier Attribution & Notice Obligations
--------------------------------------------------------------------------------------------------------------------------------------------------
SKILL08-SEC-001      security-audit                 skills/security-audit/SKILL.md                       MIT                 Tier 1         Retain Cloudflare, Inc. copyright notice;
                                                    (cloudflare/security-audit-skill)                    (Root LICENSE)      (Permissive)   bundle standard MIT license text.
--------------------------------------------------------------------------------------------------------------------------------------------------
SKILL08-DOC-001      humanizer                      SKILL.md                                             MIT                 Tier 1         Retain Siqi Chen copyright notice;
                                                    (blader/humanizer)                                   (Root & Frontmatter)(Permissive)   bundle standard MIT license text.
--------------------------------------------------------------------------------------------------------------------------------------------------
SKILL08-UI-001       unslop                         skills/unslop/SKILL.md                               CC-BY-4.0           Tier 2         Attribute Damir Sokolovsky; link to CC-BY-4.0;
                                                    (heydamir/unslop)                                    (Root LICENSE)      (Conditional)  MANDATORY Section 3(a)(1)(B) change disclosure.
--------------------------------------------------------------------------------------------------------------------------------------------------
SKILL08-UI-002       hallmark                       skills/hallmark/SKILL.md                             MIT                 Tier 1         Retain Hallmark contributors copyright notice;
                                                    (Nutlope/hallmark)                                   (Root & Local)      (Permissive)   bundle standard MIT license text.
--------------------------------------------------------------------------------------------------------------------------------------------------
SKILL08-FE-001       design-taste-frontend          skills/taste-skill/SKILL.md                          MIT                 Tier 1         Retain Leonxlnx copyright notice;
                                                    (leonxlnx/taste-skill)                               (Root LICENSE)      (Permissive)   bundle standard MIT license text.
--------------------------------------------------------------------------------------------------------------------------------------------------
SKILL08-SWE-001      code-simplification            skills/code-simplification/SKILL.md                  MIT                 Tier 1         Retain Addy Osmani copyright notice;
                                                    (addyosmani/agent-skills)                            (Root LICENSE)      (Permissive)   bundle standard MIT license text.
--------------------------------------------------------------------------------------------------------------------------------------------------
SKILL08-SWE-002      simplify-codebase              .agents/skills/simplify-codebase/SKILL.md            MIT                 Tier 2         Retain simplify-codebase contributors notice;
                                                    (tt-a1i/archify)                                     (Local LICENSE)     (Conditional)  held conditional pending provenance confirmation.
--------------------------------------------------------------------------------------------------------------------------------------------------
SKILL08-TST-001      browser-testing-with-devtools  skills/browser-testing-with-devtools/SKILL.md        MIT                 Tier 1         Retain Addy Osmani copyright notice;
                                                    (addyosmani/agent-skills)                            (Root LICENSE)      (Permissive)   bundle standard MIT license text.
--------------------------------------------------------------------------------------------------------------------------------------------------
SKILL08-SWE-003      debugging-and-error-recovery   skills/debugging-and-error-recovery/SKILL.md         MIT                 Tier 1         Retain Addy Osmani copyright notice;
                                                    (addyosmani/agent-skills)                            (Root LICENSE)      (Permissive)   bundle standard MIT license text.
--------------------------------------------------------------------------------------------------------------------------------------------------
SKILL08-ARC-001      archify                        archify/SKILL.md                                     Apache-2.0          Tier 3         Bundle Apache-2.0, NOTICE, OFL, & Pele MIT.
                                                    (tt-a1i/archify)                                     (Root & Pkg LICENSE)(Restricted)   Sanitize generated-brand-marks; Section 4(b) notes.
--------------------------------------------------------------------------------------------------------------------------------------------------
SKILL08-FE-002       scroll-craft                   plugins/nateherk-design/skills/scroll-craft/SKILL.md MIT                 Tier 1         Retain Nate Herk copyright notice;
                                                    (nateherkai/scroll-craft)                            (Root LICENSE)      (Permissive)   bundle standard MIT license text.
--------------------------------------------------------------------------------------------------------------------------------------------------
SKILL08-UI-003       impeccable                     .agents/skills/impeccable/SKILL.md                   Apache-2.0          Tier 3         Bundle Apache-2.0 & NOTICE.md. Physically
                                                    (pbakaus/impeccable)                                 (Root LICENSE)      (Restricted)   excise scripts/; ref files unverified; 4(b) note.
--------------------------------------------------------------------------------------------------------------------------------------------------
SKILL08-UI-004       open-pencil                    skills/open-pencil/SKILL.md                          MIT                 Tier 4         Retain Danila Poyarkov / contributors notice.
                                                    (open-pencil/open-pencil)                            (REUSE & Local)     (Deferred)     Licensing clear, but deferred to v0.2+ runtime.
==================================================================================================================================================
```

---

## 4. Detailed Legal Analysis of Complex Candidates

### 4.1. `SIMPLIFY-CODEBASE` (`SKILL08-SWE-002`)
- **Upstream Location & Commit**: `tt-a1i/archify.git` at path `.agents/skills/simplify-codebase/` (Commit: `a7ed6fd665...`).
- **Local Licence Evidence**: The directory contains a dedicated file titled `LICENSE` (1,087 bytes, SHA-256: `fa5adbb22e6cbe08103f365a3418d1ede2490432e8d6c8769118f326b47dfc30`) granting standard MIT permissions on behalf of `Copyright (c) 2026 simplify-codebase contributors`.
- **Directory Scope & Companion Playbooks**:
  - The local `LICENSE` file resides at the root of `.agents/skills/simplify-codebase/`.
  - Under standard open-source directory conventions, placing a license file at the root of a distinct folder creates a presumptive legal grant covering all files within that directory tree (`SKILL.md`, `agents/openai.yaml`, and the five companion reference playbooks in `references/`: `boundaries-and-lifecycle.md`, `decision-records.md`, `execution-and-recovery.md`, `integrating-findings.md`, `investigation.md`).
  - **Absence of Individual File Headers**: Physical inspection confirms that none of the five companion playbooks contain file-level copyright headers. In established open-source legal practice, the absence of individual file headers does **not** invalidate a directory-level license file, nor does it cause those files to revert to the parent repository's license.
- **Upstream Repository Reconciliation**:
  - In `manifests/manifest.yaml`, the declared license is recorded as `Apache-2.0`, which reflected the parent repository's root license rather than the directory layout.
  - Upstream `archify/NOTICE` explicitly provides for sub-package licensing variations:
    > *"Archify is distributed under the Apache License, Version 2.0 (LICENSE), except where a file, package manifest, or third-party notice specifies otherwise. The separately versioned DeepSeek Harness adapter remains MIT; its bundled Skill retains the license of the immutable source selected in release.json."*
  - This carve-out confirms that sub-packages within `archify` carry independent licensing.
- **Unresolved Contributor Provenance & Conditional Clearance**:
  - While the local MIT license is legally valid on disk, upstream repository records do not enumerate or identify `"simplify-codebase contributors"`, nor does `NOTICE` reference this skill by name.
  - **Clearance Decision**: The candidate cannot be classified as unconditionally clear while contributor provenance remains unconfirmed. It is classified as **Tier 2: Conditional Clearance**.
  - **Packaging Rule**: When packaged for Skills08, the distribution must bundle `.agents/skills/simplify-codebase/LICENSE` and retain attribution to `simplify-codebase contributors`.

---

### 4.2. `IMPECCABLE` (`SKILL08-UI-003`)
- **Upstream Location & Commit**: `pbakaus/impeccable.git` at path `.agents/skills/impeccable/` (Commit: `d41d9860b0094dcb68030657da63461212835aaa`).
- **Governing Licence**: Apache License 2.0 (`LICENSE`, 10,957 bytes).
- **Derived Work Analysis & Unresolved Statutory MIT Preservation (`ehmo`)**:
  - Upstream root `NOTICE.md` (514 bytes) acknowledges:
    > *"The `skill/reference/ios.md` and `skill/reference/android.md` platform reference files are distilled from ehmo's `platform-design-skills` (Apple Human Interface Guidelines and Material Design 3 rules), rewritten in Impeccable's voice. Original work: https://github.com/ehmo/platform-design-skills. Original license: MIT. Author: ehmo."*
  - **Distinction Between Upstream `NOTICE.md` Phrasing and Legal Status**:
    - The upstream `NOTICE.md` describes the reference playbooks as "distilled... rewritten in Impeccable's voice." This descriptive characterization cannot be conflated with an independently established legal conclusion regarding whether rewritten platform reference text constitutes a copyright-protected derivative work.
    - If the material constitutes a derivative work or a substantial portion of the original work, downstream distributors are legally bound by the statutory terms of the incoming MIT license.
  - **Distinction Between `NOTICE.md` Attribution and Statutory MIT Notice Preservation**:
    - Citing `ehmo` in `NOTICE.md` satisfies Apache 2.0 Section 4(d) attribution obligations.
    - However, the incoming source work (`platform-design-skills`) is licensed under the **MIT License**, which explicitly mandates:
      > *"The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software."*
    - Attribution in `NOTICE.md` does **not** satisfy the statutory MIT notice obligation. A descriptive citation in an Apache NOTICE file stating that an upstream work was under "MIT" does not fulfill the statutory requirement to include the actual MIT copyright notice and permission text.
    - Physical inspection of `.agents/skills/impeccable/reference/ios.md` and `reference/android.md` confirms neither file embeds the MIT text.
  - **Unresolved Evidence on External Upstream Checkout**:
    - The external repository `ehmo/platform-design-skills` is **not** among the 19 acquired sources in `research/sources/` and was not cloned locally.
    - The original copyright notice (exact year and legal identity of the copyright holder) and the original license text have **not been inspected or verified from local checkouts**.
    - Statutory MIT notice preservation has **not been resolved** and cannot be treated as a completed packaging condition.
  - **Distribution Restriction**:
    - Until the open legal question regarding derivative work status is resolved and the upstream rights and notices in that material are verified or excluded following formal legal assessment, the reference files (`reference/ios.md` and `reference/android.md`) remain unverified and **must not be redistributed as clean upstream code**.
    - Consequently, `impeccable` remains subject to **Tier 3: Restricted Clearance** pending resolution of the `ehmo` evidence.
- **Direct Evidence on D4 Fallback Exclusions & `scripts/` Directory**:
  - In Deliverable 4 (`COMPATIBILITY_MATRIX.md`, Profile 12), `impeccable` was evaluated under its documented pure-instruction fallback mode:
    > *"Required Adaptations: 1. Pin instructions strictly to the documented pure-instruction fallback mode. 2. Remove references to binary launcher execution. 3. Co-locate all 12 reference playbooks in `reference/`."*
  - Physical inspection of `.agents/skills/impeccable/SKILL.md` confirms that the skill instructions execute the binary launcher:
    - `${CLAUDE_SKILL_DIR}/scripts/impeccable context`
    - `${CLAUDE_SKILL_DIR}/scripts/impeccable.cmd`
  - In contrast, the remaining files in `scripts/` are auxiliary files used by upstream build and extension harnesses:
    - `scripts/modern-screenshot.umd.js` (29,304 bytes, SHA-256: `9b0dc34415466edac6e6802574006608b5e5c0da9fdcb7b2651dbd1ea06713a6`): An uncredited minified build of `modern-screenshot` (MIT by wheeeb / qq15725) with stripped copyright headers and no citation in `NOTICE.md`. This file is not a legal notice or license text, but an uncredited JavaScript bundle inspected to establish third-party licensing risk.
    - `scripts/live-browser-*.js`: In-page DOM inspection scripts.
    - `scripts/data/font-index.json`: Font metrics metadata.
  - **Direct Evidence Finding**: D4 established that runtime execution of the launcher is bypassed in fallback mode. However, fallback mode does **not** physically delete files from the disk checkout. Naively copying the candidate folder would distribute `modern-screenshot.umd.js` without required MIT attribution.
  - **Mandatory Packaging Rule**: The Skills08 packaging specification must **explicitly enforce the physical exclusion of the entire `scripts/` directory** from the distribution package.
- **Apache 2.0 Section 4(b) Modification Notices**:
  - Modifying `.agents/skills/impeccable/SKILL.md` to remove binary execution steps and enforce fallback mode constitutes creating a modified file under Apache 2.0.
  - Section 4(b) legally mandates that the modified file carry prominent notices stating that it was changed (e.g. `<!-- Modified by Skills08: Adapted for Antigravity pure-instruction fallback mode -->`).

---

### 4.3. `ARCHIFY` (`SKILL08-ARC-001`)
- **Upstream Location & Commit**: `tt-a1i/archify.git` at path `archify/` (Commit: `a7ed6fd6657da90414831d1d42cf95987188750c`).
- **Governing Licence**: Apache License 2.0 (`archify/LICENSE`, 11,358 bytes).
- **Exact Proposed v0.1 Distribution Boundary**:
  To ensure licensing compliance, prevent copyleft contagion, and avoid bloat, upstream files are mapped across four strict boundaries:
  1. *Selected Core Skill*: `archify/SKILL.md` (18,877 bytes).
  2. *Required Companion Files*:
     - `references/` (authoring contracts, architecture repair, delivery contracts, layout repair).
     - `schemas/` (11 JSON-IR schemas: `architecture.schema.json`, `sequence.schema.json`, etc.).
     - `bin/archify.mjs` and core renderers (`renderers/**`, `assets/template.html`).
  3. *Optional Upstream Components & Data Assets*:
     - `brand-marks/catalog.json` (14,154 bytes) & `brand-marks/README.md`.
     - `renderers/shared/generated-brand-marks.mjs` (163,612 bytes).
     - `explainer/vendor/pele/` (Pele Mermaid core, MIT).
     - `assets/JetBrainsMono-OFL.txt` (SIL Open Font License 1.1).
     - `locales/` (translations).
     - `examples/` (reference JSON and HTML files).
  4. *Unrelated Upstream Assets (Excluded from Candidate Scope)*:
     - `.agents/skills/simplify-codebase/` (independent skill).
     - `integrations/deepseek-harness/` (separate adapter).
     - Root development files (`test/`, `scripts/`, `docs/`).
- **Asset-Level Licensing Assessment of Brand Marks (`generated-brand-marks.mjs`)**:
  - Upstream `renderers/shared/generated-brand-marks.mjs` embeds SVG path data for corporate logos generated from Simple Icons 16.28.0.
  - Physical inspection of metadata inside `generated-brand-marks.mjs` reveals distinct asset-level licenses:
    - **Vue.js**: Recorded as **`CC-BY-NC-SA-4.0`** (Non-Commercial + ShareAlike).
    - **Rust**: Recorded as **`CC-BY-SA-4.0`** (ShareAlike).
    - **Jenkins**: Recorded as **`CC-BY-SA-3.0`** (ShareAlike).
    - **Angular**: Recorded as `CC-BY-4.0`.
    - **.NET**: Recorded as `CC0-1.0`.
    - **JavaScript**: Recorded as `MIT`.
    - **Apache Airflow / Kafka**: Recorded as `Apache-2.0`.
  - **Module Imports & Load-Time Dependencies**:
    - Static inspection confirms that `renderers/shared/brand-marks.mjs` directly imports `BRAND_MARKS` from `generated-brand-marks.mjs`:
      ```javascript
      import { BRAND_MARKS } from './generated-brand-marks.mjs';
      ```
    - **Crucial Packaging Constraint**: Simply deleting `generated-brand-marks.mjs` would cause Node.js ESM module resolution to fail (`ERR_MODULE_NOT_FOUND`) when `renderers/shared/brand-marks.mjs` is loaded.
    - **Accurate Sanitization Requirement**: Sanitization requires replacing or modifying `generated-brand-marks.mjs` with a valid ESM module exporting an empty or permissive-only `BRAND_MARKS` array (e.g. `export const BRAND_MARKS = [];` or retaining only MIT/Apache/CC0 marks), thereby preserving the import path and module loading integrity.
- **Control-Flow Analysis & Feasibility Evaluation**:
  - Static code inspection of `renderers/shared/brand-marks.mjs` confirms how brand marks are resolved in control flow:
    - `findBrandMark(value)` searches `MARK_BY_LOOKUP` and returns `null` if the requested mark is missing or excised.
    - `renderBrandMark(node)` explicitly implements: `const mark = brandMarkFor(node); if (!mark) return '';`.
    - When a mark is omitted or returns `null`, the renderer outputs an empty string and renders the diagram node normally without an icon.
    - `references/brand-marks.md` explicitly instructs agents: *"If there is no match and no user-provided URL, omit brand."*
  - **Softened Feasibility Conclusion**:
    - Static inspection of the control flow indicates that omitted brand marks should fall back gracefully without breaking diagram generation.
    - However, static inspection alone does not guarantee end-to-end execution; **runtime and package-level validation remain required after sanitization** to confirm that CLI workflows and renderer passes execute cleanly without unhandled edge cases.
- **Copyright Licences vs. Trademark Permissions**:
  - Upstream `THIRD_PARTY_NOTICES.md` explicitly records:
    > *"Archify includes optional vector data for third-party brand marks... Names and logos do not imply official endorsement, and the software license grants no general trademark permission... Users are responsible for confirming that their particular use is permitted."*
  - Corporate logos represent protected trademarks regardless of the vector data's copyright license. Skills08 grants no trademark rights and makes no claim of universal commercial or trademark clearance.
- **Font Inclusion Analysis (JetBrains Mono)**:
  - Physical inspection of `research/sources/archify/archify/assets/` confirms that **no standalone font binaries (`.ttf`, `.woff`, `.woff2`) exist on disk**.
  - Instead, variable font subsets are embedded as base64-encoded WOFF2 strings directly inside `assets/template.html` (which is distributed with the renderer).
  - The accompanying license notice `assets/JetBrainsMono-OFL.txt` (4,398 bytes) provides the complete text of the SIL Open Font License 1.1 required for distributing that font subset.
- **Minimum Safe Distribution Scope for v0.1**:
  - Distribute `SKILL.md`, `references/`, `schemas/`, `bin/archify.mjs`, core `renderers/`, `assets/template.html`, and `vendor/pele/`.
  - **Sanitize `generated-brand-marks.mjs` by preserving the module import path and exporting an empty or permissive-only `BRAND_MARKS` array**, excising the `CC-BY-NC-SA-4.0` (Vue.js) and `CC-BY-SA` (Rust, Jenkins) entries; sanitize or omit `brand-marks/catalog.json` accordingly.
  - Bundle Apache 2.0 license, `NOTICE`, `THIRD_PARTY_NOTICES.md`, Pele MIT license, and SIL OFL font notice.
  - Apply Apache Section 4(b) modification notices to any altered files.
  - Conduct mandatory runtime and package-level validation post-sanitization.

---

### 4.4. `UNSLOP` (`SKILL08-UI-001`)
- **Upstream Location & Commit**: `heydamir/unslop.git` at path `skills/unslop/` (Commit: `620163eedb...`).
- **Governing Licence**: Creative Commons Attribution 4.0 International (`CC-BY-4.0`) (`LICENSE`, 19,053 bytes).
- **Author & Rights Holder**: Damir Sokolovsky (`@heydamir`).
- **Companion Asset Provenance**:
  - The directory contains 6 markdown reference playbooks, 5 `.webp` visual reference images in `references/refs/`, and 1 companion script `scripts/snapshot.mjs`.
  - Upstream `references/refs.md` explicitly documents the provenance and licensing of the visual assets:
    > *"Finished screens by Damir Sokolovsky ([@heydamir]). Look at them before the Visuals pass... Part of unslop by Damir Sokolovsky ([@heydamir]), CC BY 4.0. Keep this credit in copies and adaptations."*
  - This verifies that the reference images are original works created by the upstream author under CC-BY-4.0.
- **Statutory Modification Disclosure Mandate**:
  - CC-BY-4.0 permits commercial distribution, copying, and adaptation, but Section 3(a)(1)(B) imposes an affirmative legal obligation:
    > *"indicate if You modified the Licensed Material and retain an indication of any previous modifications;"*
  - **Packaging Requirement**: If Skills08 adapts `unslop` (e.g. sanitizing relative paths, modifying frontmatter, or adding agent wrapping), the distributed skill **must include an explicit change notice** (in `MODIFICATIONS.md` or a prominent header block) detailing all alterations made by Skills08.

---

## 5. Licence Compliance Taxonomy

The Skills08 project classifies incoming and outgoing licensing terms into seven distinct classes, defining exact rights, obligations, and copyleft boundaries.

```
========================================================================================================================
SKILLS08 FORMAL LICENCE & COMPLIANCE TAXONOMY
========================================================================================================================
Class   SPDX Identifier    Category              Rights Granted       Statutory Conditions & Compliance Rules
------------------------------------------------------------------------------------------------------------------------
Class A MIT                Permissive Software   Commercial, Modify,  • Retain original copyright notice and permission text.
        BSD-3-Clause                             Distribute, Private  • Permissive; compatible with all installation scopes.
------------------------------------------------------------------------------------------------------------------------
Class B Apache-2.0         Permissive Software   Commercial, Modify,  • Section 4(a): Provide copy of Apache-2.0 license.
                           with Patent Grant     Distribute, Patent   • Section 4(b): MANDATORY PROMINENT NOTICE ON MODIFIED FILES.
                                                 Grant                • Section 4(c): Retain all copyright, patent, & notices.
                                                                      • Section 4(d): MANDATORY RETENTION OF NOTICE FILE TEXT.
                                                                      • Section 6: No grant of trademark permissions.
------------------------------------------------------------------------------------------------------------------------
Class C CC-BY-4.0          Content Attribution   Commercial, Modify,  • Section 3(a)(1): Attribution to creator, link to license.
                                                 Distribute           • Section 3(a)(1)(B): MANDATORY NOTICE OF MODIFICATIONS.
                                                                      • Permissive content license; permits commercial use.
------------------------------------------------------------------------------------------------------------------------
Class D CC0-1.0            Public Domain         Unrestricted Use     • Voluntary waiver of all copyright and related rights.
                           Dedication                                 • No statutory attribution required by law.
------------------------------------------------------------------------------------------------------------------------
Class E CC-BY-SA-3.0       Reciprocal Content    Commercial, Modify,  • ShareAlike: Any Adapted Material produced by modifying
        CC-BY-SA-4.0       (ShareAlike Copyleft) Distribute with SA    this work MUST be distributed under the SAME license.
                                                                      • Does NOT automatically infect independent software in an
                                                                        aggregate distribution.
------------------------------------------------------------------------------------------------------------------------
Class F CC-BY-NC-SA-4.0    Non-Commercial        NON-COMMERCIAL ONLY, • NonCommercial: "not primarily intended for or directed
                           Reciprocal Content    Modify, Distribute   towards commercial advantage or monetary compensation."
                                                 with ShareAlike      • Strictly restricts distribution of the asset commercially.
                                                                      • ShareAlike: Derivative works must use the same license.
------------------------------------------------------------------------------------------------------------------------
Class G None               Unlicensed / Default  NONE (All Rights     • No license grant. Redistribution without explicit
        (All Rights Reserved)Copyright Default   Reserved)            upstream authorization is legally prohibited.
========================================================================================================================
```

### Detailed Notes on Creative Commons Mechanics:
1. **ShareAlike Scope & Aggregate Distributions**:
   - Under CC-BY-SA-3.0 and CC-BY-SA-4.0, the ShareAlike obligation applies strictly to **Adapted Material** (material derived from or based upon the licensed work).
   - Bundling a CC-BY-SA asset beside independent software in an aggregate collection does **not** automatically convert the independent software into a derivative work or subject the entire repository to ShareAlike terms.
   - However, modifying or creating a derivative work of the specific CC-BY-SA asset legally requires releasing that adaptation under the identical ShareAlike license.
2. **Creative Commons NonCommercial Definition**:
   - CC-BY-NC-SA-4.0 defines NonCommercial as: *"not primarily intended for or directed towards commercial advantage or monetary compensation."*
   - Skills08 does not make broader assumptions regarding commercial intent. To prevent legal exposure for enterprise or commercial users of Skills08, assets bearing NonCommercial restrictions must be excised from general-purpose distribution bundles.

---

## 6. Evidence and Integrity: Cryptographic Legal & Provenance Ledger

The cryptographic ledger below records the exact repository-relative paths, byte sizes, binary SHA-256 checksums, and legal classifications for **selected legal, notice, and candidate-level evidence files directly verified in the locked repository checkouts**. All checksums were calculated directly from binary disk reads (`open(..., 'rb')`).

To maintain strict evidentiary precision, the ledger explicitly distinguishes primary legal and notice files from auxiliary files inspected to establish third-party provenance, unlicensed code, or asset-level licensing risk (such as uncredited bundles or embedded multi-licensed datasets).

### 6.1. Selected Primary Repository and Candidate Legal & Notice Files

The following table records verified primary legal files, root licenses, candidate-level license files, statutory `NOTICE` documents, and font notices across the 19 locked checkouts.

```
========================================================================================================================================================================================
PRIMARY REPOSITORY & CANDIDATE LEGAL EVIDENCE LEDGER (Authoritative Binary Disk Verification)
========================================================================================================================================================================================
Repo ID / Entity            Exact Repository-Relative File Path                                   Bytes  SHA-256 Checksum (Binary Mode)                                    SPDX / Legal Status
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
01 agent-skills             research/sources/agent-skills/LICENSE                                 1,068  6f202f8bd568cd730dbb2b0d1f8e243bc74c2fa1f64dbce9b2c7ea08bd5c9fd7  Class A (MIT)
02 antigravity-skills       research/sources/antigravity-skills/LICENSE                           1,127  a27bbcf4c259b990debbb9c8d74424ca29565a85903bdd4d59d41c7600e3d36d  Class A (MIT)
03 archify (Root)           research/sources/archify/LICENSE                                     11,358  cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30  Class B (Apache-2.0)
03 archify (Root)           research/sources/archify/LICENSE-MIT                                  1,102  b799ab081703e7821ae5096d2c1abdf14bbdc75e8ea1c4045998c36ed6db9706  Class A (Historical MIT)
03 archify (Root)           research/sources/archify/NOTICE                                       1,340  665eb53e6fcf09cee183c9f23c8052645dc95570d9ccbbf53dc0f5213a1b5edd  Class B (Apache-2.0 NOTICE)
03 archify (Root)           research/sources/archify/THIRD_PARTY_NOTICES.md                       5,669  b5e129197f391568f7abf287c74b24f4835f10e5388f600407c8788feaeb9015  Class B/E/F Third-Party
03 archify (Pkg)            research/sources/archify/archify/LICENSE                             11,358  cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30  Class B (Pkg Apache-2.0)
03 archify (Pkg)            research/sources/archify/archify/LICENSE-MIT                          1,102  b799ab081703e7821ae5096d2c1abdf14bbdc75e8ea1c4045998c36ed6db9706  Class A (Pkg MIT)
03 archify (Pkg)            research/sources/archify/archify/NOTICE                               1,340  665eb53e6fcf09cee183c9f23c8052645dc95570d9ccbbf53dc0f5213a1b5edd  Class B (Pkg NOTICE)
03 archify (Pkg)            research/sources/archify/archify/THIRD_PARTY_NOTICES.md               5,669  b5e129197f391568f7abf287c74b24f4835f10e5388f600407c8788feaeb9015  Class B/E/F Third-Party
03 archify (Font)           research/sources/archify/archify/assets/JetBrainsMono-OFL.txt         4,398  c1ab7c666206842a02b35b30770dac0d7a10156ed401c9defc3f02a754d89e90  SIL OFL 1.1 Font Notice
03 archify (Vendor)         research/sources/archify/archify/explainer/vendor/pele/LICENSE        1,934  311bccc30de6f7b9cbfb64232bb0c911ccb2191abe316550813ae25b2c7925b9  Class A (Pele Core MIT)
03 simplify-codebase        research/sources/archify/.agents/skills/simplify-codebase/LICENSE     1,087  fa5adbb22e6cbe08103f365a3418d1ede2490432e8d6c8769118f326b47dfc30  Class A (Local MIT)
04 awesome-design-md        research/sources/awesome-design-md/LICENSE                            1,087  0862a727415509d17206d78bfbfe2f6b142f2c2833283b457a6f0db972ee6ed3  Class A (MIT)
05 awesome-playwright       research/sources/awesome-playwright/LICENSE                           7,169  f4e7f373b9b996950337e8d41a4a2939c2d90b7725e9baf3d5084a22717ad328  Class D (CC0-1.0)
06 ecc                      research/sources/ecc/LICENSE                                          1,071  326146379f01bb137c0a5d3c54770c1aa31076705c8b88a7f6b26a460f6221b2  Class A (MIT)
07 free-for-dev             research/sources/free-for-dev/ (NO LEGAL FILE FOUND)                      0  MISSING                                                           Class G (Unlicensed)
08 hallmark (Root)          research/sources/hallmark/LICENSE                                     1,078  06088a8b94598626f27612dea42300154bf7be967c85d9d3eee4490cb056af7d  Class A (MIT)
08 hallmark (Candidate)     research/sources/hallmark/skills/hallmark/LICENSE                     1,078  06088a8b94598626f27612dea42300154bf7be967c85d9d3eee4490cb056af7d  Class A (Local MIT)
09 humanizer                research/sources/humanizer/LICENSE                                    1,087  caa1be9cba41c1afb88fe730ab1a4e04728295ea5b29ac2ee9f003a4ffbe3a77  Class A (MIT)
10 hyperframes              research/sources/hyperframes/LICENSE                                 10,763  4259155fb06f127687ee7b0a8a3682d45132db0f2da26cbc0b7a2d1e796436b8  Class B (Apache-2.0)
11 impeccable               research/sources/impeccable/LICENSE                                  10,957  fc0673369dae07c045c46869d3d4c9113678c77fcc7d3b4e3a39ac074cfa68b6  Class B (Apache-2.0)
11 impeccable               research/sources/impeccable/NOTICE.md                                   514  9bc6cf69fa566aaaf6fa5cf40397597eab8b39f497de61728da7bcf0930db207  Class B (NOTICE Citation)
12 open-design              research/sources/open-design/LICENSE                                 11,497  5af3e43224f112bc45788d510afd3e1c0eec60bbc54e9a95b9171e54d750f4b0  Class B (Apache-2.0)
13 open-pencil (Root)       research/sources/open-pencil/LICENSE                                  1,121  8ddd3124beb01b4a41d405607829ca33404cb4adbe05c0fecfe21c754fd27158  Class A (MIT Root)
13 open-pencil (REUSE)      research/sources/open-pencil/REUSE.toml                               1,963  4126c6d8d3885a01c79d5c690e1463647bcdbc043e6e89649d9c9fcdd4d03784  REUSE Specification
13 open-pencil (Apache)     research/sources/open-pencil/LICENSES/Apache-2.0.txt                 11,560  3ddf9be5c28fe27dad143a5dc76eea25222ad1dd68934a047064e56ed2fa40c5  Class B (Apache-2.0 Text)
13 open-pencil (MIT)        research/sources/open-pencil/LICENSES/MIT.txt                         1,121  8ddd3124beb01b4a41d405607829ca33404cb4adbe05c0fecfe21c754fd27158  Class A (MIT Text)
13 open-pencil (Candidate)  research/sources/open-pencil/skills/open-pencil/LICENSE.txt           1,093  a4b377fc000d454305551d65be0f2dd55cc55657846af39465bf55fc414764c4  Class A (Candidate MIT)
14 public-apis              research/sources/public-apis/LICENSE                                  1,089  71236c06f05cc570aa6b12c42d14bdcd4896517e1af7afa34b3ba42c08c8ab63  Class A (MIT)
15 scroll-craft             research/sources/scroll-craft/LICENSE                                 1,087  0333ae139466b1a84b10b415847479b5000d01378932c9ea96d5771b2ce3d1cf  Class A (MIT)
16 security-audit-skill     research/sources/security-audit-skill/LICENSE                         1,099  c007a58f958f8a5b2870aa35d8a17aa72a546447aecee6d2b72e19fea530890b  Class A (MIT)
17 Soup                     research/sources/Soup/LICENSE                                        11,560  3ddf9be5c28fe27dad143a5dc76eea25222ad1dd68934a047064e56ed2fa40c5  Class B (Apache-2.0)
17 Soup                     research/sources/Soup/NOTICE                                             65  735b8b261b303dd72b1996699d21f0152af2849ce473b723bcc7d0117c97eddd  Class B (Apache-2.0 NOTICE)
18 taste-skill              research/sources/taste-skill/LICENSE                                  1,086  3c9f63518df3378772203cc64d38d9e381d2a4723b93d2c3849b2bf3d464de0c  Class A (MIT)
19 unslop                   research/sources/unslop/LICENSE                                      19,053  d07988f4be47912f75a73b44da8a9c0b602bf6c8ced69de858b848f379ecd973  Class C (CC-BY-4.0)
========================================================================================================================================================================================
```

### 6.2. Third-Party Provenance and Licensing Risk Evidence Files

The following files are **not** legal notices or license texts, but non-legal assets inspected directly to establish third-party provenance, unlicensed code, or asset-level licensing risk:

```
========================================================================================================================================================================================
THIRD-PARTY PROVENANCE & LICENSING RISK EVIDENCE LEDGER (Non-Legal Files Directly Inspected for Risk Analysis)
========================================================================================================================================================================================
Repo ID / Entity               Exact Repository-Relative File Path                                   Bytes  SHA-256 Checksum (Binary Mode)                                    Asset Type & Licensing Risk Classification
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
11 impeccable (Risk Evidence)  research/sources/impeccable/.agents/skills/impeccable/scripts/modern-screenshot.umd.js
                                                                                                    29,304  9b0dc34415466edac6e6802574006608b5e5c0da9fdcb7b2651dbd1ea06713a6  Uncredited Minified JS Bundle (Stripped MIT headers; mandatory physical exclusion)
03 archify (Risk Evidence)     research/sources/archify/archify/renderers/shared/generated-brand-marks.mjs
                                                                                                   163,612  0f157d229c12df6f53763a3b88684baa5803a52484c49c4d34ec40b8743beea2  Embedded Data Module (Contains CC-BY-NC-SA & CC-BY-SA marks; requires module sanitization)
========================================================================================================================================================================================
```

### 6.3. Evidentiary Boundaries & Maintenance Rules
1. **Directly Verified Facts**: The file existence, exact byte counts, and cryptographic SHA-256 hashes tabulated above represent direct physical facts verified against the locked repository checkouts.
2. **Reasonable Interpretations**: Applying standard open-source directory conventions (e.g. treating local `LICENSE` files as governing subfolders) and identifying Section 4(b) triggers represent standard legal interpretations.
3. **Unresolved Questions & Unverified Externals**:
   - `ehmo/platform-design-skills`: The original repository was not cloned in `research/sources/`. The statutory MIT notice text remains unverified locally, and derivative work status has not been legally resolved.
   - `simplify-codebase`: Contributor provenance ("simplify-codebase contributors") is unconfirmed in upstream repository metadata.
   - `archify` Brand Marks: Third-party trademark permissions cannot be established by open-source copyright licenses alone, and post-sanitization runtime validation remains required.
4. **Maintenance Standard**: Future updates to skills or upstream commit checkouts must recompute these exact hashes to prevent silent drift.

---

## 7. Final Clearance Register

Every candidate from `manifests/manifest.yaml` appears **exactly once** in the final clearance register.

> [!IMPORTANT]
> This register establishes **licensing clearance tiers and mandatory packaging prerequisites**. It does **NOT** grant actual redistribution approval. All candidates remain classified in `manifests/manifest.yaml` as provisional research candidates until Phase 2 packaging and formal project sign-off.

> [!NOTE]
> **Candidate Scope Boundary for Tier 1**: The classification **Tier 1: Standard Permissive Licence — No Additional Licensing Blocker Identified** applies strictly to the reviewed candidate distribution scope, not to every file that might ever be included in the candidate's upstream repository or directory tree. An upstream repository's MIT license does not automatically establish the provenance or licensing of every embedded or bundled third-party component (as demonstrated by the asset-level analyses of `archify` and `impeccable`). Within the reviewed candidate packaging boundaries, no additional licensing blockers were identified.

```
========================================================================================================================
FINAL REDISTRIBUTION CLEARANCE REGISTER (13 Manifest Candidates)
========================================================================================================================
Candidate Identifier Canonical Skill Name           Clearance Classification Mandatory Packaging Prerequisites
------------------------------------------------------------------------------------------------------------------------
SKILL08-SEC-001      security-audit                 Tier 1: Standard         Retain Cloudflare, Inc. copyright notice.
                                                    Permissive Licence —     Bundle standard MIT license text.
                                                    No Additional Licensing  (Scope strictly restricted to candidate bundle).
                                                    Blocker Identified
------------------------------------------------------------------------------------------------------------------------
SKILL08-DOC-001      humanizer                      Tier 1: Standard         Retain Siqi Chen copyright notice.
                                                    Permissive Licence —     Bundle standard MIT license text.
                                                    No Additional Licensing  (Scope strictly restricted to candidate bundle).
                                                    Blocker Identified
------------------------------------------------------------------------------------------------------------------------
SKILL08-UI-002       hallmark                       Tier 1: Standard         Retain Hallmark contributors copyright notice.
                                                    Permissive Licence —     Bundle standard MIT license text.
                                                    No Additional Licensing  (Scope strictly restricted to candidate bundle).
                                                    Blocker Identified
------------------------------------------------------------------------------------------------------------------------
SKILL08-FE-001       design-taste-frontend          Tier 1: Standard         Retain Leonxlnx copyright notice.
                                                    Permissive Licence —     Bundle standard MIT license text.
                                                    No Additional Licensing  (Scope strictly restricted to candidate bundle).
                                                    Blocker Identified
------------------------------------------------------------------------------------------------------------------------
SKILL08-SWE-001      code-simplification            Tier 1: Standard         Retain Addy Osmani copyright notice.
                                                    Permissive Licence —     Bundle standard MIT license text.
                                                    No Additional Licensing  (Scope strictly restricted to candidate bundle).
                                                    Blocker Identified
------------------------------------------------------------------------------------------------------------------------
SKILL08-TST-001      browser-testing-with-devtools  Tier 1: Standard         Retain Addy Osmani copyright notice.
                                                    Permissive Licence —     Bundle standard MIT license text.
                                                    No Additional Licensing  (Scope strictly restricted to candidate bundle).
                                                    Blocker Identified
------------------------------------------------------------------------------------------------------------------------
SKILL08-SWE-003      debugging-and-error-recovery   Tier 1: Standard         Retain Addy Osmani copyright notice.
                                                    Permissive Licence —     Bundle standard MIT license text.
                                                    No Additional Licensing  (Scope strictly restricted to candidate bundle).
                                                    Blocker Identified
------------------------------------------------------------------------------------------------------------------------
SKILL08-FE-002       scroll-craft                   Tier 1: Standard         Retain Nate Herk copyright notice.
                                                    Permissive Licence —     Bundle standard MIT license text.
                                                    No Additional Licensing  (Scope strictly restricted to candidate bundle).
                                                    Blocker Identified
------------------------------------------------------------------------------------------------------------------------
SKILL08-SWE-002      simplify-codebase              Tier 2: Conditional ClearMust bundle local MIT license; retain contributors notice.
                                                                             Subject to scope & contributor provenance confirmation.
------------------------------------------------------------------------------------------------------------------------
SKILL08-UI-001       unslop                         Tier 2: Conditional ClearMust attribute Damir Sokolovsky and link to CC-BY-4.0.
                                                                             MANDATORY Section 3(a)(1)(B) affirmative modification notice.
------------------------------------------------------------------------------------------------------------------------
SKILL08-UI-003       impeccable                     Tier 3: Restricted Clear UNMODIFIED UPSTREAM NOT DISTRIBUTABLE.
                                                                             Held under Tier 3 restricted clearance pending ehmo resolution.
                                                                             Reference files (reference/ios.md, reference/android.md)
                                                                             must not be redistributed until original MIT notice and
                                                                             derivative rights are verified or excluded.
                                                                             Must physically excise scripts/ directory.
                                                                             Must bundle Apache 2.0 and NOTICE.md.
                                                                             Must include Apache Section 4(b) modification notices.
------------------------------------------------------------------------------------------------------------------------
SKILL08-ARC-001      archify                        Tier 3: Restricted Clear UNMODIFIED UPSTREAM NOT DISTRIBUTABLE.
                                                                             Must sanitize generated-brand-marks.mjs preserving import path
                                                                             (exporting empty/permissive array, excising NC/SA marks).
                                                                             Sanitize or omit brand-marks/catalog.json accordingly.
                                                                             Must bundle Apache 2.0, NOTICE, THIRD_PARTY, OFL, & Pele MIT.
                                                                             Must include Apache Section 4(b) modification notices.
                                                                             Requires runtime and package validation post-sanitization.
------------------------------------------------------------------------------------------------------------------------
SKILL08-UI-004       open-pencil                    Tier 4: Deferred Clear   OPERATIONALLY DEFERRED TO v0.2+ (Group B).
                                                                             Licensing clear under MIT; deferred due to runtime binary.
========================================================================================================================
```

*Clearance Register Verification*:
- **Tier 1 (Standard Permissive Licence — No Additional Licensing Blocker Identified)**: 8 candidates (Reviewed candidate distribution scope strictly defined).
- **Tier 2 (Conditional Clearance)**: 2 candidates.
- **Tier 3 (Restricted Clearance)**: 2 candidates (Pending resolution of `ehmo` evidence or mandatory module sanitization).
- **Tier 4 (Deferred Clearance)**: 1 candidate.
- **Total Registered Candidates**: $8 + 2 + 2 + 1 = 13 \text{ Candidates}$ ($100\%$ accounted for, zero duplicates, zero omissions).
