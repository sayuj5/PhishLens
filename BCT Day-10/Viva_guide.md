# Cybersecurity Viva Guide

This comprehensive guide covers essential cybersecurity concepts, definitions, and interview/viva questions.

## Table of Contents
1. [Core Concepts](#1-core-concepts)
2. [Information Security vs. Cybersecurity](#2-information-security-vs-cybersecurity)
3. [Domains of Cybersecurity (CISSP 8 Domains)](#3-domains-of-cybersecurity-cissp-8-domains)
4. [DFIR (Digital Forensics and Incident Response)](#4-dfir-digital-forensics-and-incident-response)
5. [SOC (Security Operations Center)](#5-soc-security-operations-center)
6. [Threats, Vulnerabilities, and Risks](#6-threats-vulnerabilities-and-risks)
7. [Network Security & Intrusions](#7-network-security--intrusions)
8. [Malware, Phishing & Social Engineering](#8-malware-phishing--social-engineering)
9. [Web Application Security (OWASP)](#9-web-application-security-owasp)
10. [Ethical Hacking & Legal Boundaries](#10-ethical-hacking--legal-boundaries)

---

## 1. Core Concepts

**Q: What is Cybersecurity?**
**A:** Cybersecurity is the practice of protecting systems, networks, devices, and programs from digital attacks. These cyberattacks are usually aimed at accessing, changing, or destroying sensitive information, extorting money from users, or interrupting normal business processes.

**Example:** Using encryption, firewalls, and multi-factor authentication (MFA) to protect customer data on an e-commerce website.

---

## 2. Information Security vs. Cybersecurity

**Q: Does Cybersecurity fall under Information Security? What is the difference?**
**A:** Yes, Cybersecurity is a subset of Information Security (InfoSec).
- **Information Security (InfoSec):** Broadly covers the protection of *all* forms of information (physical and digital) from unauthorized access, ensuring Confidentiality, Integrity, and Availability (The CIA Triad).
- **Cybersecurity:** Specifically focuses on protecting *digital* data, networks, and internet-connected systems from cyber threats.

**Example:** Locking a filing cabinet containing paper records is InfoSec. Setting up a firewall to protect a database is Cybersecurity.

---

## 3. Domains of Cybersecurity (CISSP 8 Domains)

**Q: What are the 8 domains of the CISSP framework?**
**A:** The CISSP (Certified Information Systems Security Professional) framework defines 8 core domains of cybersecurity:

1. **Security and Risk Management:** Policies, risk assessments, and compliance.
2. **Asset Security:** Protecting data lifecycle, privacy, and media handling.
3. **Security Architecture and Engineering:** Designing secure systems, cryptography, and physical security.
4. **Communication and Network Security:** Securing network channels, firewalls, and VPNs.
5. **Identity and Access Management (IAM):** Authentication, authorization (Role-Based Access Control), and accounting.
6. **Security Assessment and Testing:** Vulnerability assessments, penetration testing, and auditing.
7. **Security Operations:** Incident response, disaster recovery, and SOC management.
8. **Software Development Security:** Secure coding practices (SDLC), OWASP guidelines.

---

## 4. DFIR (Digital Forensics and Incident Response)

**Q: Explain DFIR in detail.**
**A:** DFIR combines two crucial post-breach disciplines:
- **Digital Forensics:** The scientific process of preserving, identifying, extracting, and documenting digital evidence to be used in a court of law or internal investigation. (Who did it? How?)
- **Incident Response:** The structured approach to handling and managing the aftermath of a security breach or cyberattack to limit damage and reduce recovery time and costs.

**Phases of Incident Response (PICERL):**
1. **Preparation:** Having a plan, team, and tools ready.
2. **Identification:** Detecting the breach.
3. **Containment:** Isolating the infected systems (e.g., disconnecting a server from the network).
4. **Eradication:** Removing the root cause (e.g., deleting malware).
5. **Recovery:** Restoring systems to normal operation.
6. **Lessons Learned:** Post-incident review to prevent future occurrences.

---

## 5. SOC (Security Operations Center)

**Q: What is a SOC?**
**A:** A Security Operations Center (SOC) is a centralized facility or team responsible for continuously monitoring and analyzing an organization's security posture on an ongoing basis. The SOC team's goal is to detect, analyze, and respond to cybersecurity incidents using a combination of technology solutions and a strong set of processes.

**Key Tools used in a SOC:** SIEM (Security Information and Event Management) like Splunk or QRadar, EDR (Endpoint Detection and Response), and Threat Intelligence feeds.

---

## 6. Threats, Vulnerabilities, and Risks

**Q: Explain the difference between Vulnerability, Risk, and Threat.**
**A:** 
- **Vulnerability:** A weakness or flaw in a system, application, or process that can be exploited. 
  *Example:* An unpatched Windows server.
- **Threat:** Any potential danger that could exploit a vulnerability to breach security and cause harm. 
  *Example:* A hacker or ransomware.
- **Risk:** The intersection of a vulnerability and a threat. It is the probability that a threat will exploit a vulnerability and the impact it will have on the business. (Risk = Threat × Vulnerability × Impact).
  *Example:* The risk of losing financial data because a hacker (threat) exploits the unpatched server (vulnerability).

---

## 7. Network Security & Intrusions

**Q: What is an IDS and what are its types?**
**A:** An Intrusion Detection System (IDS) is a monitoring system that detects suspicious activities and generates alerts when they are detected.

**Types of IDS:**
1. **NIDS (Network Intrusion Detection System):** Placed at strategic points within the network to monitor traffic to and from all devices on the network. Promiscuous mode. *Example: Snort, Zeek.*
2. **HIDS (Host-based Intrusion Detection System):** Installed on a single host (computer/server) to monitor inbound and outbound packets from that specific machine, as well as file system modifications. *Example: OSSEC.*

**Detection Methods:**
- **Signature-based:** Compares traffic against a database of known attack patterns (like antivirus).
- **Anomaly-based:** Uses machine learning/baselining to detect deviations from "normal" behavior (good for detecting zero-day attacks).

**Q: What are common Network-related attacks?**
**A:**
- **DoS (Denial of Service):** Overwhelming a system with traffic from a single source so it cannot respond to legitimate requests.
- **DDoS (Distributed Denial of Service):** Same as DoS, but launched from a botnet (multiple compromised computers globally).
- **Man-in-the-Middle (MitM):** Intercepting communications between two parties (e.g., ARP Spoofing).
- **Packet Sniffing:** Capturing network traffic in transit.

---

## 8. Malware, Phishing & Social Engineering

**Q: What is Social Engineering and its types?**
**A:** Social engineering is the psychological manipulation of people into performing actions or divulging confidential information.

**Types:**
- **Phishing:** Fraudulent emails masquerading as a reputable entity to steal credentials.
- **Spear Phishing:** Highly targeted phishing aimed at a specific individual or organization.
- **Whaling:** Spear phishing targeting high-level executives (CEOs, CFOs).
- **Vishing / Smishing:** Voice phishing (phone calls) / SMS phishing (text messages).
- **Baiting:** Leaving a malware-infected USB drive in a parking lot hoping an employee plugs it in.
- **Tailgating:** Following an authorized person into a secure physical area without badging in.

**Q: What is Malware?**
**A:** Malicious software designed to cause harm.
- **Ransomware:** Encrypts files and demands payment for the decryption key.
- **Trojan:** Disguises itself as legitimate software.
- **Worm:** Self-replicating malware that spreads across networks without human interaction.
- **Spyware:** Secretly monitors user activity and steals data.

---

## 9. Web Application Security (OWASP)

**Q: What is OWASP and what are common web attacks?**
**A:** OWASP (Open Worldwide Application Security Project) provides unbiased, practical information about application security. The OWASP Top 10 is a standard awareness document representing the most critical security risks to web applications.

**Common Attacks:**
1. **SQL Injection (SQLi):** Inserting malicious SQL statements into input fields to manipulate the database. 
   *Example:* Inputting `' OR '1'='1` into a login field.
2. **Cross-Site Scripting (XSS):** Injecting malicious JavaScript into a web page viewed by other users to steal session cookies.
3. **Broken Authentication:** Weak session management allowing attackers to steal session IDs or brute-force passwords.
4. **Cross-Site Request Forgery (CSRF):** Forcing a logged-in user to execute unwanted actions on a web application they are authenticated on.

---

## 10. Ethical Hacking & Legal Boundaries

**Q: What is the Ethical Hacking Methodology?**
**A:** A structured approach used by authorized professionals to find vulnerabilities before malicious hackers do.
1. **Reconnaissance (Footprinting):** Gathering information about the target (Passive & Active).
2. **Scanning:** Identifying open ports, services, and vulnerabilities (e.g., using Nmap, Nessus).
3. **Gaining Access (Exploitation):** Exploiting identified vulnerabilities to access the system.
4. **Maintaining Access:** Creating backdoors or establishing persistence.
5. **Clearing Tracks:** Erasing logs to avoid detection.

**Q: What are the Legal and Ethical boundaries?**
**A:** The primary difference between a Black Hat hacker and an Ethical (White Hat) hacker is **Authorization and Intent**.
- **Rules of Engagement (RoE):** A signed document detailing exactly what can and cannot be tested during a penetration test.
- **Scope:** Testing must strictly adhere to the agreed-upon IP addresses or applications. Testing out of scope is illegal.
- **Non-Disclosure Agreement (NDA):** Ensuring any vulnerabilities found remain confidential.
