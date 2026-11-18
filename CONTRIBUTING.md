# Contributing to Skills08

Thank you for your interest in contributing to **Skills08**! We are building the open-source package manager and distribution standard for AI coding agents.

---

## 🛠️ Development Setup

### 1. Clone & Install in Editable Mode
```bash
git clone https://github.com/atharva081106/skills08.git
cd skills08
pip install -e .
```

### 2. Run the Verification Test Suite
Before making any changes, ensure all tests pass:
```bash
python tests/run_all_tests.py
```
Skills08 maintains a strict **100% pass rate** requirement across all supported Python versions (3.8–3.12).

---

## 📦 How to Add a New Skill Package

Skills in Skills08 follow the **Model A (Instruction-Only / Companion Guidance)** specification. They empower AI coding agents without introducing arbitrary subprocess scripts, zombie daemons, or security risks.

### 1. Scaffold the Skill Directory
```bash
skills08 new <skill-name> \
  -d "Brief, action-oriented description of what the skill does" \
  -c "Category Name (e.g. Security, Frontend, Code Quality)" \
  -a "Your Name / Organization"
```

### 2. Author the `SKILL.md` File
Every skill must contain a standard `SKILL.md` with:
- **YAML Frontmatter**:
  ```yaml
  ---
  name: your-skill-name
  description: One-sentence description explaining when and how agents should use this skill.
  ---
  ```
- **Actionable Sections**:
  - `## Overview`
  - `## When to Use This Skill`
  - `## Step-by-Step Instructions`
  - `## Guidelines & Best Practices`
  - `## Examples`

### 3. Add Attribution & License
If the skill is adapted from an open-source upstream repository:
- Ensure the upstream license permits redistribution (MIT, Apache-2.0, BSD).
- Include a `NOTICE.md` detailing the upstream repository URL, commit SHA, author, and modifications made.

### 4. Validate & Package
```bash
# Validate and test packaging
skills08 pack "./packages/<skill-name>"
```

### 5. Verify Multi-Agent Sync
```bash
# Verify the skill projects cleanly across Cursor, Claude, Antigravity, and Copilot
skills08 sync -w .
```

---

## 🧪 Test Guidelines

When contributing code or new CLI features:
- Add unit or integration tests under `tests/`.
- Ensure tests run cleanly with zero third-party dependencies (standard library only).
- Run `python tests/run_all_tests.py` and verify all tests pass.

---

## 🚀 Pull Request Checklist

- [ ] Code follows Python standard library guidelines.
- [ ] No hardcoded credentials or API keys.
- [ ] All 50 tests pass (`python tests/run_all_tests.py`).
- [ ] Documentation updated if introducing new CLI flags or commands.
