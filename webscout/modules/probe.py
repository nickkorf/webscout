"""
probe.py - Core HTTP probing module

Sends a request to the target URL and extracts security-relevant information.
This is the foundation that all future modules will build on.
"""

import requests
import time
from urllib.parse import urlparse
from webscout.utils.url import normalize_url, is_valid_url
from webscout.utils.tech_detect import detect_technologies


# Security headers we care about - missing ones are findings
SECURITY_HEADERS = {
    "Strict-Transport-Security": "Enforces HTTPS connections (HSTS)",
    "Content-Security-Policy": "Prevents XSS and injection attacks",
    "X-Frame-Options": "Prevents clickjacking attacks",
    "X-Content-Type-Options": "Prevents MIME-type sniffing",
    "Referrer-Policy": "Controls referrer information leakage",
    "Permissions-Policy": "Controls browser feature access",
    "X-XSS-Protection": "Legacy XSS filter (older browsers)",
}

# Headers that reveal server information (info disclosure)
INFO_DISCLOSURE_HEADERS = [
    "Server",
    "X-Powered-By",
    "X-AspNet-Version",
    "X-AspNetMvc-Version",
    "X-Generator",
    "Via",
]


def probe_target(url: str, timeout: int = 5, verbose: bool = False) -> dict:
    """
    Probe a target URL and collect security-relevant information.

    Args:
        url:     Target URL to probe
        timeout: Request timeout in seconds
        verbose: Include extra detail in output

    Returns:
        A dictionary containing all findings
    """
    url = normalize_url(url)

    if not is_valid_url(url):
        return {"error": f"Invalid URL: {url}"}

    results = {
        "target": url,
        "status": None,
        "error": None,
        "response_time_ms": None,
        "redirect_chain": [],
        "final_url": None,
        "server": None,
        "technologies": [],
        "cookies": [],
        "security_headers": {
            "present": {},
            "missing": {},
        },
        "info_disclosure": {},
        "all_headers": {},
    }

    try:
        start = time.time()
        response = requests.get(
            url,
            timeout=timeout,
            allow_redirects=True,
            headers={"User-Agent": "WebScout/0.1 Security Scanner"},
        )
        elapsed = round((time.time() - start) * 1000, 2)

        results["status"] = response.status_code
        results["response_time_ms"] = elapsed
        results["final_url"] = response.url
        results["all_headers"] = dict(response.headers)

        # Capture redirect chain if any
        if response.history:
            for r in response.history:
                results["redirect_chain"].append({
                    "url": r.url,
                    "status": r.status_code,
                })

        # Server / info disclosure headers
        for header in INFO_DISCLOSURE_HEADERS:
            value = response.headers.get(header)
            if value:
                results["info_disclosure"][header] = value

        results["server"] = response.headers.get("Server", "Not disclosed")

        # Security header analysis
        for header, description in SECURITY_HEADERS.items():
            value = response.headers.get(header)
            if value:
                results["security_headers"]["present"][header] = value
            else:
                results["security_headers"]["missing"][header] = description

        # Cookie analysis
        for cookie in response.cookies:
            cookie_info = {
                "name": cookie.name,
                "secure": cookie.secure,
                "http_only": cookie.has_nonstandard_attr("HttpOnly")
                             or "httponly" in str(cookie).lower(),
                "samesite": cookie._rest.get("SameSite", "Not set"),
            }
            results["cookies"].append(cookie_info)

        # Technology detection
        results["technologies"] = detect_technologies(response)

    except requests.exceptions.ConnectionError:
        results["error"] = "Connection refused or host unreachable"
    except requests.exceptions.Timeout:
        results["error"] = f"Request timed out after {timeout}s"
    except requests.exceptions.TooManyRedirects:
        results["error"] = "Too many redirects"
    except requests.exceptions.RequestException as e:
        results["error"] = f"Request failed: {str(e)}"

    return results