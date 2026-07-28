# 👁️ SentinelX

> **Lightweight Terminal-Based Network Intrusion Detection System**

<p align="center">
        ▲<br>
      /███\<br>
     /█████\<br>
    |  👁  |<br>
    |██████|<br>
     \████/<br>
      \██/<br>
       ||<br>
      /||\
</p>

## Overview
SentinelX is a production-quality, multi-threaded Network Intrusion Detection System (NIDS) designed for educational purposes. Inspired by Snort and themed with a classic "HackTheBox / Kali Linux" aesthetic, it captures live network traffic, parses packets, and evaluates them against YAML-based heuristic rules using a sliding-window detection engine.

### Key Features
- **Live Packet Capture**: Uses `scapy` to sniff TCP, UDP, ICMP, DNS, ARP, HTTP, and SSH.
- **Sliding-Window Engine**: Efficiently detects floods and bursts using time-based threshold counters.
- **Terminal Dashboard**: A real-time `rich` terminal UI displaying traffic stats, top talkers, and alerts.
- **Configurable Rules**: YAML-based signature definitions loaded dynamically.
- **Structured Logging**: Outputs alerts to text files and raw packets to JSON logs.

## 📁 Project Structure

```text
SentinelX/
├── core/             # Core sniffing, parsing, engine, and logging
├── rules/            # YAML rules and Rule Engine
├── terminal/         # Rich terminal UI components
├── attacks/          # Simulated attack scripts (Lab Use Only!)
├── logs/             # Generated logs (alerts and JSON packets)
├── sentinel.py       # Main CLI entry point
└── requirements.txt  # Dependencies
```

## 🛠️ Installation & Setup

1. **Clone the Repository**
2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *(Note for Windows users: You must have Npcap installed, usually bundled with Wireshark, for `scapy` to capture packets).*

## 🚀 Usage

### 1. Start the IDS
Run SentinelX with administrator/root privileges (required for packet sniffing):
```bash
sudo python sentinel.py start --iface eth0
```
*(Replace `eth0` with your active network interface, e.g., `Wi-Fi` on Windows).*

### 2. Verify Rules
To check if the YAML rules are parsed correctly:
```bash
python sentinel.py check-rules
```

## ⚔️ Lab Testing (Attack Simulators)

> [!CAUTION]
> **UNAUTHORIZED USE IS STRICTLY PROHIBITED.**
> The scripts in the `attacks/` directory generate real network attacks (Floods). They must **ONLY** be run on local, isolated lab environments that you own or have explicit authorization to test.

Open a second terminal and run a simulator to test SentinelX's detection:

```bash
# ICMP Flood
sudo python attacks/icmp_flood.py --target 127.0.0.1 --count 200

# TCP SYN Flood
sudo python attacks/syn_flood.py --target 127.0.0.1 --port 80
```
Observe the SentinelX dashboard. You will see a `[HIGH]` severity alert pop up in the **Recent Alerts** panel and logged to `logs/alerts.log`.

## 📜 Educational Note
SentinelX was built to demonstrate Systems Programming, Network Security, and Clean Architecture in Python. Its heuristic-based engine shows the fundamentals of how professional NIDS/NIPS (like Snort or Suricata) evaluate stateful traffic patterns.
