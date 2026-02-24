#!/usr/bin/env python3
"""
Generate requirements.txt from the current environment.

Use this after creating the conda env from environment.yml:
  conda activate cocoaboard
  python scripts/generate_requirements.py

Or run via conda without activating:
  conda run -n cocoaboard pip freeze -l > requirements.txt

This script uses pip freeze --local for a clean list from the active env.
"""
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REQUIREMENTS_FILE = REPO_ROOT / "requirements.txt"


def main():
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "freeze", "--local"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
    except FileNotFoundError:
        print("pip not found. Activate the cocoaboard conda env first.", file=sys.stderr)
        sys.exit(1)

    if result.returncode != 0:
        print(result.stderr or result.stdout, file=sys.stderr)
        sys.exit(result.returncode)

    lines = [line.strip() for line in result.stdout.strip().splitlines() if line.strip()]
    lines.sort(key=lambda s: s.lower().split("==")[0])

    REQUIREMENTS_FILE.write_text("\n".join(lines) + "\n")
    print(f"Wrote {len(lines)} packages to {REQUIREMENTS_FILE}")


if __name__ == "__main__":
    main()
