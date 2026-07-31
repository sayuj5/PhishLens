<div align="center">

# 🛡️ Cybersecurity Viva & Interview Guide

### Comprehensive Preparation Guide for Security Assessments

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Level](https://img.shields.io/badge/Level-Intermediate-blue.svg)]()
[![Focus](https://img.shields.io/badge/Focus-Cybersecurity-009688.svg)]()

**A rigorous reference manual for cybersecurity vivas, technical interviews, and academic assessments.**

</div>

---

> **📖 Overview**: This guide covers foundational security concepts, industry-standard frameworks, network defense mechanisms, and ethical hacking methodologies in detail. It is designed to bridge the gap between academic theory and practical SOC/DFIR knowledge.

---

## 📋 Table of Contents

- [1. Foundations of Security](#1-foundations-of-security)
- [2. Security Frameworks & Domains](#2-security-frameworks--domains)
- [3. Threat Intelligence & Vulnerability Management](#3-threat-intelligence--vulnerability-management)
- [4. Digital Forensics & Incident Response (DFIR)](#4-digital-forensics--incident-response-dfir)
- [5. Security Operations Center (SOC) & SIEM/EDR](#5-security-operations-center-soc--siemedr)
- [6. OSINT & Reconnaissance 🆕](#6-osint--reconnaissance)
- [7. Network Security & Intrusion Detection](#7-network-security--intrusion-detection)
- [8. Adversarial Tactics: Malware & Social Engineering](#8-adversarial-tactics-malware--social-engineering)
- [9. Web Application Security (OWASP)](#9-web-application-security-owasp)
- [10. Ethical Hacking Methodology](#10-ethical-hacking-methodology)

---

## 1. Foundations of Security

### Q: What is Cybersecurity, and how does it relate to Information Security (InfoSec)?
**A:** 
- **Information Security (InfoSec)** is the overarching discipline of protecting information—both physical and digital—from unauthorized access, disclosure, disruption, modification, or destruction. Its core objective is maintaining the **CIA Triad**:
  - **Confidentiality:** Ensuring data is accessible only to authorized entities (e.g., via Encryption).
  - **Integrity:** Ensuring data remains accurate and unaltered by unauthorized entities (e.g., via Hashing).
  - **Availability:** Ensuring systems and data are accessible when needed (e.g., via Redundancy and DDoS mitigation).
- **Cybersecurity** is a specialized sub-domain of InfoSec. It is specifically concerned with protecting internet-connected systems, networks, hardware, and digital data from cyber threats. 

> **Example:** Locking a filing cabinet is InfoSec; configuring a Next-Generation Firewall (NGFW) is Cybersecurity.

---

## 2. Security Frameworks & Domains

### Q: Explain the 8 Domains of Cybersecurity defined by the CISSP framework.
**A:** The Certified Information Systems Security Professional (CISSP) framework provides a globally recognized taxonomy for security operations:

| Domain | Focus Area | Example |
|--------|------------|---------|
| **1. Security & Risk Management** | Governance, risk assessments, compliance | ISO 27001, Policies |
| **2. Asset Security** | Data classification, privacy, media disposal | GDPR compliance |
| **3. Architecture & Engineering** | Secure design principles, cryptography | Zero Trust |
| **4. Communication & Network** | Securing network topologies, VPNs, IPsec | Firewalls, SDN |
| **5. Identity & Access (IAM)** | Authentication, authorization (RBAC) | MFA, SSO |
| **6. Assessment & Testing** | Penetration tests, vulnerability audits | Nessus scans |
| **7. Security Operations** | Day-to-day posture, IR, DR, BCP | SOC Management |
| **8. Software Development** | Secure coding practices, DevSecOps | SSDLC, SAST/DAST |

---

## 3. Threat Intelligence & Vulnerability Management

### Q: Distinguish between a Vulnerability, a Threat, and a Risk.
**A:** These terms form the foundation of risk management:
- **Vulnerability:** An inherent weakness or flaw in a system, process, or architectural design that can be exploited. *(e.g., Hardcoded API keys in a public GitHub repository).*
- **Threat:** An external or internal agent, circumstance, or event that possesses the capability to exploit a vulnerability. *(e.g., A malicious insider or an APT group).*
- **Risk:** The statistical probability of a threat exploiting a vulnerability and the resulting business impact. 

> **Formula:** `Risk = Threat × Vulnerability × Impact`

---

## 4. Digital Forensics & Incident Response (DFIR)

### Q: What is DFIR, and what are the standard phases of Incident Response?
**A:** DFIR represents the intersection of post-breach investigation and crisis management:
- **Digital Forensics:** The rigorous, scientifically-backed process of preserving, identifying, extracting, and documenting digital evidence to establish a timeline of adversarial actions while maintaining a legal chain of custody.
- **Incident Response (IR):** The rapid, structured approach to mitigating a breach to limit systemic damage.

**The NIST Incident Response Lifecycle (PICERL):**
1. **Preparation:** Establishing an IR plan, playbooks, and deploying monitoring tools.
2. **Identification/Detection:** Correlating logs and alerts to confirm a breach has occurred.
3. **Containment:** Stopping the bleed (e.g., logically isolating a compromised server at the switch level).
4. **Eradication:** Removing the root cause (e.g., purging malware, closing firewall gaps).
5. **Recovery:** Restoring services from clean backups and validating system integrity.
6. **Lessons Learned:** Conducting a post-mortem analysis to improve future resilience.

---

## 5. Security Operations Center (SOC) & SIEM/EDR

### Q: Describe the function of a SOC.
**A:** A Security Operations Center (SOC) is a centralized unit that continuously monitors, detects, analyzes, and responds to cybersecurity incidents. It unites people, processes, and technology to defend against threats 24/7.

### Q: What is a SIEM, and how does it function?
**A:** **SIEM (Security Information and Event Management)** aggregates, normalizes, and analyzes log data from across an organization's entire IT infrastructure.
- **Core Functions:** Log Aggregation, Correlation (using AI to connect unrelated events, e.g., "Impossible Travel"), and Alerting.
- **Examples:** Splunk, IBM QRadar, Microsoft Sentinel.

### Q: What is EDR, and how does it differ from traditional Antivirus?
**A:** **EDR (Endpoint Detection and Response)** is an advanced endpoint security solution that continuously records system behaviors (process executions, memory injections).
- **Difference from AV:** Traditional AV relies on *signature-based detection* (matching known bad files). EDR relies on *behavioral analysis* to detect fileless malware or zero-day threats and allows remote endpoint isolation.
- **Examples:** CrowdStrike Falcon, SentinelOne, Microsoft Defender for Endpoint.

---

## 6. OSINT & Reconnaissance

### Q: What is OSINT and how is it used in Cybersecurity?
**A:** **OSINT (Open Source Intelligence)** is the collection, analysis, and dissemination of information that is publicly available and legally accessible. In cybersecurity, it is heavily used during the Reconnaissance phase by both attackers (to profile a target) and defenders (for threat intelligence).
- **Sources:** Social media, public DNS records, WHOIS databases, search engine dorks, government records, and the dark web.

### Q: Name some popular OSINT Tools.
**A:**
- **Shodan / Censys:** Search engines for internet-connected devices (IoT, exposed servers, open databases).
- **theHarvester:** Gathers emails, subdomains, hosts, and employee names from different public sources.
- **Maltego:** An interactive data mining tool that renders complex graphs for link analysis and entity relationships.
- **Google Dorks:** Using advanced search operators (e.g., `site:example.com filetype:pdf`) to find hidden or exposed data.
- **Recon-ng:** A full-featured Web Reconnaissance framework written in Python.

---

## 7. Network Security & Intrusion Detection

### Q: What is an Intrusion Detection System (IDS), and how does it differ by type and detection methodology?
**A:** An IDS is a passive monitoring system designed to detect malicious activities and policy violations. (An IPS—Intrusion Prevention System—actively drops malicious traffic).

**By Type:**
- **NIDS (Network IDS):** Monitors transit traffic across an entire subnet via a SPAN port. *(Examples: Snort, Zeek).*
- **HIDS (Host-based IDS):** Installed locally on endpoints to monitor internal logs and file integrity. *(Example: OSSEC).*

**By Methodology:**
- **Signature-Based:** Compares packet payloads against known malware signatures. Fast, but blind to zero-day attacks.
- **Anomaly-Based:** Uses baselining and machine learning to alert on statistical deviations. Detects novel threats but has a high false-positive rate.

### Q: Explain the mechanics of common network-layer attacks.
**A:**
- **DoS / DDoS (Denial of Service):** Exhausting resources (bandwidth, CPU) of a target. DDoS utilizes a decentralized botnet.
- **Man-in-the-Middle (MitM):** An adversary secretly relays and alters communications (e.g., via ARP Spoofing).

---

## 8. Adversarial Tactics: Malware & Social Engineering

### Q: What is Social Engineering, and what are its primary vectors?
**A:** The psychological manipulation of humans to extract confidential information or bypass security.
- **Phishing:** Fraudulent mass emails.
- **Spear Phishing:** Highly targeted phishing crafted for a specific individual using OSINT.
- **Whaling:** Spear phishing targeting high-level executives (C-Suite).
- **Vishing & Smishing:** Voice phishing (phone calls) and SMS phishing (texts).
- **Tailgating:** Following an authorized employee through a secure physical door.

### Q: Define Malware and its distinct variants.
**A:** Malicious Software intended to compromise systems.
- **Ransomware:** Cryptographically locks files for extortion.
- **Trojan:** Malware disguised as legitimate software.
- **Worm:** Self-propagating malware that moves laterally without human interaction.
- **Rootkit:** Stealth malware designed to gain administrative control while hiding from the OS.

---

## 9. Web Application Security (OWASP)

### Q: What is the OWASP Top 10? Provide examples of critical vulnerabilities.
**A:** The Open Worldwide Application Security Project (OWASP) Top 10 highlights the most critical web application risks.
1. **Injection (e.g., SQLi):** Untrusted input is sent directly to an interpreter. *(Example: Injecting `' OR 1=1;--` to dump a database).*
2. **Cross-Site Scripting (XSS):** Injecting malicious client-side JavaScript into a web page viewed by other users to steal session cookies.
3. **Cross-Site Request Forgery (CSRF):** Forcing an authenticated user's browser to execute unwanted, state-changing actions (like transferring funds).

---

## 10. Ethical Hacking Methodology

### Q: Detail the phases of the Ethical Hacking (Penetration Testing) lifecycle.
**A:** Penetration testing is the authorized, simulated cyberattack against a system:
1. **Reconnaissance (Footprinting):** Gathering intelligence on the target using OSINT, DNS lookups, and social engineering.
2. **Scanning & Enumeration:** Actively probing the target to identify live hosts, open ports, running services, and OS versions using tools like Nmap.
3. **Vulnerability Analysis:** Mapping identified services to known vulnerabilities using scanners like Nessus or OpenVAS.
4. **Exploitation (Gaining Access):** Leveraging vulnerabilities to breach the system (e.g., using Metasploit for a buffer overflow).
5. **Post-Exploitation (Maintaining Access):** Escalating privileges (e.g., to SYSTEM/root), pivoting to other network segments, and installing backdoors.
6. **Reporting:** The most critical phase. Documenting findings, risk levels, and providing actionable remediation guidance to the client.

### Q: What distinguishes Ethical Hacking from malicious activities from a legal perspective?
**A:** The distinction rests entirely on **Authorization, Scope, and Intent**.
- **Rules of Engagement (RoE):** A legally binding document defining the exact parameters of the test.
- **Scope Restriction:** An ethical hacker must *never* target assets outside the mutually agreed scope.
- **Intent:** Ethical hacking seeks to patch vulnerabilities; malicious hacking seeks exploitation for harm or financial gain.

---
<div align="center">
Made with ❤️ for the cybersecurity community.
</div>
