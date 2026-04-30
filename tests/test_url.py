"""
Tests for URL utility functions.
Run with: pytest tests/
"""

import pytest
from webscout.utils.url import normalize_url, is_valid_url, get_base_url


class TestNormalizeUrl:
    def test_adds_http_when_no_scheme(self):
        assert normalize_url("example.com") == "http://example.com"

    def test_preserves_https(self):
        assert normalize_url("https://example.com") == "https://example.com"

    def test_preserves_http(self):
        assert normalize_url("http://example.com") == "http://example.com"

    def test_strips_whitespace(self):
        assert normalize_url("  example.com  ") == "http://example.com"


class TestIsValidUrl:
    def test_valid_http_url(self):
        assert is_valid_url("http://example.com") is True

    def test_valid_https_url(self):
        assert is_valid_url("https://example.com/path?q=1") is True

    def test_invalid_no_scheme(self):
        assert is_valid_url("example.com") is False

    def test_invalid_empty(self):
        assert is_valid_url("") is False

    def test_invalid_ftp(self):
        assert is_valid_url("ftp://example.com") is False


class TestGetBaseUrl:
    def test_strips_path_and_query(self):
        assert get_base_url("https://example.com/path?q=1") == "https://example.com"

    def test_preserves_port(self):
        assert get_base_url("http://example.com:8080/page") == "http://example.com:8080"