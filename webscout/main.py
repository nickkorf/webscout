"""
WebScout - Web Application Security Scanner
Phase 1: HTTP Probe & Response Analysis
"""

import argparse
from webscout.modules.probe import probe_target
from webscout.utils.output import print_banner, print_summary


def parse_args():
    parser = argparse.ArgumentParser(
        prog="webscout",
        description="WebScout - Web Application Security Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m webscout http://target.com
  python -m webscout https://target.com --output results.json
  python -m webscout http://target.com --timeout 10 --verbose
        """,
    )

    parser.add_argument(
        "target",
        help="Target URL to scan (e.g. http://target.com)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=5,
        help="Request timeout in seconds (default: 5)"
    )
    parser.add_argument(
        "--output",
        help="Save results to a JSON file (e.g. results.json)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show all headers and extended info"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    print_banner()

    results = probe_target(
        url=args.target,
        timeout=args.timeout,
        verbose=args.verbose,
    )

    print_summary(results, verbose=args.verbose, output_file=args.output)


if __name__ == "__main__":
    main()