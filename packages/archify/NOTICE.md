# Skills08 Package Attribution Notice: archify

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
