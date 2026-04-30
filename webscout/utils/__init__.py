"""
webscout.utils
==============
 
Shared utility functions used across all WebScout modules.
 
url           URL normalisation, validation, and base-URL extraction.
tech_detect   Passive technology fingerprinting from HTTP responses.
output        Rich terminal output, plain-text fallback, and JSON export.
"""
 
from webscout.utils.url import normalize_url, is_valid_url, get_base_url
from webscout.utils.tech_detect import detect_technologies
from webscout.utils.output import print_banner, print_summary
 
__all__ = [
    "normalize_url",
    "is_valid_url",
    "get_base_url",
    "detect_technologies",
    "print_banner",
    "print_summary",
]