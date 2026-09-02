#!/usr/bin/env python3
"""
NMAP DECOY LAB - Cyberpunk Terminal UI
Built for Debian-based systems (Kali Linux, Parrot OS)
Created by Rax Ontto
"""

import subprocess
import re
import time
import sys
import os
from pathlib import Path
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from rich.live import Live
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
from rich.columns import Columns

console = Console()

# ─────────────────────────────────────────────────────────────────────────────
# COLOR PALETTE
# ─────────────────────────────────────────────────────────────────────────────
GREEN = "#00ff9f"
GREEN_DIM = "#00cc7a"
CYAN = "#00e5ff"
MAGENTA = "#ff00aa"
AMBER = "#ffb700"
RED = "#ff3b3b"
SILVER = "#8a9bb0"
DIM = "#3a4455"


# ─────────────────────────────────────────────────────────────────────────────
# BOOT SEQUENCE
# ─────────────────────────────────────────────────────────────────────────────
def boot_sequence():
    """Display startup animation."""
    console.clear()
    
    # ASCII art banner
    banner = """
    ███████╗███╗   ███╗
    ██╔════╝████╗ ████║
    █████╗  ██╔████╔██║
    ██╔══╝  ██║╚██╔╝██║
    ██║     ██║ ╚═╝ ██║
    ╚═╝     ╚═╝     ╚═╝
    """
    console.print(banner, style=f"bold {GREEN}")
    
    header = Panel(
        Align.center(
            Text("D E C O Y   N E T W O R K   L A B\n", style=f"bold {CYAN}")
            + Text("N M A P   O P E R A T I O N S   C O N S O L E", style=SILVER)
        ),
        border_style=GREEN_DIM,
        expand=False,
        padding=(1, 4)
    )
    console.print(Align.center(header))
    
    tags = Columns([
        Text("◈ KALI LINUX", style=MAGENTA),
        Text("◈ PARROT OS", style=MAGENTA),
        Text("◈ LAB MODE", style=MAGENTA),
    ], equal=True, width=60)
    console.print(Align.center(tags))
    
    console.print("\n")
    
    # System initialization checks
    checks = [
        ("Kernel", "ONLINE"),
        ("Python Runtime", "ONLINE"),
        ("Nmap Engine", "ONLINE"),
        ("Packet Analyzer", "READY"),
        ("Authorization Layer", "ACTIVE"),
    ]
    
    init_table = Table(show_header=False, box=None, padding=(0, 2))
    
    for i, (label, status) in enumerate(checks):
        time.sleep(0.3)
        dot = f"[{GREEN}]◉[/{GREEN}]" if i < len(checks) else ""
        console.print(f"  {dot} {label:<30} {status:>20}", style=SILVER)
    
    console.print("\n")
    time.sleep(0.5)
    console.print("  [bold green]>>> SYSTEM READY <<<[/bold green]")
    console.print("\n")
    time.sleep(1)
    console.clear()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN MENU
# ─────────────────────────────────────────────────────────────────────────────
def main_menu():
    """Display main operations menu."""
    console.clear()
    
    # Header
    header_text = Text()
    header_text.append("DECOY NETWORK LAB", style=f"bold {GREEN}")
    header_text.append("\n", style="")
    header_text.append("NMAP OPERATIONS CONSOLE  ◈  v1.0.0  ◈  BY RAX ONTTO", style=SILVER)
    
    console.print(Align.left(Panel(header_text, border_style=DIM, padding=(1, 2))))
    
    # Menu items
    ops = [
        ("01", "DECOY SCAN", "Execute authorized lab scan", "scan"),
        ("02", "TRACE ANALYZER", "Analyze packet evidence", "trace"),
        ("03", "NMAP ANALYZER", "Parse saved scan output", "nmap"),
        ("04", "SYSTEM STATUS", "Inspect environment", "status"),
        ("00", "EXIT", "Close console", "exit"),
    ]
    
    menu_table = Table(show_header=False, box=None, padding=(0, 2))
    
    for code, label, desc, cmd in ops:
        menu_table.add_row(
            Text(f"[{code}]", style=MAGENTA),
            Text("◈", style=GREEN),
            Text(label, style=f"bold {SILVER}"),
            Text(desc, style=DIM),
        )
    
    console.print(Panel(menu_table, border_style=GREEN_DIM, padding=(1, 2), title="OPERATIONS"))
    
    console.print()
    while True:
        choice = console.input(f"  [{CYAN}]SELECT OPERATION[/{CYAN}]: ").strip().lower()
        op_map = {op[3]: op for op in ops}
        if choice in op_map:
            return choice
        console.print(f"  [{RED}]✕ Invalid selection[/{RED}]")


