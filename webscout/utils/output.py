"""
output.py - Terminal output and report generation

Handles all printing to the terminal using `rich` for clean, colored output.
Also handles saving results to JSON.
"""

import json
from datetime import datetime

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

console = Console() if RICH_AVAILABLE else None


def print_banner():
    banner = r"""
 __        __   _     ____  _________   _   _ _____ 
 \ \      / /__| |__ / ___|/ ___|  _ \ | | | |_   _|
  \ \ /\ / / _ \ '_ \\___ \| |   | | | | | | | | |  
   \ V  V /  __/ |_) |___) | |___| |_| | |_| | | |  
    \_/\_/ \___|_.__/|____/ \____|____/  \___/  |_|  

  Web Application Security Scanner  |  v0.1.0  |  Phase 1
    """
    if RICH_AVAILABLE:
        console.print(f"[bold cyan]{banner}[/bold cyan]")
    else:
        print(banner)


def print_summary(results: dict, verbose: bool = False, output_file: str = None):
    """Print a formatted summary of probe results to the terminal."""

    if results.get("error"):
        _print_error(results)
        return

    if RICH_AVAILABLE:
        _print_rich(results, verbose)
    else:
        _print_plain(results, verbose)

    if output_file:
        _save_json(results, output_file)


# ─── Rich output (pretty) ────────────────────────────────────────────────────

def _print_rich(results: dict, verbose: bool):
    c = console

    # ── Target Overview ──
    status = results["status"]
    status_color = "green" if 200 <= status < 300 else "yellow" if status < 400 else "red"

    c.print(f"\n[bold]Target:[/bold]  {results['target']}")
    c.print(f"[bold]Status:[/bold]  [{status_color}]{status}[/{status_color}]  "
            f"({results['response_time_ms']}ms)")
    c.print(f"[bold]Server:[/bold]  {results['server']}")

    if results["final_url"] != results["target"]:
        c.print(f"[bold]Redirected to:[/bold] [cyan]{results['final_url']}[/cyan]")

    if results["redirect_chain"]:
        c.print(f"[bold]Redirects:[/bold] {len(results['redirect_chain'])} hop(s)")

    # ── Technologies ──
    if results["technologies"]:
        c.print(f"\n[bold]Detected Technologies:[/bold]")
        for tech in results["technologies"]:
            c.print(f"  [cyan]•[/cyan] {tech}")

    # ── Info Disclosure ──
    if results["info_disclosure"]:
        c.print(f"\n[bold yellow]⚠ Information Disclosure:[/bold yellow]")
        for header, value in results["info_disclosure"].items():
            c.print(f"  [yellow]{header}:[/yellow] {value}")

    # ── Security Headers ──
    missing = results["security_headers"]["missing"]
    present = results["security_headers"]["present"]

    c.print(f"\n[bold]Security Headers:[/bold]")
    c.print(f"  [green]✓ Present:[/green] {len(present)}")
    c.print(f"  [red]✗ Missing:[/red]  {len(missing)}")

    if missing:
        c.print(f"\n[bold red]Missing Security Headers:[/bold red]")
        for header, desc in missing.items():
            c.print(f"  [red]✗[/red] [bold]{header}[/bold]")
            c.print(f"      [dim]{desc}[/dim]")

    if verbose and present:
        c.print(f"\n[bold green]Present Security Headers:[/bold green]")
        for header, value in present.items():
            c.print(f"  [green]✓[/green] [bold]{header}:[/bold] {value}")

    # ── Cookies ──
    if results["cookies"]:
        c.print(f"\n[bold]Cookies ({len(results['cookies'])}):[/bold]")
        for cookie in results["cookies"]:
            flags = []
            if cookie["secure"]:
                flags.append("[green]Secure[/green]")
            else:
                flags.append("[red]!Secure[/red]")
            if cookie["http_only"]:
                flags.append("[green]HttpOnly[/green]")
            else:
                flags.append("[red]!HttpOnly[/red]")
            flags_str = "  ".join(flags)
            c.print(f"  [cyan]{cookie['name']}[/cyan]  {flags_str}  SameSite={cookie['samesite']}")

    # ── All headers (verbose) ──
    if verbose and results["all_headers"]:
        c.print(f"\n[bold dim]All Response Headers:[/bold dim]")
        for k, v in results["all_headers"].items():
            c.print(f"  [dim]{k}:[/dim] {v}")

    c.print()


# ─── Plain fallback output ────────────────────────────────────────────────────

def _print_plain(results: dict, verbose: bool):
    print(f"\nTarget : {results['target']}")
    print(f"Status : {results['status']} ({results['response_time_ms']}ms)")
    print(f"Server : {results['server']}")

    if results["technologies"]:
        print(f"\nTechnologies: {', '.join(results['technologies'])}")

    if results["info_disclosure"]:
        print("\n[!] Info Disclosure:")
        for h, v in results["info_disclosure"].items():
            print(f"    {h}: {v}")

    missing = results["security_headers"]["missing"]
    print(f"\nMissing Security Headers ({len(missing)}):")
    for h in missing:
        print(f"  - {h}")


def _print_error(results: dict):
    msg = f"[ERROR] {results['error']}"
    if RICH_AVAILABLE:
        console.print(f"[bold red]{msg}[/bold red]")
    else:
        print(msg)


# ─── JSON export ─────────────────────────────────────────────────────────────

def _save_json(results: dict, filepath: str):
    output = {
        "scan_time": datetime.utcnow().isoformat() + "Z",
        "results": results,
    }
    with open(filepath, "w") as f:
        json.dump(output, f, indent=2)

    msg = f"\nResults saved to: {filepath}"
    if RICH_AVAILABLE:
        console.print(f"[dim]{msg}[/dim]")
    else:
        print(msg)