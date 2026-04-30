"""
tech_detect.py - Passive technology detection from HTTP responses

Infers what technologies a server is using based on response headers,
cookies, and body content. No active probing — pure analysis.
"""

import re


# Signatures: each entry is (technology_name, header_or_field, pattern)
HEADER_SIGNATURES = [
    ("PHP",          "X-Powered-By",  r"php",           re.IGNORECASE),
    ("ASP.NET",      "X-Powered-By",  r"asp\.net",      re.IGNORECASE),
    ("ASP.NET MVC",  "X-AspNetMvc-Version", r".+",      re.IGNORECASE),
    ("IIS",          "Server",        r"IIS",            re.IGNORECASE),
    ("Apache",       "Server",        r"Apache",         re.IGNORECASE),
    ("Nginx",        "Server",        r"nginx",          re.IGNORECASE),
    ("Cloudflare",   "Server",        r"cloudflare",     re.IGNORECASE),
    ("Cloudflare",   "CF-RAY",        r".+",             re.IGNORECASE),
    ("Express.js",   "X-Powered-By",  r"Express",        re.IGNORECASE),
    ("WordPress",    "X-Powered-By",  r"WP",             re.IGNORECASE),
    ("Drupal",       "X-Generator",   r"Drupal",         re.IGNORECASE),
    ("Python/Django","Server",        r"WSGIServer",     re.IGNORECASE),
    ("Gunicorn",     "Server",        r"gunicorn",       re.IGNORECASE),
]

COOKIE_SIGNATURES = [
    ("PHP",          r"PHPSESSID"),
    ("ASP.NET",      r"ASP\.NET_SessionId"),
    ("Laravel",      r"laravel_session"),
    ("Rails",        r"_session_id"),
    ("Django",       r"csrftoken|sessionid"),
    ("WordPress",    r"wordpress_|wp-settings"),
]

BODY_SIGNATURES = [
    ("WordPress",    r"wp-content|wp-includes"),
    ("Joomla",       r"/components/com_|Joomla!"),
    ("Drupal",       r"Drupal\.settings|sites/default/files"),
    ("React",        r"__REACT_|react-dom"),
    ("Vue.js",       r"__vue__"),
    ("jQuery",       r"jquery"),
    ("Bootstrap",    r"bootstrap\.min\.css|bootstrap\.min\.js"),
]


def detect_technologies(response) -> list:
    """
    Analyse an HTTP response and return a list of detected technologies.

    Args:
        response: A requests.Response object

    Returns:
        A sorted, deduplicated list of technology name strings
    """
    detected = set()

    # Check headers
    for tech, header, pattern, flags in HEADER_SIGNATURES:
        value = response.headers.get(header, "")
        if value and re.search(pattern, value, flags):
            detected.add(tech)

    # Check cookies
    cookie_header = response.headers.get("Set-Cookie", "")
    for tech, pattern in COOKIE_SIGNATURES:
        if re.search(pattern, cookie_header, re.IGNORECASE):
            detected.add(tech)

    # Check body (limit to first 50KB for performance)
    try:
        body = response.text[:50000]
        for tech, pattern in BODY_SIGNATURES:
            if re.search(pattern, body, re.IGNORECASE):
                detected.add(tech)
    except Exception:
        pass

    return sorted(detected)