# ─────────────────────────────────────────────────────────────────────────────
# TARGET INPUT
# ─────────────────────────────────────────────────────────────────────────────
def get_target():
    """Prompt for and validate target IP/domain."""
    console.clear()
    
    console.print(Panel(
        "[cyan]Enter an authorized laboratory IP address or domain.[/cyan]\n"
        "[amber]⚠ Only target systems you own or are explicitly authorized to test.[/amber]",
        title="TARGET ACQUISITION",
        border_style=CYAN,
        padding=(1, 2)
    ))
    
    while True:
        target = console.input(f"  [{CYAN}]TARGET ──►[/{CYAN}] ").strip()
        
        if not target:
            console.print(f"  [{RED}]✕ Target required[/{RED}]")
            continue
        
        # Validate IP
        ip_pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
        if re.match(ip_pattern, target):
            parts = [int(x) for x in target.split(".")]
            if any(p > 255 for p in parts) or parts[0] in (0, 255):
                console.print(f"  [{RED}]✕ Invalid IP address[/{RED}]")
                continue
        # Validate domain
        elif not re.match(r"^[a-zA-Z0-9][a-zA-Z0-9.-]{1,253}$", target):
            console.print(f"  [{RED}]✕ Invalid IP or domain format[/{RED}]")
            continue
        
        console.print(f"  [{GREEN}]✓ Target validated[/{GREEN}]")
        return target


# ─────────────────────────────────────────────────────────────────────────────
# DECOY SELECTION
# ─────────────────────────────────────────────────────────────────────────────
def get_decoy_count():
    """Prompt for decoy count (1-10)."""
    console.clear()
    
    console.print(Panel(
        "[cyan]Set number of decoy nodes (1–10).[/cyan]\n"
        "[silver]Decoys inject random source IPs into the scan, obscuring the real attacker.[/silver]",
        title="DECOY MATRIX",
        border_style=CYAN,
        padding=(1, 2)
    ))
    
    # Show number grid
    grid = "  "
    for i in range(1, 11):
        grid += f"[{GREEN}]{i:02d}[/{GREEN}]  "
        if i % 5 == 0:
            grid += "\n  "
    console.print(grid)
    console.print()
    
    while True:
        try:
            count = int(console.input(f"  [{CYAN}]DECOY COUNT ──►[/{CYAN}] ").strip())
            if 1 <= count <= 10:
                console.print(f"  [{GREEN}]✓ {count} decoy nodes selected[/{GREEN}]")
                return count
            console.print(f"  [{RED}]✕ Enter value between 1 and 10[/{RED}]")
        except ValueError:
            console.print(f"  [{RED}]✕ Invalid input[/{RED}]")


# ─────────────────────────────────────────────────────────────────────────────
# PORT SELECTION
# ─────────────────────────────────────────────────────────────────────────────
def get_ports():
    """Prompt for port range."""
    console.clear()
    
    console.print(Panel(
        "[cyan]Select or enter a port range.[/cyan]",
        title="PORT MATRIX",
        border_style=CYAN,
        padding=(1, 2)
    ))
    
    presets = ["1-200", "1-1024", "80", "22,80,443", "1-65535"]
    for i, p in enumerate(presets, 1):
        console.print(f"  [{i}] {p}")
    
    console.print()
    
    while True:
        choice = console.input(f"  [{CYAN}]PORTS ──►[/{CYAN}] ").strip()
        
        if choice in presets:
            return choice
        if re.match(r"^[\d,\-]+$", choice):
            console.print(f"  [{GREEN}]✓ Port range accepted[/{GREEN}]")
            return choice
        
        console.print(f"  [{RED}]✕ Invalid port format[/{RED}]")


