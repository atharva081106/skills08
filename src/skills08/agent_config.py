"""
Universal Multi-Agent Integration and Workspace Manager.
Enables Skills08 skills to work seamlessly across every major AI coding agent:
- Google Antigravity (.agents/skills/ and GEMINI.md)
- Cursor (.cursor/rules/*.mdc and .cursorrules)
- Claude Code (CLAUDE.md and .claude/skills/)
- GitHub Copilot (.github/copilot-instructions.md)
- Windsurf (.windsurfrules)
- Cline / Roo Code (.clinerules)
- Universal Agents standard (AGENTS.md)
"""

import re
import json
import shutil
from pathlib import Path
from typing import Dict, Any, Tuple, List, Optional

from .constants import DEFAULT_PROJECT_SCOPE

MANAGED_START_TAG = "<!-- BEGIN SKILLS08 MANAGED BLOCK -->"
MANAGED_END_TAG = "<!-- END SKILLS08 MANAGED BLOCK -->"

SUPPORTED_AGENTS = [
    "antigravity",
    "cursor",
    "claude",
    "copilot",
    "windsurf",
    "cline",
    "gemini",
    "agents_md"
]

class AgentConfigManager:
    """Configures project directories and projects skills to every AI coding agent."""

    @classmethod
    def _extract_frontmatter(cls, skill_md_content: str) -> Tuple[Dict[str, str], str]:
        """Extract YAML frontmatter and body from SKILL.md."""
        fm = {}
        body = skill_md_content
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", skill_md_content, re.DOTALL)
        if match:
            fm_text = match.group(1)
            body = match.group(2)
            for line in fm_text.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip()] = v.strip().strip("'\"")
        return fm, body

    @classmethod
    def _update_managed_file(cls, file_path: Path, new_managed_content: str, default_header: str) -> None:
        """Safely update or insert a managed block inside an instructions file, preserving user edits."""
        managed_block = (
            f"{MANAGED_START_TAG}\n"
            f"<!-- Automatically managed by Skills08. Do not edit inside this block. -->\n\n"
            f"{new_managed_content.strip()}\n\n"
            f"{MANAGED_END_TAG}\n"
        )

        if not file_path.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)
            content = f"{default_header.strip()}\n\n{managed_block}"
            file_path.write_text(content, encoding="utf-8")
            return

        existing_text = file_path.read_text(encoding="utf-8", errors="replace")
        pattern = re.compile(
            re.escape(MANAGED_START_TAG) + r".*?" + re.escape(MANAGED_END_TAG) + r"\n?",
            re.DOTALL
        )

        if pattern.search(existing_text):
            updated_text = pattern.sub(managed_block, existing_text)
        else:
            updated_text = existing_text.rstrip() + "\n\n" + managed_block

        file_path.write_text(updated_text, encoding="utf-8")

    @classmethod
    def _clean_managed_file(cls, file_path: Path) -> None:
        """Remove the managed block if no skills remain installed."""
        if not file_path.exists():
            return
        existing_text = file_path.read_text(encoding="utf-8", errors="replace")
        pattern = re.compile(
            re.escape(MANAGED_START_TAG) + r".*?" + re.escape(MANAGED_END_TAG) + r"\n?",
            re.DOTALL
        )
        if pattern.search(existing_text):
            cleaned_text = pattern.sub("", existing_text).strip()
            if cleaned_text:
                file_path.write_text(cleaned_text + "\n", encoding="utf-8")
            else:
                # If file only had the managed block, delete it cleanly
                file_path.unlink(missing_ok=True)

    @classmethod
    def init_workspace(
        cls,
        workspace_root: Path,
        agents: Optional[List[str]] = None
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """Initialize workspace directories and scaffolding for all requested AI coding agents."""
        try:
            ws = workspace_root.resolve()
            target_agents = [a.lower() for a in agents] if agents else SUPPORTED_AGENTS

            created_files = []

            # 1. Google Antigravity (.agents/)
            if "antigravity" in target_agents:
                agents_dir = ws / ".agents"
                skills_dir = ws / DEFAULT_PROJECT_SCOPE
                agents_dir.mkdir(parents=True, exist_ok=True)
                skills_dir.mkdir(parents=True, exist_ok=True)

                cfg_file = agents_dir / "skills.json"
                if not cfg_file.exists():
                    cfg_file.write_text(json.dumps({
                        "version": "1.0.0",
                        "manager": "skills08",
                        "supported_agents": [
                            "Google Antigravity",
                            "Cursor",
                            "Claude Code",
                            "GitHub Copilot",
                            "Windsurf",
                            "Cline / Roo Code",
                            "Gemini CLI"
                        ]
                    }, indent=2), encoding="utf-8")
                    created_files.append(str(cfg_file))

                gi_file = agents_dir / ".gitignore"
                if not gi_file.exists():
                    gi_file.write_text(".skills08_staging_*\n*.tmp\n__pycache__/\n", encoding="utf-8")
                    created_files.append(str(gi_file))

                readme_file = agents_dir / "README.md"
                if not readme_file.exists():
                    readme_file.write_text(
                        "# AI Agent Skills Directory\n\n"
                        "This directory contains skills and instructions indexed by AI coding agents\n"
                        "(Google Antigravity, Claude Code, Cursor, Gemini CLI).\n\n"
                        "Skills installed here via `skills08 install <skill-name>` are automatically\n"
                        "discovered and used during project reasoning and development tasks.\n",
                        encoding="utf-8"
                    )
                    created_files.append(str(readme_file))

            # 2. Cursor (.cursor/rules/)
            if "cursor" in target_agents:
                cursor_rules_dir = ws / ".cursor" / "rules"
                cursor_rules_dir.mkdir(parents=True, exist_ok=True)
                readme_cursor = cursor_rules_dir / "README.md"
                if not readme_cursor.exists():
                    readme_cursor.write_text(
                        "# Cursor Rules\n\nSkills managed by Skills08 are projected here as `.mdc` rules.\n",
                        encoding="utf-8"
                    )
                    created_files.append(str(readme_cursor))

            # 3. Claude Code (.claude/skills/)
            if "claude" in target_agents:
                claude_skills_dir = ws / ".claude" / "skills"
                claude_skills_dir.mkdir(parents=True, exist_ok=True)
                claude_md = ws / "CLAUDE.md"
                if not claude_md.exists():
                    claude_md.write_text(
                        "# Project Guidelines for Claude Code\n\nThis project uses Skills08 to manage AI agent skills.\n",
                        encoding="utf-8"
                    )
                    created_files.append(str(claude_md))

            # 4. GitHub Copilot (.github/)
            if "copilot" in target_agents:
                github_dir = ws / ".github"
                github_dir.mkdir(parents=True, exist_ok=True)
                copilot_file = github_dir / "copilot-instructions.md"
                if not copilot_file.exists():
                    copilot_file.write_text(
                        "# GitHub Copilot Custom Instructions\n\nActive skills and coding guidelines.\n",
                        encoding="utf-8"
                    )
                    created_files.append(str(copilot_file))

            # 5. Windsurf (.windsurfrules)
            if "windsurf" in target_agents:
                ws_rules = ws / ".windsurfrules"
                if not ws_rules.exists():
                    ws_rules.write_text(
                        "# Windsurf Cascade Rules\n\nActive skills and project instructions.\n",
                        encoding="utf-8"
                    )
                    created_files.append(str(ws_rules))

            # 6. Cline / Roo Code (.clinerules)
            if "cline" in target_agents:
                cline_rules = ws / ".clinerules"
                if not cline_rules.exists():
                    cline_rules.write_text(
                        "# Cline & Roo Code Project Rules\n\nActive skills and project guidelines.\n",
                        encoding="utf-8"
                    )
                    created_files.append(str(cline_rules))

            # 7. Gemini CLI (GEMINI.md)
            if "gemini" in target_agents:
                gemini_md = ws / "GEMINI.md"
                if not gemini_md.exists():
                    gemini_md.write_text(
                        "# Gemini Coding Guidelines\n\nInstructions for Gemini CLI and Code Assist.\n",
                        encoding="utf-8"
                    )
                    created_files.append(str(gemini_md))

            # 8. Open Universal Standard (AGENTS.md)
            if "agents_md" in target_agents:
                agents_md = ws / "AGENTS.md"
                if not agents_md.exists():
                    agents_md.write_text(
                        "# Open AI Agent Guidelines\n\nUniversal instructions for AI coding agents.\n",
                        encoding="utf-8"
                    )
                    created_files.append(str(agents_md))

            return True, f"Successfully initialized workspace for {len(target_agents)} coding agent(s).", {
                "workspace_root": str(ws),
                "agents_initialized": target_agents,
                "created_files": created_files
            }

        except Exception as e:
            return False, f"Failed to initialize workspace for agents: {e}", {}

    @classmethod
    def sync_all_agents(
        cls,
        workspace_root: Path,
        agents: Optional[List[str]] = None
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Synchronize all currently installed skills across all target AI coding agent configurations.
        """
        ws = workspace_root.resolve()
        skills_dir = ws / DEFAULT_PROJECT_SCOPE
        target_agents = [a.lower() for a in agents] if agents else SUPPORTED_AGENTS

        # Collect all installed skills
        installed_skills: List[Dict[str, Any]] = []
        if skills_dir.exists():
            for item in sorted(skills_dir.iterdir()):
                if item.is_dir() and (item / "SKILL.md").exists():
                    skill_md = item / "SKILL.md"
                    raw_text = skill_md.read_text(encoding="utf-8", errors="replace")
                    fm, body = cls._extract_frontmatter(raw_text)
                    name = fm.get("name", item.name)
                    desc = fm.get("description", f"Skill {name}")

                    installed_skills.append({
                        "name": name,
                        "dir_name": item.name,
                        "description": desc,
                        "skill_dir": item,
                        "body": body,
                        "raw_md": raw_text
                    })

        synced_counts = {agent: 0 for agent in target_agents}

        # 1. Modern Cursor Rules (.cursor/rules/<name>.mdc)
        if "cursor" in target_agents:
            cursor_rules_dir = ws / ".cursor" / "rules"
            cursor_rules_dir.mkdir(parents=True, exist_ok=True)

            # Remove old .mdc files not present in installed skills
            active_names = {s["name"] for s in installed_skills}
            for existing_mdc in cursor_rules_dir.glob("*.mdc"):
                stem = existing_mdc.stem
                if stem not in active_names:
                    existing_mdc.unlink(missing_ok=True)

            # Generate modern .mdc file for each skill
            for s in installed_skills:
                mdc_file = cursor_rules_dir / f"{s['name']}.mdc"
                clean_desc = s['description'].replace('"', '\\"')
                mdc_content = (
                    f"---\n"
                    f"description: \"{clean_desc}\"\n"
                    f"globs: \"*\"\n"
                    f"alwaysApply: false\n"
                    f"---\n\n"
                    f"{s['body'].strip()}\n"
                )
                mdc_file.write_text(mdc_content, encoding="utf-8")
                synced_counts["cursor"] += 1

            # Also maintain .cursorrules for legacy Cursor users
            if installed_skills:
                cursorrules_text = cls._build_summary_instructions(installed_skills)
                cls._update_managed_file(
                    ws / ".cursorrules",
                    cursorrules_text,
                    "# Cursor Rules\n\nProject rules for Cursor IDE."
                )
            else:
                cls._clean_managed_file(ws / ".cursorrules")

        # 2. Claude Code (CLAUDE.md and .claude/skills/)
        if "claude" in target_agents:
            claude_skills_dir = ws / ".claude" / "skills"
            claude_skills_dir.mkdir(parents=True, exist_ok=True)

            # Mirror skills into .claude/skills/
            active_dirs = {s["name"] for s in installed_skills}
            for existing_dir in claude_skills_dir.iterdir():
                if existing_dir.is_dir() and existing_dir.name not in active_dirs:
                    shutil.rmtree(existing_dir, ignore_errors=True)

            for s in installed_skills:
                target_dest = claude_skills_dir / s["name"]
                if not target_dest.exists():
                    target_dest.mkdir(parents=True, exist_ok=True)
                (target_dest / "SKILL.md").write_text(s["raw_md"], encoding="utf-8")
                synced_counts["claude"] += 1

            # Update CLAUDE.md
            claude_md = ws / "CLAUDE.md"
            if installed_skills:
                summary = cls._build_summary_instructions(installed_skills)
                cls._update_managed_file(
                    claude_md,
                    summary,
                    "# Claude Code Instructions\n\nProject guidelines for Claude Code."
                )
            else:
                cls._clean_managed_file(claude_md)

        # 3. GitHub Copilot (.github/copilot-instructions.md)
        if "copilot" in target_agents:
            copilot_file = ws / ".github" / "copilot-instructions.md"
            if installed_skills:
                summary = cls._build_summary_instructions(installed_skills)
                cls._update_managed_file(
                    copilot_file,
                    summary,
                    "# GitHub Copilot Custom Instructions\n\nGuidelines for GitHub Copilot in VS Code / JetBrains."
                )
                synced_counts["copilot"] = len(installed_skills)
            else:
                cls._clean_managed_file(copilot_file)

        # 4. Windsurf (.windsurfrules)
        if "windsurf" in target_agents:
            windsurf_file = ws / ".windsurfrules"
            if installed_skills:
                summary = cls._build_summary_instructions(installed_skills)
                cls._update_managed_file(
                    windsurf_file,
                    summary,
                    "# Windsurf Cascade Rules\n\nCustom rules for Windsurf Cascade agent."
                )
                synced_counts["windsurf"] = len(installed_skills)
            else:
                cls._clean_managed_file(windsurf_file)

        # 5. Cline / Roo Code (.clinerules)
        if "cline" in target_agents:
            cline_file = ws / ".clinerules"
            if installed_skills:
                summary = cls._build_summary_instructions(installed_skills)
                cls._update_managed_file(
                    cline_file,
                    summary,
                    "# Cline & Roo Code Instructions\n\nCustom instructions for Cline / Roo Code."
                )
                synced_counts["cline"] = len(installed_skills)
            else:
                cls._clean_managed_file(cline_file)

        # 6. Gemini CLI (GEMINI.md)
        if "gemini" in target_agents:
            gemini_file = ws / "GEMINI.md"
            if installed_skills:
                summary = cls._build_summary_instructions(installed_skills)
                cls._update_managed_file(
                    gemini_file,
                    summary,
                    "# Gemini Coding Instructions\n\nGuidelines for Gemini CLI and Code Assist."
                )
                synced_counts["gemini"] = len(installed_skills)
            else:
                cls._clean_managed_file(gemini_file)

        # 7. Universal Open Standard (AGENTS.md)
        if "agents_md" in target_agents:
            agents_md_file = ws / "AGENTS.md"
            if installed_skills:
                summary = cls._build_summary_instructions(installed_skills)
                cls._update_managed_file(
                    agents_md_file,
                    summary,
                    "# Open Agent Guidelines\n\nUniversal conventions for AI coding agents."
                )
                synced_counts["agents_md"] = len(installed_skills)
            else:
                cls._clean_managed_file(agents_md_file)

        # 8. Antigravity (.agents/skills/ is already native)
        if "antigravity" in target_agents:
            synced_counts["antigravity"] = len(installed_skills)

        return True, f"Synchronized {len(installed_skills)} active skill(s) across {len(target_agents)} coding agent format(s).", {
            "workspace_root": str(ws),
            "installed_skills_count": len(installed_skills),
            "synced_counts": synced_counts
        }

    @classmethod
    def _build_summary_instructions(cls, skills: List[Dict[str, Any]]) -> str:
        """Construct structured multi-skill instructions for single-file agent configuration."""
        lines = [
            "## Active Skills & Guidelines (Skills08 Managed)",
            "The following cognitive skills and guidelines are active in this workspace. "
            "Follow their instructions and workflows when relevant tasks arise:\n"
        ]

        for s in skills:
            lines.append(f"### Skill: `{s['name']}`")
            lines.append(f"**Description**: {s['description']}\n")
            lines.append(f"**Instructions & Rules**:")
            # Extract main guidelines/instructions, trimming excessive markdown headers
            body_lines = s["body"].strip().splitlines()
            # Include clean excerpt of the instructions
            excerpt = []
            for bl in body_lines:
                if bl.startswith("# "):
                    continue
                excerpt.append(bl)
            lines.append("\n".join(excerpt).strip())
            lines.append("\n---\n")

        return "\n".join(lines)
