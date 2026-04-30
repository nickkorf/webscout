"""
webscout.modules
================
 
Each module in this package represents a distinct scanning capability.
Import the function you need directly, or let webscout.main orchestrate them.
 
Available modules
-----------------
probe       Core HTTP probe — the Phase 1 entry point.
            Sends one request and returns a structured findings dict.
 
Planned (Phase 2+)
------------------
crawler     Link extraction, form discovery, endpoint mapping.
dirbust     Directory and path brute-forcing with wordlists.
vulnscan    Active vulnerability checks (SQLi, XSS, misconfigs).
"""
 
from webscout.modules.probe import probe_target
 
__all__ = ["probe_target"]
 
 