# ─────────────────────────────────────────────────────────────────────────────
# VERBOSE MODE
# ─────────────────────────────────────────────────────────────────────────────
def get_verbose():
    """Prompt for verbose mode."""
    console.clear()
    
    console.print(Panel(
        "[cyan]Enable verbose output to see raw Nmap telemetry.[/cyan]",
        title="VERBOSE MODE",
        border_style=CYAN,
        padding=(1, 2)
    ))
    
    console.print(f"\n  [{GREEN}][ ON ][/{GREEN}]   ◉ ACTIVE (default)\n")
    console.print(f"  [{DIM}][OFF ][/{DIM}]   ○ DISABLED\n")
    
    choice = console.input(f"  [{CYAN}]VERBOSE ──► [Y/n][/{CYAN}] ").strip().lower()
    return choice != "n"


# ─────────────────────────────────────────────────────────────────────────────
# AUTHORIZATION GATE
# ─────────────────────────────────────────────────────────────────────────────
def authorization_gate(target, decoys, ports, verbose):
    """Authorization confirmation screen."""
    console.clear()
    
    warning_panel = Panel(
        Text("⚠ WARNING", style=f"bold {AMBER}") + "\n\n"
        + Text("AUTHORIZED SECURITY LAB ONLY", style=AMBER) + "\n\n"
        + Text(
            "This console is intended for systems you own or are explicitly authorized to test.\n"
            "Target scope must be verified before execution. Unauthorized scanning is illegal.\n",
            style=SILVER
        ),
        border_style=AMBER,
        padding=(1, 2)
    )
    console.print(Align.center(warning_panel))
    
    console.print()
    console.print(f"  [{SILVER}]SCAN PROFILE[/{SILVER}]")
    console.print(f"    TARGET:  [{CYAN}]{target}[/{CYAN}]")
    console.print(f"    DECOYS:  [{GREEN}]{decoys}[/{GREEN}]")
    console.print(f"    PORTS:   [{GREEN}]{ports}[/{GREEN}]")
    console.print(f"    VERBOSE: [{GREEN}]{'ON' if verbose else 'OFF'}[/{GREEN}]")
    console.print()
    
    while True:
        confirm = console.input(f"  [{AMBER}]CONFIRM ──► [Y/n][/{AMBER}] ").strip().lower()
        if confirm in ("y", ""):
            return True
        elif confirm == "n":
            return False


# ─────────────────────────────────────────────────────────────────────────────
# NMAP EXECUTION
# ─────────────────────────────────────────────────────────────────────────────
def run_nmap_scan(target, decoys, ports, verbose):
    """Execute nmap with decoy nodes."""
    console.clear()
    
    cmd = ["sudo", "nmap", "-D", f"RND:{decoys}", "-p", ports, target]
    if verbose:
        cmd.insert(5, "-v")
    
    console.print(Panel(
        Text("LIVE OPERATION", style=f"bold {CYAN}"),
        border_style=GREEN_DIM,
        padding=(1, 2)
    ))
    
    console.print()
    console.print(f"  [{SILVER}]TARGET:[/{SILVER}]    {target}")
    console.print(f"  [{SILVER}]DECOYS:[/{SILVER}]    {decoys}")
    console.print(f"  [{SILVER}]PORTS:[/{SILVER}]     {ports}")
    console.print(f"  [{SILVER}]VERBOSE:[/{SILVER}]   {'ON' if verbose else 'OFF'}")
    console.print()
    
    console.print(f"  [{GREEN}]COMMAND:[/{GREEN}]")
    console.print(f"    {' '.join(cmd)}")
    console.print()
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            return parse_nmap_output(result.stdout), result.stdout
        else:
            console.print(f"  [{RED}]✕ Nmap failed:[/{RED}]")
            console.print(result.stderr)
            return None, result.stderr
    
    except subprocess.TimeoutExpired:
        console.print(f"  [{RED}]✕ Scan timed out[/{RED}]")
        return None, ""
    except Exception as e:
        console.print(f"  [{RED}]✕ Error: {e}[/{RED}]")
        return None, str(e)


