"""
Command-line interface for Skills08 lifecycle management.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from .catalog import Catalog
from .installer import Installer
from .verifier import IntegrityVerifier
from .conflicts import ConflictDetector
from .constants import (
    EXIT_SUCCESS,
    EXIT_ERROR,
    EXIT_CONFLICT,
    EXIT_VERIFICATION_FAILED
)

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

    print("\n=== Skills08 Phase 1 Candidate Catalog ===\n")
    headers = ["Candidate ID", "Skill Name", "Category", "Tier", "Operational Model", "Installed"]
    rows = []

    for c in catalog.candidates:
        inst_status = installed.get(c.name, "No")
        rows.append([c.id, c.name, c.category, c.tier, c.operational_model, inst_status])

    print(format_table(headers, rows))
    print(f"\nTotal Candidates: {len(catalog.candidates)} (12 Approved Group A, 1 Deferred Group B)\n")
    return EXIT_SUCCESS

def cmd_inspect(args, installer: Installer) -> int:
    catalog = installer.catalog
    cand = catalog.find(args.identifier)
    if not cand:
        print(f"Error: Candidate '{args.identifier}' not found in catalog.", file=sys.stderr)
        return EXIT_ERROR

    prov = cand.provenance
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

def cmd_install(args, installer: Installer) -> int:
    success, msg = installer.install(args.identifier, scope=args.scope, force=args.force)
    if success:
        print(f"\n[OK] {msg}\n")
        return EXIT_SUCCESS
    else:
        print(f"\n[FAILED] {msg}\n", file=sys.stderr)
        return EXIT_ERROR

def cmd_uninstall(args, installer: Installer) -> int:
    success, msg = installer.uninstall(args.name, scope=args.scope)
    if success:
        print(f"\n[OK] {msg}\n")
        return EXIT_SUCCESS
    else:
        print(f"\n[FAILED] {msg}\n", file=sys.stderr)
        return EXIT_ERROR

def cmd_status(args, installer: Installer) -> int:
    installed = installer.list_installed()
    print("\n=== Skills08 Workspace & Global Status ===\n")
    print(f"Workspace Root:       {installer.workspace_root}")
    print(f"Project Scope Path:   {installer.project_skills_root}")
    print(f"Global Scope Path:    {installer.global_skills_root}\n")

    if not installed:
        print("No Skills08 skills currently installed in project or global scopes.\n")
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
    proj_skills = installer.list_installed("project")
    glob_skills = installer.list_installed("global")

    issues = detector.scan_environment(proj_skills, glob_skills)
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

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skills08",
        description="Skills08: Local-First AI Agent Skill Distribution & Lifecycle Manager"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # list
    p_list = subparsers.add_parser("list", help="List all candidate skills in catalog")

    # inspect
    p_inspect = subparsers.add_parser("inspect", help="Inspect candidate metadata and guidelines")
    p_inspect.add_argument("identifier", help="Candidate ID (e.g. SKILL08-SEC-001) or skill name")

    # install
    p_install = subparsers.add_parser("install", help="Install a skill package")
    p_install.add_argument("identifier", help="Candidate ID or skill name")
    p_install.add_argument("--scope", choices=["project", "global"], default="project", help="Target installation scope")
    p_install.add_argument("--force", "-f", action="store_true", help="Force overwrite existing installation")

    # uninstall
    p_uninstall = subparsers.add_parser("uninstall", help="Uninstall a skill package")
    p_uninstall.add_argument("name", help="Installed skill name")
    p_uninstall.add_argument("--scope", choices=["project", "global"], default="project", help="Target scope")

    # status
    p_status = subparsers.add_parser("status", help="Show installed skills and scope status")

    # conflicts
    p_conflicts = subparsers.add_parser("conflicts", help="Check installed skills for conflicts and shadowing")

    # verify
    p_verify = subparsers.add_parser("verify", help="Verify cryptographic integrity of installed skills")
    p_verify.add_argument("name", nargs="?", default=None, help="Optional specific skill name to verify")
    p_verify.add_argument("--scope", choices=["project", "global"], default=None, help="Scope to verify")

    return parser

def main(args=None) -> int:
    parser = build_parser()
    parsed = parser.parse_args(args)

    if not parsed.command:
        parser.print_help()
        return EXIT_SUCCESS

    installer = Installer()

    if parsed.command == "list":
        return cmd_list(parsed, installer)
    elif parsed.command == "inspect":
        return cmd_inspect(parsed, installer)
    elif parsed.command == "install":
        return cmd_install(parsed, installer)
    elif parsed.command == "uninstall":
        return cmd_uninstall(parsed, installer)
    elif parsed.command == "status":
        return cmd_status(parsed, installer)
    elif parsed.command == "conflicts":
        return cmd_conflicts(parsed, installer)
    elif parsed.command == "verify":
        return cmd_verify(parsed, installer)
    else:
        parser.print_help()
        return EXIT_ERROR

if __name__ == "__main__":
    sys.exit(main())
