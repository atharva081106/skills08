# Security Policy

Skills08 is engineered with a **local-first, defense-in-depth** security architecture. We take the security of AI agent skills, host systems, and developer environments seriously.

---

## 🔒 Security Invariants

Skills08 enforces the following mandatory security properties:

1. **Model A Safe Execution**:
   - Skills are distributed as structured prompt instructions and companion guidance markdown.
   - Arbitrary background daemons, port listeners, and unvetted binary scripts are prohibited from execution during skill management.
2. **Zero Telemetry**:
   - Skills08 executes 100% locally on your machine.
   - Zero telemetry, analytics, or behavioral tracking is sent to external servers.
3. **Path Traversal Defenses**:
   - Strict root containment using `pathlib.Path.is_relative_to()` prevents directory traversal attacks during installation or uninstallation.
4. **Reparse Point & Junction Containment**:
   - Safe removal routines (`_safe_remove_path`) handle Windows directory junctions (`mklink /J`) and symlinks without traversing reparse targets.
5. **Atomic Staging**:
   - Installs stage into isolated randomized directories before atomic filesystem renaming, preventing partial corruption.
6. **Cryptographic Verification**:
   - Every installed file is hashed with SHA-256 and tracked in `skills08.lock.json` to detect tampering.

---

## 🚨 Reporting a Vulnerability

If you discover a potential security vulnerability in Skills08:

1. **Do NOT open a public GitHub issue.**
2. Send an email to the security maintainers at: `security@skills08.dev` (or open a private security advisory via GitHub Security Advisories).
3. Include:
   - A description of the vulnerability.
   - Step-by-step reproduction instructions or a minimal proof of concept.
   - Impact assessment on host environments or agent execution.

We will acknowledge receipt within 48 hours and work with you on a coordinated disclosure timeline.