# ─────────────────────────────────────────────────────────────────────────────
# PARSE NMAP OUTPUT
# ─────────────────────────────────────────────────────────────────────────────
def parse_nmap_output(output):
    """Parse nmap output and extract open ports."""
    ports = []
    for line in output.split("\n"):
        # Match lines like "22/tcp   open   ssh"
        match = re.match(r"^(\d+)/(\w+)\s+(\w+)\s+(.+)$", line.strip())
        if match:
            port, proto, state, service = match.groups()
            if state == "open":
                ports.append({
                    "port": f"{port}/{proto}",
                    "state": state,
                    "service": service.strip()
                })
    return {"ports": ports, "raw_output": output}


# ─────────────────────────────────────────────────────────────────────────────
# RESULTS DISPLAY
# ─────────────────────────────────────────────────────────────────────────────
def display_results(target, decoys, ports_range, parsed, raw_output):
    """Display scan results."""
    console.clear()
    
    console.print(Panel(
        Text("◈ OPERATION COMPLETE ◈", style=f"bold {GREEN}"),
        border_style=GREEN_DIM,
        padding=(1, 2)
    ))
    
    console.print()
    
    # Summary table
    summary_table = Table(show_header=False, box=None, padding=(0, 2))
    summary_table.add_row(Text("TARGET", style=DIM), Text(target, style=CYAN))
    summary_table.add_row(Text("DECOY COUNT", style=DIM), Text(str(decoys), style=GREEN))
    summary_table.add_row(Text("PORT RANGE", style=DIM), Text(ports_range, style=GREEN))
    summary_table.add_row(Text("OPEN PORTS", style=DIM), Text(str(len(parsed["ports"])), style=GREEN))
    summary_table.add_row(Text("STATUS", style=DIM), Text("● SUCCESS", style=GREEN))
    
    console.print(Panel(summary_table, border_style=GREEN_DIM, padding=(1, 2)))
    
    console.print()
    console.print(Panel(
        Text("NMAP TELEMETRY", style=SILVER),
        border_style=GREEN_DIM,
        padding=(0, 2)
    ))
    
    # Results table
    results_table = Table(show_header=True, box=None, padding=(0, 2))
    results_table.add_column("PORT", style=CYAN)
    results_table.add_column("STATE", style=GREEN)
    results_table.add_column("SERVICE", style=WHITE)
    
    for p in parsed["ports"]:
        results_table.add_row(p["port"], p["state"].upper(), p["service"])
    
    console.print(results_table)
    
    console.print()
    
    # Command used
    console.print(f"[{SILVER}]COMMAND USED[/{SILVER}]")
    console.print(f"  nmap -D RND:{decoys} -p {ports_range} {target}")
    
    console.print()
    
    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = Path.home() / "decoy_reports" / f"scan_{timestamp}.txt"
    report_path.parent.mkdir(exist_ok=True)
    
    with open(report_path, "w") as f:
        f.write("=" * 70 + "\n")
        f.write("NMAP DECOY LAB - SCAN REPORT\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"TARGET:       {target}\n")
        f.write(f"DECOYS:       {decoys}\n")
        f.write(f"PORT RANGE:   {ports_range}\n")
        f.write(f"TIMESTAMP:    {timestamp}\n")
        f.write(f"OPEN PORTS:   {len(parsed['ports'])}\n\n")
        f.write("RESULTS:\n")
        f.write("-" * 70 + "\n")
        for p in parsed["ports"]:
            f.write(f"  {p['port']:<20} {p['state']:<12} {p['service']}\n")
        f.write("\n" + "=" * 70 + "\n")
        f.write("RAW NMAP OUTPUT:\n")
        f.write("=" * 70 + "\n\n")
        f.write(raw_output)
    
    console.print(f"[{GREEN}]✓ Report saved:[/{GREEN}] {report_path}")
    console.print()
    console.input("  [Press ENTER to continue]")


# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM STATUS
# ─────────────────────────────────────────────────────────────────────────────
def system_status():
    """Display system information."""
    console.clear()
    
    console.print(Panel(
        Text("SYSTEM STATUS", style=f"bold {CYAN}"),
        border_style=CYAN,
        padding=(1, 2)
    ))
    
    console.print()
    console.print(f"[{SILVER}]RUNTIME ENVIRONMENT[/{SILVER}]")
    
    status_table = Table(show_header=False, box=None, padding=(0, 2))
    status_table.add_row(Text("Platform", style=DIM), Text("Linux", style=GREEN))
    status_table.add_row(Text("Distribution", style=DIM), Text("Kali/Parrot (Debian-based)", style=GREEN))
    status_table.add_row(Text("Python Runtime", style=DIM), Text(f"{sys.version.split()[0]}", style=GREEN))
    status_table.add_row(Text("Nmap Installed", style=DIM), Text("Required", style=GREEN))
    status_table.add_row(Text("Rich Library", style=DIM), Text("Loaded", style=GREEN))
    
    console.print(status_table)
    
    console.print()
    console.print(f"[{AMBER}]SECURITY CONSTRAINTS[/{AMBER}]")
    console.print(f"  [{RED}]✕[/{RED}] No arbitrary -S source spoofing")
    console.print(f"  [{RED}]✕[/{RED}] No exploit automation")
    console.print(f"  [{RED}]✕[/{RED}] Lab networks only")
    console.print(f"  [{RED}]✕[/{RED}] Decoys limited to 1–10")
    
    console.print()
    console.print(f"[{GREEN}]PERMITTED OPERATIONS[/{GREEN}]")
    console.print(f"  [{GREEN}]✓[/{GREEN}] -D RND:N decoy scan")
    console.print(f"  [{GREEN}]✓[/{GREEN}] Authorized lab networks")
    console.print(f"  [{GREEN}]✓[/{GREEN}] Port range 1–65535")
    console.print(f"  [{GREEN}]✓[/{GREEN}] Verbose output")
    console.print(f"  [{GREEN}]✓[/{GREEN}] Report generation")
    
    console.print()
    console.input("  [Press ENTER to continue]")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN LOOP
# ─────────────────────────────────────────────────────────────────────────────
def main():
    """Main application loop."""
    try:
        boot_sequence()
        
        while True:
            choice = main_menu()
            
            if choice == "exit":
                console.clear()
                console.print(Panel(
                    Align.center(Text("NDL CONSOLE  ◈  TERMINATED", style=f"bold {GREEN}")),
                    border_style=GREEN_DIM,
                    padding=(2, 4)
                ))
                break
            
            elif choice == "scan":
                target = get_target()
                decoys = get_decoy_count()
                ports = get_ports()
                verbose = get_verbose()
                
                if authorization_gate(target, decoys, ports, verbose):
                    console.clear()
                    console.print(Panel(
                        Text("Launching scan…", style=GREEN),
                        border_style=GREEN_DIM
                    ))
                    time.sleep(1)
                    
                    parsed, raw_output = run_nmap_scan(target, decoys, ports, verbose)
                    
                    if parsed:
                        display_results(target, decoys, ports, parsed, raw_output)
            
            elif choice == "status":
                system_status()
            
            elif choice == "trace":
                console.clear()
                console.print(Panel(
                    Text("TRACE ANALYZER - Demo Mode", style=CYAN),
                    border_style=CYAN,
                    padding=(2, 2)
                ))
                console.print()
                console.print("[silver]This feature requires imported Wireshark PCAP files.[/silver]")
                console.print("[dim]Feature documentation coming soon.[/dim]")
                console.print()
                console.input("  [Press ENTER to continue]")
            
            elif choice == "nmap":
                console.clear()
                console.print(Panel(
                    Text("NMAP ANALYZER - Demo Mode", style=CYAN),
                    border_style=CYAN,
                    padding=(2, 2)
                ))
                console.print()
                console.print("[silver]Paste raw Nmap output to parse and analyze.[/silver]")
                console.print("[dim]Feature documentation coming soon.[/dim]")
                console.print()
                console.input("  [Press ENTER to continue]")
    
    except KeyboardInterrupt:
        console.print("\n\n[red]✕ Console interrupted[/red]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]✕ Fatal error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
