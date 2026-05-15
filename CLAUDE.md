# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install in editable mode with dev dependencies (recommended)
pip install -e ".[dev]"

# Run all tests
pytest

# Run tests with coverage
pytest --cov=webscout --cov-report=term-missing

# Run a single test file
pytest tests/test_tech_detect.py

# Run a single test by name
pytest tests/test_tech_detect.py::test_function_name

# Run the CLI
webscout <url> [--verbose] [--output results.json] [--timeout 10] [--no-color]
```

## Architecture

WebScout is a modular web application security scanner. Phase 1 (current) focuses on HTTP probing and passive analysis.

**Data flow:** CLI (`main.py`) or library caller → `probe_target(url)` → structured results dict → `print_summary()` or JSON export.

**Core result dict keys:** `target`, `status`, `error`, `response_time_ms`, `redirect_chain`, `final_url`, `server`, `technologies`, `cookies`, `security_headers`, `info_disclosure`, `all_headers`.

### Key modules

- `webscout/modules/probe.py` — `probe_target(url, timeout, verbose)` is the single entry point for scanning. Contains `SECURITY_HEADERS` (7 rules) and `INFO_DISCLOSURE_HEADERS` (6 patterns) as constants.
- `webscout/utils/tech_detect.py` — Passive fingerprinting via three signature dicts: header patterns, cookie patterns, body content patterns. Add new signatures here.
- `webscout/utils/url.py` — URL normalization (defaults scheme to `http://`) and validation.
- `webscout/utils/output.py` — Rich colored terminal output with plain-text fallback and JSON export.
- `webscout/main.py` — CLI argument parsing; add new flags here and thread them through to module functions.

### Extension patterns

- **New scan modules:** Add to `webscout/modules/` following the `probe_target()` signature (URL/options in, structured dict out).
- **New tech signatures:** Add pattern dicts to the three signature collections in `tech_detect.py`.
- **New CLI flags:** Update `parse_args()` in `main.py` and pass values to the relevant module function.

The project roadmap adds a crawler (Phase 2), vulnerability scanner (Phase 3), and async engine + plugin system (Phase 4).
