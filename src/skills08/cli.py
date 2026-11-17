"""
Command-line interface for Skills08 lifecycle management.
Supports discovery, inspection, search, atomic installation, uninstallation,
integrity verification, conflict detection, scaffolding, packaging, and diagnostics.
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import Optional, List, Dict, Any

from .constants import (
    VERSION,
    EXIT_SUCCESS,
    EXIT_ERROR,
    EXIT_CONFLICT,
    EXIT_VERIFICATION_FAILED,
    EXIT_NOT_FOUND,
    EXIT_INVALID_ARGS
)
from .catalog import Catalog
from .installer import Installer
from .verifier import IntegrityVerifier
from .conflicts import ConflictDetector
from .scaffold import SkillScaffolder
from .packager import SkillPackager
from .doctor import EnvironmentDoctor
from .agent_config import AgentConfigManager

def format_table(headers: list, rows: list) -> str:
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))
    
    fmt = " | ".join(f"{{:<{w}}}" for w in col_widths)
    sep = "-+-".join("-" * w for w in col_widths)
    
    lines = [fmt.format(*headers), sep]
    for row in rows:
        lines.append(fmt.format(*[str(v) for v in row]))
    return "\n".join(lines)

def cmd_list(args, installer: Installer) -> int:
    catalog = installer.catalog
    installed = {s.name: s.scope for s in installer.list_installed()}

    candidates = catalog.candidates
    if getattr(args, "category", None):
        candidates = [c for c in candidates if args.category.lower() in c.category.lower()]
    if getattr(args, "tier", None):
        candidates = [c for c in candidates if args.tier.lower() in c.tier.lower()]

    if getattr(args, "json", False):
        data = []
        for c in candidates:
            data.append({
                "id": c.id,
                "name": c.name,
                "display_name": c.display_name,
                "category": c.category,
                "tier": c.tier,
                "operational_model": c.operational_model,
                "installed_scope": installed.get(c.name, None)
            })
        print(json.dumps(data, indent=2))
        return EXIT_SUCCESS

    print("\n=== Skills08 Phase 1 Candidate Catalog ===\n")
    headers = ["Candidate ID", "Skill Name", "Category", "Tier", "Operational Model", "Installed"]
    rows = []

    for c in candidates:
        inst_status = installed.get(c.name, "No")
        rows.append([c.id, c.name, c.category, c.tier, c.operational_model, inst_status])

    print(format_table(headers, rows))
    print(f"\nTotal Candidates: {len(candidates)} (Catalog contains {len(catalog.candidates)} total: 12 Approved Group A, 1 Deferred Group B)\n")
    return EXIT_SUCCESS

def cmd_inspect(args, installer: Installer) -> int:
    catalog = installer.catalog
    cand = catalog.find(args.identifier)
    if not cand:
        print(f"Error: Candidate '{args.identifier}' not found in catalog.", file=sys.stderr)
        return EXIT_ERROR

    prov = cand.provenance
    if getattr(args, "json", False):
        data = {
            "id": cand.id,
            "name": cand.name,
            "display_name": cand.display_name,
            "category": cand.category,
            "tier": cand.tier,
            "operational_model": cand.operational_model,
            "license_clearance": cand.license_clearance,
            "provenance": {
                "author": prov.author,
                "repository_url": prov.repository_url,
                "commit_sha": prov.commit_sha,
                "declared_license": prov.declared_license,
                "source_file_path": prov.source_file_path
            },
            "description": cand.description,
            "security_guidelines": cand.security_guidelines,
            "adaptation_requirements": cand.adaptation_requirements,
            "supporting_files": cand.supporting_files
        }
        print(json.dumps(data, indent=2))
        return EXIT_SUCCESS

    print(f"\n=== Candidate Inspection: {cand.name} ({cand.id}) ===\n")
    print(f"Display Name:         {cand.display_name}")
    print(f"Category:             {cand.category}")
    print(f"Tier:                 {cand.tier}")
    print(f"Operational Model:    {cand.operational_model}")
    print(f"Legal Clearance:      {cand.license_clearance}")
    print(f"Author / Maintainer:  {prov.author}")
    print(f"Upstream Repository:  {prov.repository_url}")
    print(f"Locked Commit SHA:    {prov.commit_sha}")
    print(f"Declared License:     {prov.declared_license}")
    print(f"\nDescription:\n  {cand.description}")
    print(f"\nSecurity Guidelines (D5):\n  {cand.security_guidelines}")
    if cand.adaptation_requirements:
        print(f"\nAdaptation Requirements (D4/D7):\n  {cand.adaptation_requirements}")
    if cand.supporting_files:
        print(f"\nSupporting Files:\n  " + ", ".join(cand.supporting_files))
    print()
    return EXIT_SUCCESS

def cmd_search(args, installer: Installer) -> int:
    catalog = installer.catalog
    results = catalog.search(
        query=args.query,
        category=getattr(args, "category", None),
        tier=getattr(args, "tier", None)
    )
    installed = {s.name: s.scope for s in installer.list_installed()}

    if getattr(args, "json", False):
        data = [{
            "id": c.id,
            "name": c.name,
            "display_name": c.display_name,
            "category": c.category,
            "tier": c.tier,
            "operational_model": c.operational_model,
            "installed_scope": installed.get(c.name, None)
        } for c in results]
        print(json.dumps(data, indent=2))
        return EXIT_SUCCESS

    print(f"\n=== Skills08 Search Results for '{args.query}' ===\n")
    if not results:
        print(f"No skills found matching '{args.query}'.\n")
        return EXIT_SUCCESS

    headers = ["Candidate ID", "Skill Name", "Category", "Tier", "Installed"]
    rows = []
    for c in results:
        inst_status = installed.get(c.name, "No")
        rows.append([c.id, c.name, c.category, c.tier, inst_status])

    print(format_table(headers, rows))
    print(f"\nFound {len(results)} matching candidate(s).\n")
    return EXIT_SUCCESS

def cmd_install(args, installer: Installer) -> int:
    success, msg = installer.install(args.identifier, scope=args.scope, force=args.force)
    if success:
        print(f"\n[OK] {msg}")
        if args.scope == "project" and getattr(args, "sync", False):
            agents_arg = getattr(args, "agents", None)
            agent_list = [a.strip() for a in agents_arg.split(",")] if agents_arg else None
            _, sync_msg, _ = AgentConfigManager.sync_all_agents(installer.workspace_root, agents=agent_list)
            print(f"[SYNC] {sync_msg}")
        print()
        return EXIT_SUCCESS
    else:
        print(f"\n[FAILED] {msg}\n", file=sys.stderr)
        return EXIT_ERROR

def cmd_uninstall(args, installer: Installer) -> int:
    success, msg = installer.uninstall(args.name, scope=args.scope)
    if success:
        print(f"\n[OK] {msg}")
        if args.scope == "project" and getattr(args, "sync", False):
            agents_arg = getattr(args, "agents", None)
            agent_list = [a.strip() for a in agents_arg.split(",")] if agents_arg else None
            _, sync_msg, _ = AgentConfigManager.sync_all_agents(installer.workspace_root, agents=agent_list)
            print(f"[SYNC] {sync_msg}")
        print()
        return EXIT_SUCCESS
    else:
        print(f"\n[FAILED] {msg}\n", file=sys.stderr)
        return EXIT_ERROR

def cmd_update(args, installer: Installer) -> int:
    identifier = getattr(args, "identifier", None)
    scope = getattr(args, "scope", "project")
    success, msg, count = installer.update(identifier=identifier, scope=scope)
    if success:
        print(f"\n[OK] {msg}\n")
        return EXIT_SUCCESS
    else:
        print(f"\n[FAILED] {msg}\n", file=sys.stderr)
        return EXIT_ERROR

def cmd_status(args, installer: Installer) -> int:
    req_scope = getattr(args, "scope", None)
    installed = installer.list_installed(scope=req_scope)

    if getattr(args, "json", False):
        data = {
            "workspace_root": str(installer.workspace_root),
            "project_skills_root": str(installer.project_skills_root),
            "global_skills_root": str(installer.global_skills_root),
            "scope_filter": req_scope,
            "installed_count": len(installed),
            "skills": [{
                "name": s.name,
                "scope": s.scope,
                "manifest_id": s.manifest_id,
                "files_count": s.files_count,
                "is_shadowed": s.is_shadowed,
                "path": s.path
            } for s in installed]
        }
        print(json.dumps(data, indent=2))
        return EXIT_SUCCESS

    print("\n=== Skills08 Workspace & Global Status ===\n")
    print(f"Workspace Root:       {installer.workspace_root}")
    print(f"Project Scope Path:   {installer.project_skills_root}")
    print(f"Global Scope Path:    {installer.global_skills_root}")
    if req_scope:
        print(f"Scope Filter:         {req_scope}")
    print()

    if not installed:
        print("No Skills08 skills currently installed in requested scope(s).\n")
        return EXIT_SUCCESS

    headers = ["Skill Name", "Scope", "Files", "Shadowed", "Path"]
    rows = []
    for s in installed:
        shad = "YES (Shadowed)" if s.is_shadowed else "No"
        rows.append([s.name, s.scope, s.files_count, shad, s.path])

    print(format_table(headers, rows))
    print(f"\nTotal Active Skills: {len(installed)}\n")
    return EXIT_SUCCESS

def cmd_conflicts(args, installer: Installer) -> int:
    detector = ConflictDetector(installer.workspace_root)
    req_scope = getattr(args, "scope", None)

    proj_skills = installer.list_installed("project") if req_scope in [None, "project"] else []
    glob_skills = installer.list_installed("global") if req_scope in [None, "global"] else []

    issues = detector.scan_environment(proj_skills, glob_skills)

    if getattr(args, "json", False):
        data = {
            "scope_filter": req_scope,
            "issues_count": len(issues),
            "issues": [{
                "conflict_id": i.conflict_id,
                "name": i.name,
                "severity": i.severity,
                "category": i.category,
                "description": i.description,
                "affected_skills": i.affected_skills,
                "mitigation": i.mitigation
            } for i in issues]
        }
        print(json.dumps(data, indent=2))
        return EXIT_SUCCESS if not issues else EXIT_CONFLICT

    print("\n=== Skills08 Conflict & Shadowing Analysis ===\n")

    if not issues:
        print("[PASS] No active conflicts, shadowing, or collisions detected in the current environment.\n")
        return EXIT_SUCCESS

    print(f"Detected {len(issues)} ecosystem interaction issue(s):\n")
    for i, issue in enumerate(issues, 1):
        print(f"[{i}] {issue.conflict_id}: {issue.name} (Severity: {issue.severity})")
        print(f"    Category: {issue.category}")
        print(f"    Details:  {issue.description}")
        print(f"    Mitigation: {issue.mitigation}\n")

    return EXIT_CONFLICT

def cmd_verify(args, installer: Installer) -> int:
    verifier = IntegrityVerifier(installer)
    target_name = getattr(args, "name", None)

    if target_name:
        scope = args.scope or "project"
        results = {f"{target_name} [{scope}]": verifier.verify_skill(target_name, scope=scope)}
    else:
        results = verifier.verify_all(scope=args.scope)

    if getattr(args, "json", False):
        data = {}
        for skill_scope, items in results.items():
            data[skill_scope] = [{
                "relative_path": it.relative_path,
                "expected_hash": it.expected_hash,
                "actual_hash": it.actual_hash,
                "status": it.status,
                "details": it.details
            } for it in items]
        print(json.dumps(data, indent=2))
        all_ok = all(it.status == "MATCH" for items in results.values() for it in items) if results else True
        return EXIT_SUCCESS if all_ok else EXIT_VERIFICATION_FAILED

    print("\n=== Skills08 Cryptographic Integrity Verification ===\n")
    if not results or not any(results.values()):
        print("No installed skills found to verify.\n")
        return EXIT_SUCCESS

    all_matched = True
    total_files = 0
    matched_files = 0

    for skill_scope, items in results.items():
        print(f"-> Verifying {skill_scope}:")
        for it in items:
            total_files += 1
            if it.status == "MATCH":
                matched_files += 1
                if getattr(args, "verbose", False) or len(items) <= 5:
                    print(f"   [PASS] {it.relative_path} (SHA-256 match)")
            elif it.status == "MODIFIED":
                all_matched = False
                print(f"   [MODIFIED] {it.relative_path} (Hash mismatch: {it.actual_hash[:12]} vs {it.expected_hash[:12]})")
            elif it.status == "MISSING":
                all_matched = False
                print(f"   [MISSING] {it.relative_path} ({it.details})")
            elif it.status == "EXTRA":
                all_matched = False
                print(f"   [EXTRA] {it.relative_path} ({it.details})")
            elif it.status in ["UNKNOWN"]:
                all_matched = False
                print(f"   [ERROR] {it.details}")
        print()

    print(f"Verification Summary: {matched_files}/{total_files} files verified identical.")
    if all_matched:
        print("[PASS] All inspected skill packages passed cryptographic integrity checks.\n")
        return EXIT_SUCCESS
    else:
        print("[FAILED] Integrity drift or missing assets detected.\n", file=sys.stderr)
        return EXIT_VERIFICATION_FAILED

def cmd_new(args, installer: Installer) -> int:
    dest_dir = getattr(args, "target_dir", None)
    if dest_dir:
        dest_path = Path(dest_dir).resolve()
    else:
        dest_path = installer.project_skills_root

    success, msg, created_path = SkillScaffolder.scaffold(
        name=args.name,
        destination_dir=dest_path,
        description=getattr(args, "description", None),
        author=getattr(args, "author", None),
        category=getattr(args, "category", None),
        with_subdirs=not getattr(args, "no_subdirs", False)
    )

    if success:
        print(f"\n[OK] {msg}")
        print(f"Primary definition: {created_path / 'SKILL.md'}")
        print("You can now customize your skill instructions and examples.\n")
        return EXIT_SUCCESS
    else:
        print(f"\n[FAILED] {msg}\n", file=sys.stderr)
        return EXIT_ERROR

def cmd_pack(args, installer: Installer) -> int:
    skill_dir = Path(args.directory).resolve()
    out_dir = Path(args.output).resolve() if getattr(args, "output", None) else None

    success, msg, metadata = SkillPackager.pack(
        skill_dir=skill_dir,
        output_dir=out_dir,
        archive_name=getattr(args, "name", None)
    )

    if getattr(args, "json", False):
        print(json.dumps({"success": success, "message": msg, "metadata": metadata}, indent=2))
        return EXIT_SUCCESS if success else EXIT_ERROR

    if success:
        print(f"\n[OK] {msg}")
        print(f"Archive SHA-256: {metadata.get('archive_sha256')}")
        print(f"Archive Size:    {metadata.get('archive_size_bytes')} bytes")
        print(f"Files Packaged:  {metadata.get('files_count')}\n")
        return EXIT_SUCCESS
    else:
        print(f"\n[FAILED] {msg}\n", file=sys.stderr)
        return EXIT_ERROR

def cmd_doctor(args, installer: Installer) -> int:
    doctor = EnvironmentDoctor(
        workspace_root=installer.workspace_root,
        global_root=installer.global_skills_root
    )
    checks = doctor.run_all_checks()

    if getattr(args, "json", False):
        print(json.dumps([c.to_dict() for c in checks], indent=2))
        has_fail = any(c.status == "FAIL" for c in checks)
        return EXIT_ERROR if has_fail else EXIT_SUCCESS

    print(f"\n=== Skills08 Environment & System Doctor (v{VERSION}) ===\n")
    headers = ["Category", "Check Name", "Status", "Details"]
    rows = []
    has_fail = False

    for c in checks:
        if c.status == "FAIL":
            has_fail = True
        rows.append([c.category, c.name, f"[{c.status}]", c.details])

    print(format_table(headers, rows))
    print()

    recommendations = [c for c in checks if c.recommendation]
    if recommendations:
        print("Diagnostic Recommendations:")
        for r in recommendations:
            print(f"- [{r.name}]: {r.recommendation}")
        print()

    if not has_fail:
        print("[PASS] System and environment are ready for AI agent skill execution.\n")
        return EXIT_SUCCESS
    else:
        print("[FAIL] One or more diagnostic checks failed. Please address recommendations.\n", file=sys.stderr)
        return EXIT_ERROR

def cmd_agent_init(args, installer: Installer) -> int:
    target_ws = Path(args.target).resolve() if getattr(args, "target", None) else installer.workspace_root
    agents_arg = getattr(args, "agents", None)
    agent_list = [a.strip() for a in agents_arg.split(",")] if agents_arg else None

    success, msg, data = AgentConfigManager.init_workspace(target_ws, agents=agent_list)

    if success:
        AgentConfigManager.sync_all_agents(target_ws, agents=agent_list)

    if getattr(args, "json", False):
        print(json.dumps({"success": success, "message": msg, "data": data}, indent=2))
        return EXIT_SUCCESS if success else EXIT_ERROR

    if success:
        print(f"\n=== Skills08 Universal Agent Initialization ===\n")
        print(f"[OK] {msg}")
        print(f"Target Workspace: {data.get('workspace_root')}")
        print("Initialized Support for Coding Agents:")
        for ag in data.get("agents_initialized", []):
            print(f"  - {ag}")
        print("\nYour workspace is now equipped for every AI coding agent.\n")
        return EXIT_SUCCESS
    else:
        print(f"\n[FAILED] {msg}\n", file=sys.stderr)
        return EXIT_ERROR

def cmd_sync(args, installer: Installer) -> int:
    target_ws = installer.workspace_root
    agents_arg = getattr(args, "agents", None)
    agent_list = [a.strip() for a in agents_arg.split(",")] if agents_arg else None

    success, msg, data = AgentConfigManager.sync_all_agents(target_ws, agents=agent_list)

    if getattr(args, "json", False):
        print(json.dumps({"success": success, "message": msg, "data": data}, indent=2))
        return EXIT_SUCCESS if success else EXIT_ERROR

    if success:
        print(f"\n=== Skills08 Multi-Agent Sync ===\n")
        print(f"[OK] {msg}")
        print(f"Workspace: {data.get('workspace_root')}")
        print(f"Active Skills: {data.get('installed_skills_count')}\n")
        print("Agent Projections Updated:")
        for ag, cnt in data.get("synced_counts", {}).items():
            print(f"  - {ag:<15}: {cnt} skill(s) synced")
        print("\nAll coding agents (Antigravity, Cursor, Claude Code, Copilot, Windsurf, Cline, Gemini) are now in sync!\n")
        return EXIT_SUCCESS
    else:
        print(f"\n[FAILED] {msg}\n", file=sys.stderr)
        return EXIT_ERROR

def build_parser() -> argparse.ArgumentParser:
    common_parent = argparse.ArgumentParser(add_help=False)
    common_parent.add_argument("--workspace-root", "-w", type=Path, default=argparse.SUPPRESS, help="Project workspace root directory")
    common_parent.add_argument("--global-root", "-g", type=Path, default=argparse.SUPPRESS, help="Global skills root directory")

    parser = argparse.ArgumentParser(
        prog="skills08",
        description="Skills08: Local-First AI Agent Skill Distribution & Lifecycle Manager"
    )
    parser.add_argument("--workspace-root", "-w", type=Path, default=None, help="Project workspace root directory")
    parser.add_argument("--global-root", "-g", type=Path, default=None, help="Global skills root directory")
    parser.add_argument("--version", "-v", action="version", version=f"skills08 {VERSION}")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # list
    p_list = subparsers.add_parser("list", parents=[common_parent], help="List all candidate skills in catalog")
    p_list.add_argument("--category", "-c", help="Filter candidates by category substring")
    p_list.add_argument("--tier", "-t", help="Filter candidates by tier (e.g. 'Group A')")
    p_list.add_argument("--json", action="store_true", help="Output results in JSON format")

    # inspect / info
    p_inspect = subparsers.add_parser("inspect", parents=[common_parent], help="Inspect candidate metadata and guidelines")
    p_inspect.add_argument("identifier", help="Candidate ID (e.g. SKILL08-SEC-001) or skill name")
    p_inspect.add_argument("--json", action="store_true", help="Output in JSON format")

    p_info = subparsers.add_parser("info", parents=[common_parent], help="Alias for inspect")
    p_info.add_argument("identifier", help="Candidate ID or skill name")
    p_info.add_argument("--json", action="store_true", help="Output in JSON format")

    # search
    p_search = subparsers.add_parser("search", parents=[common_parent], help="Search skills by keyword or metadata")
    p_search.add_argument("query", help="Keyword or search term")
    p_search.add_argument("--category", "-c", help="Filter by category")
    p_search.add_argument("--tier", "-t", help="Filter by tier")
    p_search.add_argument("--json", action="store_true", help="Output in JSON format")

    # install
    p_install = subparsers.add_parser("install", parents=[common_parent], help="Install a skill package")
    p_install.add_argument("identifier", help="Candidate ID or skill name")
    p_install.add_argument("--scope", choices=["project", "global"], default="project", help="Target installation scope")
    p_install.add_argument("--force", "-f", action="store_true", help="Force overwrite existing installation")
    p_install.add_argument("--sync", "-s", action="store_true", help="Automatically sync installed skill to all coding agents")
    p_install.add_argument("--agents", "-a", help="Comma-separated agents to sync (e.g. cursor,claude,copilot)")

    # uninstall
    p_uninstall = subparsers.add_parser("uninstall", parents=[common_parent], help="Uninstall a skill package")
    p_uninstall.add_argument("name", help="Installed skill name")
    p_uninstall.add_argument("--scope", choices=["project", "global"], default="project", help="Target scope")
    p_uninstall.add_argument("--sync", "-s", action="store_true", help="Automatically sync change to all coding agents")
    p_uninstall.add_argument("--agents", "-a", help="Comma-separated agents to sync")

    # update
    p_update = subparsers.add_parser("update", parents=[common_parent], help="Update installed skill(s) from catalog")
    p_update.add_argument("identifier", nargs="?", default=None, help="Optional skill name to update (updates all if omitted)")
    p_update.add_argument("--scope", choices=["project", "global"], default="project", help="Target scope")

    # status
    p_status = subparsers.add_parser("status", parents=[common_parent], help="Show installed skills and scope status")
    p_status.add_argument("--scope", choices=["project", "global"], default=None, help="Filter status by scope")
    p_status.add_argument("--json", action="store_true", help="Output in JSON format")

    # conflicts
    p_conflicts = subparsers.add_parser("conflicts", parents=[common_parent], help="Check installed skills for conflicts and shadowing")
    p_conflicts.add_argument("--scope", choices=["project", "global"], default=None, help="Filter conflict scan by scope")
    p_conflicts.add_argument("--json", action="store_true", help="Output in JSON format")

    # verify
    p_verify = subparsers.add_parser("verify", parents=[common_parent], help="Verify cryptographic integrity of installed skills")
    p_verify.add_argument("name", nargs="?", default=None, help="Optional specific skill name to verify")
    p_verify.add_argument("--scope", choices=["project", "global"], default=None, help="Scope to verify")
    p_verify.add_argument("--verbose", "-V", action="store_true", help="Show all verified file paths")
    p_verify.add_argument("--json", action="store_true", help="Output in JSON format")

    # sync
    p_sync = subparsers.add_parser("sync", parents=[common_parent], help="Synchronize active skills across all coding agents")
    p_sync.add_argument("--agents", "-a", help="Comma-separated target agents (default: all)")
    p_sync.add_argument("--json", action="store_true", help="Output in JSON format")

    # new / init-skill
    p_new = subparsers.add_parser("new", parents=[common_parent], help="Scaffold a new custom agent skill")
    p_new.add_argument("name", help="Skill name in lowercase kebab-case (e.g. data-analyzer)")
    p_new.add_argument("--description", "-d", help="Brief skill description")
    p_new.add_argument("--category", "-c", help="Category name")
    p_new.add_argument("--author", "-a", help="Author name")
    p_new.add_argument("--target-dir", "-t", help="Target directory (defaults to .agents/skills)")
    p_new.add_argument("--no-subdirs", action="store_true", help="Do not create examples/ and references/ subdirectories")

    # pack
    p_pack = subparsers.add_parser("pack", parents=[common_parent], help="Package a skill directory into a distributable archive")
    p_pack.add_argument("directory", help="Path to skill directory containing SKILL.md")
    p_pack.add_argument("--output", "-o", help="Output directory for archive")
    p_pack.add_argument("--name", "-n", help="Custom archive filename")
    p_pack.add_argument("--json", action="store_true", help="Output package metadata in JSON format")

    # doctor
    p_doctor = subparsers.add_parser("doctor", parents=[common_parent], help="Diagnose environment, discovery paths, and catalog integrity")
    p_doctor.add_argument("--json", action="store_true", help="Output diagnostic report in JSON format")

    # agent-init
    p_agent_init = subparsers.add_parser("agent-init", parents=[common_parent], help="Initialize workspace with multi-agent discovery layout")
    p_agent_init.add_argument("--target", "-t", help="Target workspace directory (defaults to workspace root)")
    p_agent_init.add_argument("--agents", "-a", help="Comma-separated agents to initialize (default: all)")
    p_agent_init.add_argument("--json", action="store_true", help="Output in JSON format")

    return parser

def main(args=None) -> int:
    parser = build_parser()
    parsed = parser.parse_args(args)

    if not parsed.command:
        parser.print_help()
        return EXIT_SUCCESS

    ws_root = getattr(parsed, "workspace_root", None)
    gl_root = getattr(parsed, "global_root", None)

    installer = Installer(workspace_root=ws_root, global_root=gl_root)

    if parsed.command == "list":
        return cmd_list(parsed, installer)
    elif parsed.command in ["inspect", "info"]:
        return cmd_inspect(parsed, installer)
    elif parsed.command == "search":
        return cmd_search(parsed, installer)
    elif parsed.command == "install":
        return cmd_install(parsed, installer)
    elif parsed.command == "uninstall":
        return cmd_uninstall(parsed, installer)
    elif parsed.command == "update":
        return cmd_update(parsed, installer)
    elif parsed.command == "status":
        return cmd_status(parsed, installer)
    elif parsed.command == "conflicts":
        return cmd_conflicts(parsed, installer)
    elif parsed.command == "verify":
        return cmd_verify(parsed, installer)
    elif parsed.command == "sync":
        return cmd_sync(parsed, installer)
    elif parsed.command == "new":
        return cmd_new(parsed, installer)
    elif parsed.command == "pack":
        return cmd_pack(parsed, installer)
    elif parsed.command == "doctor":
        return cmd_doctor(parsed, installer)
    elif parsed.command == "agent-init":
        return cmd_agent_init(parsed, installer)
    else:
        parser.print_help()
        return EXIT_ERROR

if __name__ == "__main__":
    sys.exit(main())
