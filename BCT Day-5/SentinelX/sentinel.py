import typer
import time
from queue import Queue
from core.sniffer import Sniffer
from core.engine import DetectionEngine
from rules.rule_engine import RuleEngine
from terminal.dashboard import Dashboard

app = typer.Typer(help="SentinelX - Lightweight Terminal-Based NIDS")

@app.command()
def start(interface: str = typer.Option("eth0", "--iface", "-i", help="Network interface to sniff on (e.g., eth0, Wi-Fi)")):
    """Start SentinelX live packet capture and detection."""
    typer.secho(f"Starting SentinelX on interface {interface}...", fg=typer.colors.GREEN, bold=True)
    
    packet_queue = Queue()
    rule_engine = RuleEngine()
    detection_engine = DetectionEngine(packet_queue, rule_engine)
    sniffer = Sniffer(interface, packet_queue)
    
    dashboard = Dashboard(detection_engine, interface)
    
    try:
        detection_engine.start()
        sniffer.start()
        dashboard.run()
    except KeyboardInterrupt:
        pass
    finally:
        typer.secho("Shutting down SentinelX...", fg=typer.colors.RED)
        sniffer.stop()
        detection_engine.stop()

@app.command()
def check_rules():
    """Validate YAML rules configuration."""
    engine = RuleEngine()
    if engine.rules:
        typer.secho(f"Rules loaded successfully: {len(engine.rules)} rules found.", fg=typer.colors.GREEN)
        for rule, details in engine.rules.items():
            typer.echo(f" - {rule}: {details}")
    else:
        typer.secho("No rules loaded or invalid YAML.", fg=typer.colors.RED)

if __name__ == "__main__":
    app()
