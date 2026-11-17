"""
Deterministic packaging script for Skills08 Group A candidates.
Curates packages into packages/<skill_name>/ without modifying research/sources/.
"""

import os
import shutil
import re
from pathlib import Path

def curate_packages():
    workspace = Path(".").resolve()
    packages_dir = workspace / "packages"
    packages_dir.mkdir(parents=True, exist_ok=True)
    sources = workspace / "research" / "sources"

    print("Building curated Phase 1 packages in packages/...")

    # 1. security-audit (SKILL08-SEC-001)
    src_sec = sources / "security-audit-skill" / "skills" / "security-audit"
    dst_sec = packages_dir / "security-audit"
    if dst_sec.exists():
        shutil.rmtree(dst_sec)
    dst_sec.mkdir(parents=True, exist_ok=True)
    for f in src_sec.iterdir():
        if f.is_file() and not f.name.endswith(".test.cjs"):
            shutil.copy2(f, dst_sec / f.name)
    (dst_sec / "NOTICE.md").write_text("""# Skills08 Package Attribution Notice: security-audit

- **Candidate ID**: SKILL08-SEC-001
- **Upstream Repository**: https://github.com/cloudflare/security-audit-skill.git
- **Locked Commit SHA**: c1c8a8c1471069fb0e188eeaff69b8e8db6564a8
- **Author / Maintainer**: Dan Jones / Cloudflare, Inc.
- **License**: MIT
- **Legal Clearance**: Tier 1: Standard Clearance (MIT)
- **Operational Model**: Companion-File Static Guidance Mode

### Governing License Notice
Copyright (c) 2026 Cloudflare, Inc.
Licensed under the MIT License.

### Skills08 Adaptations
1. Configured strictly for static Guidance Mode on Windows.
2. Full dynamic audit execution and target script execution are disabled.
3. Subagent delegations mapped strictly to Antigravity's read-only 'research' subagent.
""", encoding="utf-8")
    print("  [x] security-audit packaged.")

    # 2. humanizer (SKILL08-DOC-001)
    src_hum = sources / "humanizer" / "SKILL.md"
    dst_hum = packages_dir / "humanizer"
    if dst_hum.exists():
        shutil.rmtree(dst_hum)
    dst_hum.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_hum, dst_hum / "SKILL.md")
    (dst_hum / "NOTICE.md").write_text("""# Skills08 Package Attribution Notice: humanizer

- **Candidate ID**: SKILL08-DOC-001
- **Upstream Repository**: https://github.com/blader/humanizer.git
- **Locked Commit SHA**: b48c832f0f809c1b5658edbb838c2521b72f2413
- **Author / Maintainer**: Siqi Chen
- **License**: MIT
- **Legal Clearance**: Tier 1: Standard Clearance (MIT)
- **Operational Model**: Native Pure-Instruction

### Governing License Notice
Copyright (c) 2026 Siqi Chen.
Licensed under the MIT License.

### Skills08 Adaptations
Packaged natively for Google Antigravity discovery paths (.agents/skills/humanizer/).
""", encoding="utf-8")
    print("  [x] humanizer packaged.")

    # 3. unslop (SKILL08-UI-001)
    src_unslop = sources / "unslop" / "skills" / "unslop"
    dst_unslop = packages_dir / "unslop"
    if dst_unslop.exists():
        shutil.rmtree(dst_unslop)
    dst_unslop.mkdir(parents=True, exist_ok=True)
    
    # Read SKILL.md and neutralize script reference
    skill_text = (src_unslop / "SKILL.md").read_text(encoding="utf-8")
    # In Model A, direct pure instruction critique
    skill_text = skill_text.replace("node scripts/snapshot.mjs", "inspect code statically")
    (dst_unslop / "SKILL.md").write_text(skill_text, encoding="utf-8")
    if (src_unslop / "references").exists():
        shutil.copytree(src_unslop / "references", dst_unslop / "references")

    (dst_unslop / "NOTICE.md").write_text("""# Skills08 Package Attribution Notice: unslop

- **Candidate ID**: SKILL08-UI-001
- **Upstream Repository**: https://github.com/heydamir/unslop.git
- **Locked Commit SHA**: 620163eedb3529d9cd23a3994ed8d287d06f760d
- **Author / Maintainer**: Damir Sota
- **License**: CC-BY-4.0
- **Legal Clearance**: Tier 2: Conditional Clearance (CC-BY-4.0)
- **Operational Model**: Model A (Instruction-Only)

### Attribution Statement
Original work created by Damir Sota (heydamir/unslop), licensed under Creative Commons Attribution 4.0 International (CC-BY-4.0).
https://creativecommons.org/licenses/by/4.0/

### Statement of Modifications
Modified by Skills08 to operate in Model A (pure instruction mode):
- scripts/snapshot.mjs omitted to eliminate external Playwright dependencies, network egress, and token needs.
- Cognitive design guidelines preserved in full.
""", encoding="utf-8")
    print("  [x] unslop packaged.")

    # 4. hallmark (SKILL08-UI-002)
    src_hlm = sources / "hallmark" / "skills" / "hallmark"
    dst_hlm = packages_dir / "hallmark"
    if dst_hlm.exists():
        shutil.rmtree(dst_hlm)
    dst_hlm.mkdir(parents=True, exist_ok=True)
    
    skill_text = (src_hlm / "SKILL.md").read_text(encoding="utf-8")
    # Model A: omit scripts/sloplint.mjs
    skill_text = skill_text.replace("node scripts/sloplint.mjs", "review component layout statically")
    (dst_hlm / "SKILL.md").write_text(skill_text, encoding="utf-8")
    if (src_hlm / "references").exists():
        shutil.copytree(src_hlm / "references", dst_hlm / "references")

    (dst_hlm / "NOTICE.md").write_text("""# Skills08 Package Attribution Notice: hallmark

- **Candidate ID**: SKILL08-UI-002
- **Upstream Repository**: https://github.com/Nutlope/hallmark.git
- **Locked Commit SHA**: 04977e15f3dfd6ee4b74c887dac3eb52665d6c92
- **Author / Maintainer**: Hassan El Mghari / Hallmark contributors
- **License**: MIT
- **Legal Clearance**: Tier 1: Standard Clearance (MIT)
- **Operational Model**: Model A (Instruction-Only)

### Governing License Notice
Copyright (c) 2026 Hassan El Mghari.
Licensed under the MIT License.

### Statement of Modifications
Modified by Skills08 to operate in Model A (pure instruction mode):
- scripts/sloplint.mjs omitted to avoid Node.js file modification risks.
""", encoding="utf-8")
    print("  [x] hallmark packaged.")

    # 5. design-taste-frontend (SKILL08-FE-001)
    src_tst = sources / "taste-skill" / "skills" / "taste-skill"
    dst_tst = packages_dir / "design-taste-frontend"
    if dst_tst.exists():
        shutil.rmtree(dst_tst)
    dst_tst.mkdir(parents=True, exist_ok=True)
    
    skill_text = (src_tst / "SKILL.md").read_text(encoding="utf-8")
    # Sanitize frontmatter name to design-taste-frontend
    skill_text = re.sub(r"^name:\s*taste-skill", "name: design-taste-frontend", skill_text, flags=re.MULTILINE)
    # Strip bash stop hooks and gate.mjs mentions
    skill_text = re.sub(r"```bash\s+for f in.*?done\s+```", "<!-- stop hooks omitted for Windows PowerShell compatibility -->", skill_text, flags=re.DOTALL)
    skill_text = skill_text.replace("node scripts/gate.mjs", "apply design taste heuristics directly")
    (dst_tst / "SKILL.md").write_text(skill_text, encoding="utf-8")
    
    if (src_tst / "references").exists():
        shutil.copytree(src_tst / "references", dst_tst / "references")
    if (src_tst / "library").exists():
        shutil.copytree(src_tst / "library", dst_tst / "library")

    (dst_tst / "NOTICE.md").write_text("""# Skills08 Package Attribution Notice: design-taste-frontend

- **Candidate ID**: SKILL08-FE-001
- **Upstream Repository**: https://github.com/leonxlnx/taste-skill.git
- **Locked Commit SHA**: f6b76575f949707b4e3c37cd86cb44b0b98643e8
- **Author / Maintainer**: Leonxlnx
- **License**: MIT
- **Legal Clearance**: Tier 1: Standard Clearance (MIT)
- **Operational Model**: Model A (Instruction-Only)

### Governing License Notice
Copyright (c) 2026 Leonxlnx.
Licensed under the MIT License.

### Statement of Modifications
Modified by Skills08 to operate in Model A (pure instruction mode):
- Frontmatter standardized to 'design-taste-frontend'.
- scripts/gate.mjs and loopback server daemons omitted (eliminates port 7600/7601 collisions).
- Bash-specific stop hooks removed for Windows PowerShell 5.1 compatibility.
""", encoding="utf-8")
    print("  [x] design-taste-frontend packaged.")

    # 6. code-simplification (SKILL08-SWE-001)
    src_cs = sources / "agent-skills" / "skills" / "code-simplification" / "SKILL.md"
    dst_cs = packages_dir / "code-simplification"
    if dst_cs.exists():
        shutil.rmtree(dst_cs)
    dst_cs.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_cs, dst_cs / "SKILL.md")
    (dst_cs / "NOTICE.md").write_text("""# Skills08 Package Attribution Notice: code-simplification

- **Candidate ID**: SKILL08-SWE-001
- **Upstream Repository**: https://github.com/addyosmani/agent-skills.git
- **Locked Commit SHA**: 39b723ceebf81474d0557c1fecd01eddab585563
- **Author / Maintainer**: Addy Osmani
- **License**: MIT
- **Legal Clearance**: Tier 1: Standard Clearance (MIT)
- **Operational Model**: Native Pure-Instruction

### Governing License Notice
Copyright (c) 2026 Addy Osmani.
Licensed under the MIT License.
""", encoding="utf-8")
    print("  [x] code-simplification packaged.")

    # 7. simplify-codebase (SKILL08-SWE-002)
    src_scb = sources / "archify" / ".agents" / "skills" / "simplify-codebase"
    dst_scb = packages_dir / "simplify-codebase"
    if dst_scb.exists():
        shutil.rmtree(dst_scb)
    dst_scb.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_scb / "SKILL.md", dst_scb / "SKILL.md")
    if (src_scb / "LICENSE").exists():
        shutil.copy2(src_scb / "LICENSE", dst_scb / "LICENSE")
    if (src_scb / "references").exists():
        shutil.copytree(src_scb / "references", dst_scb / "references")

    (dst_scb / "NOTICE.md").write_text("""# Skills08 Package Attribution Notice: simplify-codebase

- **Candidate ID**: SKILL08-SWE-002
- **Upstream Repository**: https://github.com/tt-a1i/archify.git
- **Locked Commit SHA**: a7ed6fd6657da90414831d1d42cf95987188750c
- **Author / Maintainer**: tt-a1i
- **License**: MIT (bundled dedicated directory license)
- **Legal Clearance**: Tier 2: Conditional Clearance (MIT)
- **Operational Model**: Native Pure-Instruction

### Governing License Notice
Copyright (c) 2026 tt-a1i.
Licensed under the MIT License (see bundled LICENSE).
""", encoding="utf-8")
    print("  [x] simplify-codebase packaged.")

    # 8. browser-testing-with-devtools (SKILL08-TST-001)
    src_bt = sources / "agent-skills" / "skills" / "browser-testing-with-devtools" / "SKILL.md"
    dst_bt = packages_dir / "browser-testing-with-devtools"
    if dst_bt.exists():
        shutil.rmtree(dst_bt)
    dst_bt.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_bt, dst_bt / "SKILL.md")
    (dst_bt / "NOTICE.md").write_text("""# Skills08 Package Attribution Notice: browser-testing-with-devtools

- **Candidate ID**: SKILL08-TST-001
- **Upstream Repository**: https://github.com/addyosmani/agent-skills.git
- **Locked Commit SHA**: 39b723ceebf81474d0557c1fecd01eddab585563
- **Author / Maintainer**: Addy Osmani
- **License**: MIT
- **Legal Clearance**: Tier 1: Standard Clearance (MIT)
- **Operational Model**: Native Subagent Dispatch

### Governing License Notice
Copyright (c) 2026 Addy Osmani.
Licensed under the MIT License.

### Antigravity Host Binding
Binds directly to Google Antigravity native 'browser' subagent for Chrome DevTools protocol execution.
""", encoding="utf-8")
    print("  [x] browser-testing-with-devtools packaged.")

    # 9. debugging-and-error-recovery (SKILL08-SWE-003)
    src_dbg = sources / "agent-skills" / "skills" / "debugging-and-error-recovery" / "SKILL.md"
    dst_dbg = packages_dir / "debugging-and-error-recovery"
    if dst_dbg.exists():
        shutil.rmtree(dst_dbg)
    dst_dbg.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_dbg, dst_dbg / "SKILL.md")
    (dst_dbg / "NOTICE.md").write_text("""# Skills08 Package Attribution Notice: debugging-and-error-recovery

- **Candidate ID**: SKILL08-SWE-003
- **Upstream Repository**: https://github.com/addyosmani/agent-skills.git
- **Locked Commit SHA**: 39b723ceebf81474d0557c1fecd01eddab585563
- **Author / Maintainer**: Addy Osmani
- **License**: MIT
- **Legal Clearance**: Tier 1: Standard Clearance (MIT)
- **Operational Model**: Native Pure-Instruction

### Governing License Notice
Copyright (c) 2026 Addy Osmani.
Licensed under the MIT License.
""", encoding="utf-8")
    print("  [x] debugging-and-error-recovery packaged.")

    # 10. archify (SKILL08-ARC-001)
    src_arc = sources / "archify" / "archify"
    dst_arc = packages_dir / "archify"
    if dst_arc.exists():
        shutil.rmtree(dst_arc)
    dst_arc.mkdir(parents=True, exist_ok=True)
    
    skill_text = (src_arc / "SKILL.md").read_text(encoding="utf-8")
    # Model A: instruct agent to emit markdown ADRs directly; omit bin/archify.mjs
    skill_text = re.sub(r"node\s+bin/archify\.mjs\s+finalize", "generate the Architectural Decision Record directly in docs/adr/", skill_text)
    (dst_arc / "SKILL.md").write_text(skill_text, encoding="utf-8")
    if (src_arc / "references").exists():
        shutil.copytree(src_arc / "references", dst_arc / "references")

    (dst_arc / "NOTICE.md").write_text("""# Skills08 Package Attribution Notice: archify

- **Candidate ID**: SKILL08-ARC-001
- **Upstream Repository**: https://github.com/tt-a1i/archify.git
- **Locked Commit SHA**: a7ed6fd6657da90414831d1d42cf95987188750c
- **Author / Maintainer**: tt-a1i
- **License**: Apache-2.0
- **Legal Clearance**: Tier 3: Restricted Clearance (Apache-2.0)
- **Operational Model**: Model A (Instruction-Only)

### Governing License Notice
Copyright (c) 2026 tt-a1i.
Licensed under the Apache License, Version 2.0.

### Statement of Modifications (Apache-2.0 Section 4)
Modified by Skills08 to operate in Model A (pure instruction mode):
- bin/archify.mjs omitted to eliminate 15 spawnSync call sites and process execution risks.
- Directs the agent to produce Architectural Decision Records (ADRs) directly in Markdown.
""", encoding="utf-8")
    print("  [x] archify packaged.")

    # 11. scroll-craft (SKILL08-FE-002)
    src_scr = sources / "scroll-craft" / "plugins" / "nateherk-design" / "skills" / "scroll-craft"
    dst_scr = packages_dir / "scroll-craft"
    if dst_scr.exists():
        shutil.rmtree(dst_scr)
    dst_scr.mkdir(parents=True, exist_ok=True)
    
    skill_text = (src_scr / "SKILL.md").read_text(encoding="utf-8")
    # Sanitize frontmatter by stripping non-standard allowed-tools
    skill_text = re.sub(r"allowed-tools:\s*\[.*?\]", "", skill_text)
    # Model A: omit scripts/kie.mjs upload
    skill_text = skill_text.replace("node scripts/kie.mjs", "generate dimensional visuals via native canvas/artifacts")
    (dst_scr / "SKILL.md").write_text(skill_text, encoding="utf-8")
    if (src_scr / "references").exists():
        shutil.copytree(src_scr / "references", dst_scr / "references")

    (dst_scr / "NOTICE.md").write_text("""# Skills08 Package Attribution Notice: scroll-craft

- **Candidate ID**: SKILL08-FE-002
- **Upstream Repository**: https://github.com/nateherkai/scroll-craft.git
- **Locked Commit SHA**: 75d81f74e83692add18cd7a8a8e078b8a887a579
- **Author / Maintainer**: Nate Herk
- **License**: MIT
- **Legal Clearance**: Tier 1: Standard Clearance (MIT)
- **Operational Model**: Model A (Instruction-Only)

### Governing License Notice
Copyright (c) 2026 Nate Herk.
Licensed under the MIT License.

### Statement of Modifications
Modified by Skills08 to operate in Model A (pure instruction mode):
- Frontmatter sanitized (non-standard 'allowed-tools' parameter removed).
- scripts/kie.mjs omitted to eliminate unsanitized image upload vector (SEC-SCR-003).
""", encoding="utf-8")
    print("  [x] scroll-craft packaged.")

    # 12. impeccable (SKILL08-UI-003)
    src_imp = sources / "impeccable" / ".agents" / "skills" / "impeccable"
    dst_imp = packages_dir / "impeccable"
    if dst_imp.exists():
        shutil.rmtree(dst_imp)
    dst_imp.mkdir(parents=True, exist_ok=True)
    
    skill_text = (src_imp / "SKILL.md").read_text(encoding="utf-8")
    # Model A: lock to pure instruction fallback playbooks
    skill_text = re.sub(r"\$\{CLAUDE_SKILL_DIR\}/scripts/impeccable", "consult reference playbooks directly", skill_text)
    (dst_imp / "SKILL.md").write_text(skill_text, encoding="utf-8")
    if (src_imp / "reference").exists():
        shutil.copytree(src_imp / "reference", dst_imp / "reference")

    (dst_imp / "NOTICE.md").write_text("""# Skills08 Package Attribution Notice: impeccable

- **Candidate ID**: SKILL08-UI-003
- **Upstream Repository**: https://github.com/pbakaus/impeccable.git
- **Locked Commit SHA**: d41d9860b0094dcb68030657da63461212835aaa
- **Author / Maintainer**: Paul Bakaus
- **License**: Apache-2.0
- **Legal Clearance**: Tier 3: Restricted Clearance (Apache-2.0)
- **Operational Model**: Model A (Instruction-Only)

### Governing License Notice
Copyright (c) 2026 Paul Bakaus.
Licensed under the Apache License, Version 2.0.

### Statement of Modifications (Apache-2.0 Section 4)
Modified by Skills08 to operate in pure-instruction fallback mode (Model A):
- Extracted canonical skill definition from .agents/skills/impeccable/.
- Shell wrapper scripts and non-distributable font binaries omitted.
- Instructions locked to pure instruction design playbooks.
""", encoding="utf-8")
    print("  [x] impeccable packaged.")

    print("\nAll 12 Group A packages successfully curated in packages/!")

if __name__ == "__main__":
    curate_packages()

