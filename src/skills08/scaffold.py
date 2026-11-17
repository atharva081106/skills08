"""
Skill scaffolding and authoring tool for Skills08.
Generates compliant Google Antigravity / Agent skill directories with standard SKILL.md.
"""

import re
from pathlib import Path
from typing import Tuple, List, Optional

class SkillScaffolder:
    """Creates standardized, production-ready AI agent skill templates."""

    VALID_NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

    @classmethod
    def validate_name(cls, name: str) -> Tuple[bool, str]:
        """Validate that skill name matches Antigravity kebab-case naming conventions."""
        if not name or not name.strip():
            return False, "Skill name cannot be empty."
        cleaned = name.strip()
        if not cls.VALID_NAME_PATTERN.match(cleaned):
            return False, (
                f"Invalid skill name '{cleaned}'. "
                "Names must be lowercase kebab-case (e.g., 'react-refactor', 'data-pipeline')."
            )
        if len(cleaned) < 2 or len(cleaned) > 64:
            return False, "Skill name must be between 2 and 64 characters in length."
        return True, ""

    @classmethod
    def scaffold(
        cls,
        name: str,
        destination_dir: Path,
        description: Optional[str] = None,
        author: Optional[str] = None,
        category: Optional[str] = None,
        with_subdirs: bool = True
    ) -> Tuple[bool, str, Path]:
        """
        Scaffold a new skill directory with a standard compliant SKILL.md.
        """
        valid, err = cls.validate_name(name)
        if not valid:
            return False, err, destination_dir

        skill_dir = destination_dir / name
        if skill_dir.exists():
            return False, f"Directory already exists at {skill_dir}", skill_dir

        try:
            skill_dir.mkdir(parents=True, exist_ok=True)

            desc = description or f"A specialized agent skill for {name.replace('-', ' ')}."
            auth = author or "Developer"
            cat = category or "General / Productivity"
            display_title = " ".join(word.capitalize() for word in name.split("-"))

            skill_md_content = f"""---
name: {name}
description: {desc}
---

# {display_title}

## Overview
{desc}

## When to Use This Skill
- Activate when the user requests tasks involving {name.replace('-', ' ')}.
- Use for multi-step reasoning, validation, or code generation workflows.
- Do NOT use when simpler direct commands or standard system tools suffice.

## Step-by-Step Instructions

### Step 1: Context Gathering & Discovery
1. Inspect the workspace and target files before proposing modifications.
2. Confirm prerequisites and environment compatibility.

### Step 2: Implementation & Execution
1. Follow standard architectural guidelines and existing conventions.
2. Ensure defensive coding, type safety, and error handling.

### Step 3: Verification & Validation
1. Verify the changes using unit tests or static analysis.
2. Confirm no regressions or broken imports.

## Guidelines & Best Practices
- **Idempotence**: Operations should be repeatable without side effects.
- **Safety**: Do not overwrite critical configurations without user confirmation.
- **Clarity**: Keep explanations concise and actionable.

## Examples

### Example 1: Standard Usage
```bash
# Example invocation or command pattern
skills08 inspect {name}
```

---
*Created with Skills08 CLI by {auth} | Category: {cat}*
"""
            (skill_dir / "SKILL.md").write_text(skill_md_content, encoding="utf-8")

            if with_subdirs:
                examples_dir = skill_dir / "examples"
                examples_dir.mkdir(exist_ok=True)
                (examples_dir / "sample.md").write_text(
                    f"# Example Guide for {display_title}\n\nAdd reference walkthroughs here.\n",
                    encoding="utf-8"
                )

                refs_dir = skill_dir / "references"
                refs_dir.mkdir(exist_ok=True)
                (refs_dir / "spec.md").write_text(
                    f"# Reference Specifications for {display_title}\n\nAdd technical documentation here.\n",
                    encoding="utf-8"
                )

            return True, f"Successfully created skill scaffold at {skill_dir}", skill_dir

        except Exception as e:
            return False, f"Failed to scaffold skill: {e}", skill_dir
