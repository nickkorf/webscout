"""
url.py - URL normalization and validation utilities
"""

from urllib.parse import urlparse


def normalize_url(url: str) -> str:
    """
    Ensure the URL has a scheme. Defaults to http:// if missing.

    Examples:
        "example.com"        -> "http://example.com"
        "https://example.com -> "https://example.com"
    """
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url


def is_valid_url(url: str) -> bool:
    """
    Basic URL validation. Returns True if the URL has a valid scheme and netloc.
    """
    try:
        parsed = urlparse(url)
        return all([parsed.scheme in ("http", "https"), parsed.netloc])
    except Exception:
        return False


def get_base_url(url: str) -> str:
    """
    Extract just the scheme + host from a full URL.

    Example:
        "https://example.com/path?q=1" -> "https://example.com"
    """
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"