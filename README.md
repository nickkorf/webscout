# 🔍 WebScout

A modular web application security scanner, built from scratch in Python.  
Designed for learning pentesting concepts while producing a genuinely useful tool.

---

## Current Phase: 1 — HTTP Probe & Response Analysis

Point WebScout at a target and it surfaces:

- HTTP status code, response time, and redirect chain  
- Server & technology disclosure (information leakage)  
- Missing and present security headers with explanations  
- Cookie security flags (`Secure`, `HttpOnly`, `SameSite`)  
- Passive technology fingerprinting (server, framework, CMS, CDN)  
- JSON report export  

---

## Installation

```bash
git clone https://github.com/nickkorf/webscout.git
cd webscout

# Install in editable mode (best for development)
pip install -e ".[dev]"

# Or just install runtime deps
pip install -r requirements.txt
```

---

## Usage

```bash
# Basic probe
python -m webscout http://target.com

# Verbose mode — shows all headers
python -m webscout http://target.com --verbose

# Save results to JSON
python -m webscout http://target.com --output results.json

# Custom timeout
python -m webscout http://target.com --timeout 10

# After pip install -e . you can also just run:
webscout http://target.com
```

### Example output

```
Target:  http://scanme.nmap.org
Status:  200  (312ms)
Server:  Apache/2.4.7

Detected Technologies:
  • Apache

⚠ Information Disclosure:
  Server: Apache/2.4.7

Security Headers:
  ✓ Present: 0
  ✗ Missing: 7

Missing Security Headers:
  ✗ Strict-Transport-Security
      Enforces HTTPS connections (HSTS)
  ✗ Content-Security-Policy
      Prevents XSS and injection attacks
  ...
```

---

## Project Structure

```
webscout/
├── webscout/
│   ├── __init__.py          # Public API & version
│   ├── __main__.py          # python -m webscout entry point
│   ├── main.py              # CLI argument parsing
│   ├── modules/
│   │   └── probe.py         # Core HTTP probe logic
│   └── utils/
│       ├── url.py           # URL helpers
│       ├── tech_detect.py   # Technology fingerprinting
│       └── output.py        # Terminal output & JSON export
├── tests/
│   ├── test_url.py
│   └── test_tech_detect.py
├── pyproject.toml           # Package config & dependencies
├── requirements.txt         # Runtime deps
└── requirements-dev.txt     # Dev/test deps
```

---

## Running Tests

```bash
# Run all tests
pytest

# With coverage report
pytest --cov=webscout --cov-report=term-missing
```

---

## Roadmap

| Phase | Status | Description |
|-------|--------|-------------|
| 1 | ✅ Done | HTTP probe, header analysis, tech detection |
| 2 | 🔜 Next | Web crawler, endpoint & form discovery |
| 3 | ⏳ Planned | SQLi, XSS, and misconfiguration checks |
| 4 | ⏳ Planned | Async engine, plugin system, HTML reports |

---

## Legal & Ethics

Only scan targets you own or have explicit written permission to test.  
Unauthorized scanning is illegal in most jurisdictions.  
Use responsibly on: your own VMs, DVWA, HackTheBox, TryHackMe, or OWASP WebGoat.

---

## License

MIT