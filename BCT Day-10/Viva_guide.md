# Comprehensive Cybersecurity Viva & Interview Guide

This guide is designed to serve as a rigorous reference for cybersecurity vivas, technical interviews, and academic assessments. It covers foundational concepts, frameworks, network defense mechanisms, and ethical hacking methodologies in detail.

---

## Table of Contents

1. [Foundations of Security](#1-foundations-of-security)
2. [Security Frameworks & Domains](#2-security-frameworks--domains)
3. [Threat Intelligence & Vulnerability Management](#3-threat-intelligence--vulnerability-management)
4. [Digital Forensics & Incident Response (DFIR)](#4-digital-forensics--incident-response-dfir)
5. [Security Operations Center (SOC)](#5-security-operations-center-soc)
6. [SIEM & EDR Technologies](#6-siem--edr-technologies)
7. [Network Security & Intrusion Detection](#7-network-security--intrusion-detection)
8. [Adversarial Tactics: Malware & Social Engineering](#8-adversarial-tactics-malware--social-engineering)
9. [Web Application Security (OWASP)](#9-web-application-security-owasp)
10. [Ethical Hacking Methodology](#10-ethical-hacking-methodology)

---

## 1. Foundations of Security

### Q: What is Cybersecurity, and how does it relate to Information Security (InfoSec)?
**A:** 
- **Information Security (InfoSec)** is the overarching discipline of protecting information—both physical and digital—from unauthorized access, disclosure, disruption, modification, or destruction. Its core objective is maintaining the **CIA Triad**:
  - **Confidentiality:** Ensuring data is accessible only to authorized entities (e.g., via Encryption).
  - **Integrity:** Ensuring data remains accurate and unaltered by unauthorized entities (e.g., via Hashing).
  - **Availability:** Ensuring systems and data are accessible when needed (e.g., via Redundancy and DDoS mitigation).
- **Cybersecurity** is a specialized sub-domain of InfoSec. It is specifically concerned with protecting internet-connected systems, networks, hardware, and digital data from cyber threats. 
*Example:* Locking a filing cabinet is InfoSec; configuring a Next-Generation Firewall (NGFW) is Cybersecurity.

---

## 2. Security Frameworks & Domains

### Q: Explain the 8 Domains of Cybersecurity defined by the CISSP framework.
**A:** The Certified Information Systems Security Professional (CISSP) framework provides a globally recognized taxonomy for security operations:
1. **Security and Risk Management:** Governance, risk assessments, compliance frameworks (NIST, ISO 27001), and security policies.
2. **Asset Security:** Data classification, data lifecycle management, privacy laws (GDPR), and secure media disposal.
3. **Security Architecture and Engineering:** Implementing secure design principles, cryptography, and physical facility security.
4. **Communication and Network Security:** Securing network topologies, VPNs, IPsec, and firewalls.
5. **Identity and Access Management (IAM):** Authentication models (MFA), authorization (RBAC, ABAC), and identity lifecycle management.
6. **Security Assessment and Testing:** Conducting penetration tests, vulnerability assessments, and security audits.
7. **Security Operations:** Managing the day-to-day security posture, Incident Response (IR), Disaster Recovery (DR), and Business Continuity Planning (BCP).
8. **Software Development Security:** Enforcing secure coding practices, DevSecOps, and the Secure Software Development Life Cycle (SSDLC).

---

## 3. Threat Intelligence & Vulnerability Management

### Q: Distinguish between a Vulnerability, a Threat, and a Risk.
**A:** These terms form the foundation of risk management:
- **Vulnerability:** An inherent weakness or flaw in a system, process, or architectural design that can be exploited. 
  *Example:* Hardcoded API keys in a public GitHub repository.
- **Threat:** An external or internal agent, circumstance, or event that possesses the capability to exploit a vulnerability. 
  *Example:* A malicious insider, an APT (Advanced Persistent Threat) group, or a natural disaster.
- **Risk:** The statistical probability of a threat exploiting a vulnerability and the resulting business impact. 
  *(Risk = Threat × Vulnerability × Impact).* 
  *Example:* The risk of financial loss resulting from a ransomware gang (threat) exploiting an unpatched RDP server (vulnerability).

---

## 4. Digital Forensics & Incident Response (DFIR)

### Q: What is DFIR, and what are the standard phases of Incident Response?
**A:** DFIR represents the intersection of post-breach investigation and crisis management:
- **Digital Forensics:** The rigorous, scientifically-backed process of preserving, identifying, extracting, and documenting digital evidence to establish a timeline of adversarial actions while maintaining a legal chain of custody.
- **Incident Response (IR):** The rapid, structured approach to mitigating a breach to limit systemic damage.

**The NIST Incident Response Lifecycle (PICERL):**
1. **Preparation:** Establishing an IR plan, playbooks, and deploying monitoring tools.
2. **Identification/Detection:** Correlating logs and alerts to confirm a breach has occurred.
3. **Containment:** Stopping the bleed. (e.g., logically isolating a compromised server at the switch level).
4. **Eradication:** Removing the root cause (e.g., purging malware, closing firewall gaps).
5. **Recovery:** Restoring services from clean backups and validating system integrity.
6. **Lessons Learned:** Conducting a post-mortem analysis to improve future resilience.

---

## 5. Security Operations Center (SOC)

### Q: Describe the function of a SOC.
**A:** A Security Operations Center (SOC) is a centralized unit that continuously monitors, detects, analyzes, and responds to cybersecurity incidents. It acts as the central command post for an organization's network telemetry, uniting people, processes, and technology to defend against threats 24/7.

---

## 6. SIEM & EDR Technologies

### Q: What is a SIEM, and how does it function?
**A:** **SIEM (Security Information and Event Management)** is a technology solution that aggregates, normalizes, and analyzes log data from across an organization's entire IT infrastructure (firewalls, servers, routers, endpoints).
- **Core Functions:** 
  1. **Log Collection & Aggregation:** Centralizing logs into one dashboard.
  2. **Correlation:** Using rules and AI to connect seemingly unrelated events. For example, if a user fails login 10 times in London, and then successfully logs in from Russia 5 minutes later, the SIEM flags it as an "Impossible Travel" anomaly.
  3. **Alerting:** Triggering high-priority alerts for SOC analysts.
- *Examples:* Splunk, IBM QRadar, Microsoft Sentinel.

### Q: What is EDR, and how does it differ from traditional Antivirus?
**A:** **EDR (Endpoint Detection and Response)** is an advanced endpoint security solution that continuously records system behaviors and events (like process executions, registry changes, and memory injections) on endpoints (laptops, servers).
- **Difference from Antivirus:** Traditional AV relies primarily on *signature-based detection* (matching known bad files). EDR relies on *behavioral analysis*. EDR can detect fileless malware or zero-day threats by observing malicious behaviors, even if the file itself has never been seen before. It also allows analysts to remotely isolate the compromised endpoint.
- *Examples:* CrowdStrike Falcon, SentinelOne, Microsoft Defender for Endpoint.

---

## 7. Network Security & Intrusion Detection

### Q: What is an Intrusion Detection System (IDS), and how does it differ by type and detection methodology?
**A:** An IDS is a passive monitoring system designed to detect malicious activities and policy violations, generating alerts for SOC analysts. (Note: An IPS—Intrusion Prevention System—actively drops malicious traffic).

**By Type:**
- **NIDS (Network IDS):** Deployed on a network segment (often via a SPAN port) to passively monitor transit traffic across the entire subnet. *Examples: Snort, Zeek, Suricata.*
- **HIDS (Host-based IDS):** Installed locally on individual endpoints or servers to monitor internal system logs, file integrity (FIM), and local traffic. *Example: OSSEC, Wazuh.*

**By Methodology:**
- **Signature-Based:** Compares packet payloads against a database of known malware signatures and exploit patterns. Fast, but blind to zero-day attacks.
- **Anomaly/Heuristic-Based:** Uses baselining and machine learning to establish a "normal" state, alerting on statistical deviations. High false-positive rate but capable of detecting novel threats.

### Q: Explain the mechanics of common network-layer attacks.
**A:**
- **DoS (Denial of Service):** Exhausting the computational or bandwidth resources of a target system from a single source (e.g., a SYN Flood).
- **DDoS (Distributed Denial of Service):** A volumetric DoS attack launched simultaneously from thousands of compromised nodes (a botnet), making IP blocking difficult.
- **Man-in-the-Middle (MitM):** An adversary secretly relays and possibly alters the communications between two parties. Commonly achieved on local networks via **ARP Spoofing**.

---

## 8. Adversarial Tactics: Malware & Social Engineering

### Q: What is Social Engineering, and what are its primary vectors?
**A:** Social Engineering bypasses technical controls by manipulating human psychology to extract confidential information or bypass security protocols.
- **Phishing:** Mass-distributed, fraudulent emails designed to harvest credentials.
- **Spear Phishing:** Highly targeted phishing crafted for a specific individual, utilizing OSINT (Open Source Intelligence) for personalization.
- **Whaling:** Spear phishing targeting high-level executives (C-Suite) who have access to highly sensitive data.
- **Vishing & Smishing:** Voice phishing (fraudulent phone calls) and SMS phishing (fraudulent text messages).
- **Tailgating / Piggybacking:** An unauthorized individual following an authorized employee through a secure physical door.

### Q: Define Malware and its distinct variants.
**A:** Malicious Software intended to damage, disable, or compromise systems.
- **Ransomware:** Cryptographically locks files and demands cryptocurrency for the decryption key.
- **Trojan Horse:** Malware disguised as legitimate, benign software to trick users into executing it.
- **Worm:** Self-propagating malware that moves laterally across a network without requiring human interaction or a host file.
- **Rootkit:** Stealth malware designed to gain administrative control while hiding its presence from the OS and antivirus.

---

## 9. Web Application Security (OWASP)

### Q: What is the OWASP Top 10, and can you detail a few critical web vulnerabilities?
**A:** The Open Worldwide Application Security Project (OWASP) Top 10 is a globally recognized awareness document highlighting the most critical web application vulnerabilities.
1. **Injection (e.g., SQLi):** Occurs when untrusted user input is sent directly to an interpreter. An attacker can inject SQL commands (e.g., `' OR 1=1;--`) to dump database tables, bypass authentication, or execute OS commands.
2. **Cross-Site Scripting (XSS):** An attacker injects malicious client-side JavaScript into a web page viewed by other users. When executed, it can steal session cookies or redirect the victim.
   - *Stored XSS:* Payload is saved in the database (e.g., a malicious forum post).
   - *Reflected XSS:* Payload is reflected immediately in the response (e.g., in a search query parameter).
3. **Cross-Site Request Forgery (CSRF):** Exploits a user's active, authenticated session by forcing their browser to execute unwanted, state-changing actions (like transferring funds) without their consent.

---

## 10. Ethical Hacking Methodology

### Q: Detail the phases of the Ethical Hacking (Penetration Testing) lifecycle.
**A:** Penetration testing is the authorized, simulated cyberattack against a system to evaluate its security.
1. **Reconnaissance (Footprinting):** Gathering intelligence on the target. 
   - *Passive:* OSINT, WHOIS lookups, social media scraping (no direct contact with the target).
   - *Active:* DNS zone transfers, direct interactions.
2. **Scanning & Enumeration:** Actively probing the target to identify live hosts, open ports, running services, and OS versions (e.g., using Nmap).
3. **Vulnerability Analysis:** Mapping identified services to known vulnerabilities (e.g., using Nessus or OpenVAS).
4. **Exploitation (Gaining Access):** Leveraging identified vulnerabilities to breach the system (e.g., using Metasploit to exploit a buffer overflow).
5. **Post-Exploitation (Maintaining Access & Lateral Movement):** Escalating privileges (e.g., from a standard user to SYSTEM/root), dumping password hashes, pivoting to other network segments, and installing backdoors.
6. **Reporting:** The most critical phase. Documenting findings, risk levels, and providing actionable remediation guidance.

### Q: What distinguishes Ethical Hacking from malicious activities from a legal perspective?
**A:** The distinction rests entirely on **Authorization and Scope**.
- **Rules of Engagement (RoE):** A legally binding document defining the exact parameters of the test (e.g., acceptable testing hours, allowed techniques, prohibition of DoS attacks).
- **Scope Restriction:** An ethical hacker must *never* target IP addresses, domains, or assets outside of the mutually agreed scope.
- **Intent:** Ethical hacking seeks to patch vulnerabilities to protect the business, whereas malicious hacking seeks exploitation for financial gain, espionage, or destruction.
