"""
Agent integration and workspace initialization manager.
Configures workspaces for Google Antigravity, Cursor, Claude Code, and Gemini CLI.
"""

import json
from pathlib import Path
from typing import Dict, Any, Tuple

from .constants import DEFAULT_PROJECT_SCOPE

class AgentConfigManager:
    """Configures project directories for seamless AI agent skill discovery."""

    @classmethod
    def init_workspace(cls, workspace_root: Path) -> Tuple[bool, str, Dict[str, Any]]:
        """Initialize standard .agents structure and configuration files in a target workspace."""
        try:
            ws = workspace_root.resolve()
            agents_dir = ws / ".agents"
            skills_dir = ws / DEFAULT_PROJECT_SCOPE

            agents_dir.mkdir(parents=True, exist_ok=True)
            skills_dir.mkdir(parents=True, exist_ok=True)

            # 1. Write or update .agents/skills.json manifest index
            config_file = agents_dir / "skills.json"
            config_data = {
                "version": "1.0.0",
                "manager": "skills08",
                "skills_directory": "skills",
                "supported_agents": [
                    "Google Antigravity",
                    "Claude Code",
                    "Cursor",
                    "Gemini CLI"
                ],
                "description": "Skills08 agent capability index for local workspace."
            }
            if not config_file.exists():
                config_file.write_text(json.dumps(config_data, indent=2), encoding="utf-8")

            # 2. Write .agents/.gitignore to prevent staging artifacts from committing
            gitignore_file = agents_dir / ".gitignore"
            if not gitignore_file.exists():
                gitignore_file.write_text(
                    "# Skills08 temporary staging and runtime caches\n"
                    ".skills08_staging_*\n"
                    "*.tmp\n"
                    "__pycache__/\n",
                    encoding="utf-8"
                )

            # 3. Create a README.md in .agents/ explaining the skill architecture
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

            return True, f"Initialized AI agent workspace at {ws}", {
                "workspace_root": str(ws),
                "agents_directory": str(agents_dir),
                "skills_directory": str(skills_dir),
                "config_file": str(config_file)
            }

        except Exception as e:
            return False, f"Failed to initialize workspace: {e}", {}
