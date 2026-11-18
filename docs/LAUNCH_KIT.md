# 🚀 Skills08 Viral Launch Kit

A ready-to-publish social distribution kit to launch **Skills08** across Hacker News, X (Twitter), Reddit, and Product Hunt.

---

## 1. 🟠 Hacker News — Show HN Submission

### Title:
> **Show HN: Skills08 – The open-source package manager for AI coding agents**

### Post Body:
```text
Hey HN,

We built Skills08 (https://github.com/atharva081106/skills08) because we noticed a major friction point with modern AI coding agents (Cursor, Claude Code, Google Antigravity, GitHub Copilot, Windsurf):

Every agent has a slightly different way of consuming instructions (.cursorrules vs CLAUDE.md vs .github/copilot-instructions.md vs .agents/skills/). Furthermore, many third-party skills in the wild attempt to execute unvetted bash scripts, spawn zombie daemon ports, or collide silently when multiple skills compete for namespace.

Skills08 is a local-first, zero-dependency package manager and authoring framework for AI agent skills:

1. Unified Catalog: 12 production-ready cognitive skills (Security audits, Addy Osmani's code simplification heuristics, UI/UX anti-slop rules, ADR architecture generators).
2. Universal Multi-Agent Bridge: Running `skills08 install <skill> --sync` automatically projects the skill into Cursor (.cursor/rules/*.mdc), Claude Code (CLAUDE.md), GitHub Copilot (.github/copilot-instructions.md), Windsurf (.windsurfrules), Cline, and Google Antigravity.
3. Safe Non-Destructive Tagging: Single-file configs use delimited managed blocks (`<!-- BEGIN SKILLS08 MANAGED BLOCK -->`), so your existing personal developer instructions are never overwritten.
4. Model A Safety Standard: Zero arbitrary background script execution. Skills operate as verified cognitive instruction playbooks and companion guidance markdown.
5. Deterministic Cryptographic Locks: SHA-256 lockfile (`skills08.lock.json`) detects local drift or tampering.
6. Zero External Telemetry & Zero Dependencies: Built entirely on Python's standard library.

Quick install:
$ pip install git+https://github.com/atharva081106/skills08.git
$ skills08 agent-init -w ./my-app
$ skills08 install security-audit -s -w ./my-app

We'd love your feedback on the architecture, safety model, and multi-agent projection engine!
GitHub: https://github.com/atharva081106/skills08
```

---

## 2. 🐦 X (Twitter) Launch Thread

### Tweet 1 (The Hook)
> AI coding agents are getting smarter, but they still hallucinate UI boilerplate, write bloated code, and run dangerous scripts.
>
> Today, we're launching **Skills08**: The open-source package manager for AI agent skills. ⚡
>
> One command to supercharge Cursor, Claude Code, Antigravity, and Copilot. 🧵👇

### Tweet 2 (The Problem)
> Modern AI agents suffer from 3 big problems:
>
> 1️⃣ Fragmented formats (.cursorrules vs CLAUDE.md vs .agents vs copilot)  
> 2️⃣ Dangerous bash hooks & zombie daemon ports  
> 3️⃣ No supply chain verification or conflict detection  
>
> We fixed all of them.

### Tweet 3 (The Universal Bridge)
> With Skills08, install a skill once:
>
> `skills08 install security-audit --sync`
>
> It instantly projects to:
> • Cursor (`.cursor/rules/security-audit.mdc`)
> • Claude Code (`CLAUDE.md`)
> • GitHub Copilot (`.github/copilot-instructions.md`)
> • Antigravity (`.agents/skills/`)
> • Windsurf & Cline
>
> All with 100% preservation of your existing custom rules. 🪄

### Tweet 4 (The Curated Catalog)
> Comes loaded with 12 battle-tested skills:
>
> 🛡️ `security-audit` — Cloudflare-grade vulnerability checks  
> ⚡ `code-simplification` — Addy Osmani's clarity heuristics  
> 🎨 `unslop` & `hallmark` — Strip generic AI frontend tropes  
> 🧪 `browser-testing-with-devtools` — Automated browser workflows  
> 🏛️ `archify` — Structured ADR architecture generator

### Tweet 5 (Engineering Rigor)
> Built with zero external dependencies:
>
> ✅ 100% Python Standard Library  
> ✅ 50/50 automated tests passing on Windows, Linux, and macOS  
> ✅ SHA-256 cryptographic tamper detection  
> ✅ 100% Local-first, zero telemetry

### Tweet 6 (CTA)
> Try it in 30 seconds:
>
> `pip install git+https://github.com/atharva081106/skills08.git`
>
> ⭐ Star on GitHub: https://github.com/atharva081106/skills08
>
> Let us know what skills you want to see next! 🚀

---

## 3. 🔴 Reddit Submission (r/programming & r/LocalLLaMA)

### Title:
> **Skills08: An open-source package manager for AI agent skills (Cursor, Claude Code, Antigravity, Copilot)**

### Post Body:
```text
Hey everyone,

We just open-sourced Skills08 (https://github.com/atharva081106/skills08), a local-first lifecycle manager and distribution platform for AI agent skills.

### The Problem:
Every team using AI coding agents ends up maintaining ad-hoc prompt snippets or downloading unvetted third-party skill repos. These often cause:
- Agent fragmentation (Cursor rules don't work in Claude Code or Antigravity)
- Security risks (bash hooks executing unverified binaries on developer machines)
- Conflict bloat (competing persona prompts causing context degradation)

### How Skills08 Works:
Skills08 acts as a unified package manager (like `npm` or `uv` for agent skills):
- Curated catalog: 12 production skills for security, code simplification, UI anti-slop, and testing.
- Model A Standard: Pure cognitive instruction playbooks and companion guidance (zero arbitrary process execution).
- Multi-Agent Synchronization: Installs once into `.agents/skills/` and projects cleanly into Cursor (`.cursor/rules/*.mdc`), Claude Code (`CLAUDE.md`), GitHub Copilot (`.github/copilot-instructions.md`), and Windsurf.
- Safe Delimiters: Single-file configs use managed block tags so your custom developer rules are never touched.
- 100% Stdlib: Zero third-party runtime dependencies, zero telemetry. 50/50 tests passing in CI.

Check out the code, run `skills08 doctor`, and let us know what you think!
GitHub: https://github.com/atharva081106/skills08
```

---

## 4. 🐱 Product Hunt Launch Checklist

- **Name**: Skills08
- **Tagline**: The open-source package manager for AI coding agents
- **Pricing**: 100% Free & Open Source (MIT)
- **Primary Category**: Developer Tools / Artificial Intelligence
- **Key Features**:
  1. One-click skill distribution for Cursor, Claude Code, Copilot, and Antigravity
  2. Curated catalog of 12 production-tested cognitive skills
  3. Scaffolding tool to create custom team skills in seconds
  4. Cryptographic SHA-256 verification and conflict detection
  5. Zero dependencies, 100% local-first and private

