"""
Master test runner for Skills08 Phase 1 validation.
"""

import unittest
import sys
import time
import json
import platform
import subprocess
from pathlib import Path

# Add workspace to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
src_dir = root_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

def run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="test_*.py")

    start_time = time.time()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    elapsed = time.time() - start_time

    total = result.testsRun
    errors = len(result.errors)
    failures = len(result.failures)
    skipped = len(result.skipped)
    passed = total - errors - failures - skipped

    try:
        cmd_ver = subprocess.check_output("cmd /c ver", text=True).strip()
    except Exception:
        cmd_ver = platform.platform()

    report = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_tests": total,
        "passed": passed,
        "failures": failures,
        "errors": errors,
        "skipped": skipped,
        "elapsed_seconds": round(elapsed, 3),
        "status": "PASS" if (errors == 0 and failures == 0) else "FAIL",
        "environment": {
            "python_version": sys.version,
            "python_executable": sys.executable,
            "platform": sys.platform,
            "platform_string": platform.platform(),
            "windows_version_cmd": cmd_ver
        },
        "test_modules": [
            "test_manifest.py",
            "test_catalog_and_packages.py",
            "test_conflicts.py",
            "test_installer_lifecycle.py",
            "test_verifier_integrity.py",
            "test_security_and_secrets.py",
            "test_windows_compatibility.py",
            "test_protected_baselines.py"
        ]
    }

    report_path = root_dir / "tests" / "test_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("\n" + "=" * 70)
    print(f"SKILLS08 PHASE 1 TEST SUITE EXECUTION SUMMARY:")
    print(f"Total Tests Run: {total}")
    print(f"Passed:          {passed} ({(passed/total)*100:.1f}%)")
    print(f"Failures:        {failures}")
    print(f"Errors:          {errors}")
    print(f"Skipped:         {skipped}")
    print(f"Execution Time:  {elapsed:.3f}s")
    print(f"Overall Status:  {report['status']}")
    print("=" * 70 + "\n")

    return 0 if (errors == 0 and failures == 0) else 1

if __name__ == "__main__":
    sys.exit(run_tests())
