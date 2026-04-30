"""
WebScout entry point for `python -m webscout`.
 
This file is what Python executes when you run:
    python -m webscout <args>
 
It simply delegates to main() in webscout.main, which wires up the
argument parser and kicks off the scan. Keeping this file thin means
the real logic stays importable and testable inside main.py.
"""
 
import sys
 
 
def _check_dependencies():
    """Warn clearly if required packages are missing."""
    missing = []
    for pkg in ("requests", "rich"):
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
 
    if missing:
        print(
            f"[WebScout] Missing required packages: {', '.join(missing)}\n"
            f"           Run: pip install {' '.join(missing)}\n",
            file=sys.stderr,
        )
        sys.exit(1)
 
 
if __name__ == "__main__":
    _check_dependencies()
    from webscout.main import main
    main()
 
 