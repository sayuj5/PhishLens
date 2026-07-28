from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
from collections import defaultdict

def create_header(status="ONLINE", interface="eth0", stats=None):
    if stats is None:
        stats = {"total_packets": 0, "alerts_generated": 0, "dropped_packets": 0}
        
    table = Table.grid(expand=True)
    table.add_column(justify="left", ratio=1)
    table.add_column(justify="center", ratio=1)
    table.add_column(justify="right", ratio=1)
    
    status_color = "bold green" if status == "ONLINE" else "bold red"
    
    table.add_row(
        f"Status: [{status_color}]{status}[/]",
        f"[bold cyan]SentinelX NIDS[/]",
        f"Interface: [bold yellow]{interface}[/]"
    )
    table.add_row(
        f"Packets: {stats['total_packets']}",
        f"Alerts: [bold red]{stats['alerts_generated']}[/]",
        f"Dropped: {stats['dropped_packets']}"
    )
    
    return Panel(table, style="bold blue")

def create_traffic_panel(protocols: dict):
    table = Table(show_header=False, box=None, expand=True)
    table.add_column("Protocol", style="cyan", width=10)
    table.add_column("Bar", style="green")
    
    total = sum(protocols.values()) or 1
    
    for proto in sorted(protocols.keys(), key=lambda k: protocols[k], reverse=True):
        count = protocols[proto]
        bar_len = int((count / total) * 40)
        bar = "█" * bar_len
        table.add_row(proto, f"{bar} ({count})")
        
    if not protocols:
        table.add_row("Waiting for traffic...", "")
        
    return Panel(table, title="[bold]Live Traffic[/]", border_style="green")

def create_alerts_panel(recent_alerts: list):
    table = Table(show_header=True, expand=True)
    table.add_column("Time", style="dim", width=10)
    table.add_column("Severity", width=10)
    table.add_column("Rule", style="bold white")
    table.add_column("Source IP", style="cyan")
    
    for severity, rule_name, src_ip, timestamp in recent_alerts[:8]:
        sev_style = "red bold" if severity in ["HIGH", "CRITICAL"] else ("yellow bold" if severity == "MEDIUM" else "green")
        table.add_row(timestamp, f"[{sev_style}]{severity}[/]", rule_name, src_ip)
        
    if not recent_alerts:
        table.add_row("-", "-", "No recent alerts", "-")
        
    return Panel(table, title="[bold]Recent Alerts[/]", border_style="red")

def create_top_talkers_panel(top_src: dict):
    table = Table(show_header=False, box=None, expand=True)
    sorted_src = sorted(top_src.items(), key=lambda item: item[1], reverse=True)[:5]
    
    for ip, count in sorted_src:
        table.add_row(f"[cyan]{ip}[/]", str(count))
        
    if not sorted_src:
        table.add_row("No data yet")
        
    return Panel(table, title="[bold]Top Source IPs[/]", border_style="yellow")
