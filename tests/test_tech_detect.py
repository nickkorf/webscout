"""
Tests for technology detection.
Uses mock responses to avoid real HTTP calls.
"""

import pytest
from unittest.mock import MagicMock
from webscout.utils.tech_detect import detect_technologies


def make_mock_response(headers=None, cookies="", body=""):
    """Helper to create a fake requests.Response object."""
    response = MagicMock()
    response.headers = headers or {}
    response.headers.get = lambda k, default="": (headers or {}).get(k, default)
    response.text = body
    return response


class TestTechDetect:
    def test_detects_nginx(self):
        r = make_mock_response(headers={"Server": "nginx/1.18.0"})
        assert "Nginx" in detect_technologies(r)

    def test_detects_apache(self):
        r = make_mock_response(headers={"Server": "Apache/2.4.41"})
        assert "Apache" in detect_technologies(r)

    def test_detects_php_from_header(self):
        r = make_mock_response(headers={"X-Powered-By": "PHP/8.1"})
        assert "PHP" in detect_technologies(r)

    def test_detects_cloudflare(self):
        r = make_mock_response(headers={"Server": "cloudflare", "CF-RAY": "abc123"})
        assert "Cloudflare" in detect_technologies(r)

    def test_detects_wordpress_from_body(self):
        r = make_mock_response(body='<link rel="stylesheet" href="/wp-content/themes/...">')
        assert "WordPress" in detect_technologies(r)

    def test_returns_sorted_list(self):
        r = make_mock_response(headers={"Server": "nginx", "X-Powered-By": "PHP/8.0"})
        techs = detect_technologies(r)
        assert techs == sorted(techs)

    def test_no_false_positives_on_empty(self):
        r = make_mock_response()
        assert detect_technologies(r) == []