"""
WebScout - Web Application Security Scanner
============================================
 
A modular, extensible web application security scanner written in Python.
Built for learning, practicing, and real pentesting engagements.
 
Phase 1 — HTTP Probe & Response Analysis
  Probe a target URL and surface security-relevant findings:
  server disclosure, missing security headers, cookie flags,
  passive technology fingerprinting, and redirect chains.
 
Quick start:
    # From the command line:
    python -m webscout http://target.com
    python -m webscout http://target.com --verbose --output results.json
 
    # As a library:
    from webscout.modules.probe import probe_target
    results = probe_target("http://target.com")
    print(results["security_headers"]["missing"])
 
Roadmap:
    Phase 2 — Crawler & Endpoint Discovery
    Phase 3 — Vulnerability Checks (SQLi, XSS, misconfigs)
    Phase 4 — Async engine, plugin architecture, HTML reporting
"""
 
__version__ = "0.1.0"
__author__  = "Nikolas K. (github.com/nickkorf)"
__license__ = "MIT"
 
# Expose the most commonly used entry point at the top level so users can do:
#   from webscout import probe_target
from webscout.modules.probe import probe_target
 
__all__ = ["probe_target", "__version__"]