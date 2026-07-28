import argparse
import sys
from queue import Queue

def cmd_start(args):
    """Start SentinelX live packet capture and detection."""
    from core.sniffer import Sniffer
    from core.engine import DetectionEngine
    from rules.rule_engine import RuleEngine
    from terminal.dashboard import Dashboard

    print(f"\033[1;32m[+] Starting SentinelX on interface: {args.iface}\033[0m")

    packet_queue = Queue()
    rule_engine = RuleEngine()
    detection_engine = DetectionEngine(packet_queue, rule_engine)
    sniffer = Sniffer(args.iface, packet_queue)
    dashboard = Dashboard(detection_engine, args.iface)

    try:
        detection_engine.start()
        sniffer.start()
        dashboard.run()
    except KeyboardInterrupt:
        pass
    finally:
        print("\033[1;31m[-] Shutting down SentinelX...\033[0m")
        sniffer.stop()
        detection_engine.stop()


def cmd_check_rules(args):
    """Validate the YAML rules configuration."""
    from rules.rule_engine import RuleEngine
    engine = RuleEngine()
    if engine.rules:
        print(f"\033[1;32m[+] Rules loaded successfully: {len(engine.rules)} rules found.\033[0m")
        for rule, details in engine.rules.items():
            print(f"  - {rule}: {details}")
    else:
        print("\033[1;31m[!] No rules loaded or invalid YAML.\033[0m")


def main():
    parser = argparse.ArgumentParser(
        prog="sentinel",
        description="SentinelX - Lightweight Terminal-Based Network IDS"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- start command ---
    start_parser = subparsers.add_parser("start", help="Start live packet capture and detection")
    start_parser.add_argument(
        "--iface", "-i",
        default="eth0",
        help="Network interface to sniff on (default: eth0)"
    )

    # --- check-rules command ---
    subparsers.add_parser("check-rules", help="Validate YAML rules configuration")

    args = parser.parse_args()

    if args.command == "start":
        cmd_start(args)
    elif args.command == "check-rules":
        cmd_check_rules(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
