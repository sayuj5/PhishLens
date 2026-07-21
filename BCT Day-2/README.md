# 🛡️ BCT Day-2 — Cybersecurity Foundations

<p align="center">
  <img src="https://img.shields.io/badge/Domain-Cybersecurity-red?style=for-the-badge&logo=shield&logoColor=white" />
  <img src="https://img.shields.io/badge/Certification-CISSP-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Training-JIS%20University%20BCT-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Day-2-orange?style=for-the-badge" />
</p>

> ## 🎓 Academic Training Notice
>
> This folder is part of the **Bachelor of Technology in Computer Science & Engineering (B.Tech CSE) Beyond Curriculum Training (BCT)** conducted under **JIS University**.
>
> **Developed & Documented by: Sayuj Sur**
>
> This session focused on cybersecurity fundamentals — covering SOC operations, asset security, CISSP 8 domains, network security architecture, regulatory compliance, and cyber law.

---

## 📋 Table of Contents

- [🔭 Security Operations Center (SOC)](#-security-operations-center-soc)
- [🗄️ Asset Security](#️-asset-security)
- [🏛️ CISSP — The 8 Domains](#️-cissp--the-8-domains)
- [🌐 Network Security & Architecture](#-network-security--architecture)
- [📐 Architecture Diagrams](#-architecture-diagrams)
- [⚖️ Compliance & Cyber Law](#️-compliance--cyber-law)
- [📁 Folder Contents](#-folder-contents)

---

## 🔭 Security Operations Center (SOC)

A **Security Operations Center (SOC)** is a centralized unit of cybersecurity professionals that monitors, detects, analyzes, and responds to cybersecurity incidents in real time — 24 hours a day, 7 days a week, 365 days a year.

### 🏗️ SOC Structure & Tiers

```
┌─────────────────────────────────────────────────────────────┐
│                  SECURITY OPERATIONS CENTER                 │
├──────────────┬──────────────────┬───────────────────────────┤
│  TIER 1      │  TIER 2          │  TIER 3                   │
│  Analyst     │  Incident        │  Threat Hunting &         │
│  (Triage)    │  Responder       │  Forensics Expert         │
│              │                  │                           │
│  • Alert     │  • Deep dive     │  • Advanced malware       │
│    triage    │    investigation │    analysis               │
│  • Log       │  • Containment   │  • Zero-day research      │
│    monitoring│  • Remediation   │  • Intelligence feeds     │
└──────────────┴──────────────────┴───────────────────────────┘
```

### 🛠️ Core SOC Functions

| Function | Description |
|---|---|
| **Monitoring** | Continuous surveillance of networks, endpoints, and applications using SIEM tools |
| **Detection** | Identifying suspicious activity through correlation rules, anomaly detection, and threat intelligence |
| **Analysis** | Investigating alerts to determine if they are true positives or false positives |
| **Response** | Containing and eradicating threats, recovering systems, and documenting incidents |
| **Reporting** | Providing metrics, dashboards, and post-incident reports to leadership |
| **Threat Hunting** | Proactively searching for hidden threats that evade automated detection |

### 🔧 Key SOC Technologies

- **SIEM** (Security Information and Event Management) — e.g., Splunk, IBM QRadar, Microsoft Sentinel
- **SOAR** (Security Orchestration, Automation, and Response) — automated playbooks for incident response
- **EDR/XDR** — Endpoint Detection and Response / Extended Detection and Response
- **Threat Intelligence Platforms (TIP)** — aggregating global threat feeds
- **Vulnerability Scanners** — Nessus, Qualys, OpenVAS

---

## 🗄️ Asset Security

**Asset Security** is the practice of identifying, classifying, handling, and protecting an organization's information assets throughout their entire **lifecycle** — from creation to disposal.

### 📦 Information Asset Lifecycle

```
Create ──► Store ──► Use ──► Share ──► Archive ──► Destroy
  ↑                                                    ↑
  └──────────── Security Controls Applied ─────────────┘
```

### 🏷️ Data Classification Levels

| Level | Description | Example |
|---|---|---|
| 🔴 **Top Secret / Confidential** | Highest sensitivity; unauthorized disclosure causes critical damage | Encryption keys, trade secrets |
| 🟠 **Secret / Restricted** | Sensitive data; limited audience | Employee records, financial data |
| 🟡 **Sensitive / Internal** | Internal use only | Internal memos, procedures |
| 🟢 **Public / Unclassified** | Safe for public release | Marketing materials, press releases |

### 🔐 Asset Protection Principles

- **Data at Rest**: AES-256 encryption, full-disk encryption (BitLocker, FileVault)
- **Data in Transit**: TLS 1.3, VPN tunnels, HTTPS
- **Data in Use**: Memory encryption, secure enclaves (Intel SGX)
- **Data Retention**: Legal hold policies, GDPR-compliant retention schedules
- **Data Destruction**: DoD 5220.22-M wiping, physical shredding, degaussing

### 🧾 Asset Management Best Practices

1. Maintain a complete **Asset Inventory** (hardware, software, data)
2. Assign **Data Owners** responsible for classification and access control
3. Implement **DLP (Data Loss Prevention)** solutions
4. Enforce **Need-to-Know** and **Least Privilege** access
5. Audit asset access logs regularly

---

## 🏛️ CISSP — The 8 Domains

The **Certified Information Systems Security Professional (CISSP)** is the gold-standard certification in information security, governed by **(ISC)²**. It encompasses **8 domains** that collectively cover the breadth of cybersecurity practice.

---

### 🔷 Domain 1 — Security and Risk Management

> *"Security starts with understanding what you need to protect and why."*

Focuses on the foundational principles and governance frameworks of information security.

**Key Topics:**
- **CIA Triad** — Confidentiality, Integrity, Availability
- **Governance** — Policies, standards, procedures, guidelines
- **Legal & Regulatory Compliance** — GDPR, HIPAA, SOX, PCI-DSS
- **Business Continuity Planning (BCP)** — Ensuring operations survive disruptions
- **Risk Management** — Risk identification, assessment, mitigation, transfer, acceptance
- **Security Awareness Training** — Human-layer defense
- **Ethics** — (ISC)² Code of Ethics, professional responsibility

**Risk Formula:**
```
Risk = Threat × Vulnerability × Asset Value
```

---

### 🔷 Domain 2 — Asset Security

> *"You cannot protect what you don't know you have."*

Covers the classification, handling, and protection of data and information assets.

**Key Topics:**
- Data classification frameworks (Government vs. Commercial)
- Data handling policies and procedures
- Privacy protection (PII, PHI handling)
- Data retention and destruction (NIST SP 800-88)
- Scoping and tailoring security controls

---

### 🔷 Domain 3 — Security Architecture and Engineering

> *"Security must be designed in, not bolted on."*

Addresses the design and implementation of secure systems.

**Key Topics:**
- **Secure Design Principles** — Least Privilege, Defense in Depth, Fail-Safe Defaults
- **Security Models** — Bell-LaPadula (confidentiality), Biba (integrity), Clark-Wilson
- **Cryptography** — Symmetric (AES), Asymmetric (RSA), Hashing (SHA-256)
- **PKI (Public Key Infrastructure)** — Digital certificates, CAs, CRLs
- **Trusted Computing Base (TCB)** — The core of a secure OS
- **Virtualization & Cloud Security** — Hypervisor security, shared responsibility model
- **Physical Security** — Locks, badges, biometrics, CCTV

**Cryptographic Hash Properties:**
```
Pre-image resistance: Given H(x), cannot find x
Collision resistance:  Cannot find x ≠ y where H(x) = H(y)
Avalanche effect:      Small input change = drastically different hash
```

---

### 🔷 Domain 4 — Communication and Network Security

> *"Every packet is a potential threat vector."*

Focuses on securing network infrastructure and data transmission.

**Key Topics:**
- **OSI Model** — 7 layers and their security implications
- **TCP/IP Stack** — Protocol-level vulnerabilities (SYN flood, ARP poisoning)
- **Firewalls** — Packet-filtering, stateful, NGFW, WAF
- **VPN & Tunneling** — IPSec, SSL/TLS, L2TP, OpenVPN
- **Wireless Security** — WPA3, 802.1X/EAP, rogue AP detection
- **Network Segmentation** — DMZ, VLANs, micro-segmentation
- **Intrusion Detection/Prevention** — IDS vs. IPS (signature vs. anomaly-based)
- **Secure Protocols** — HTTPS, SFTP, SSH, DNSSEC

---

### 🔷 Domain 5 — Identity and Access Management (IAM)

> *"The right person gets the right access at the right time — and only then."*

Controls how identities are verified and what resources they can access.

**Key Topics:**
- **Authentication Factors** — Something you know, have, are (MFA)
- **SSO (Single Sign-On)** — SAML, OAuth 2.0, OpenID Connect
- **Access Control Models:**
  - **DAC** — Discretionary Access Control
  - **MAC** — Mandatory Access Control
  - **RBAC** — Role-Based Access Control
  - **ABAC** — Attribute-Based Access Control
- **Privileged Access Management (PAM)** — Protecting admin accounts
- **Directory Services** — LDAP, Active Directory
- **Provisioning & De-provisioning** — Joiner-Mover-Leaver lifecycle

---

### 🔷 Domain 6 — Security Assessment and Testing

> *"Test often, test everything, trust nothing."*

Covers verification that security controls are working as intended.

**Key Topics:**
- **Vulnerability Assessment** — Scanning for known weaknesses
- **Penetration Testing** — Simulated attacks (Black/White/Grey box)
- **Security Audits** — Internal & third-party compliance audits
- **Log Reviews & SIEM Analysis** — Pattern analysis for threat detection
- **Code Review** — Static (SAST) and Dynamic (DAST) analysis
- **Red Team vs. Blue Team** — Offensive vs. defensive exercises
- **Bug Bounty Programs** — Crowdsourced vulnerability discovery

---

### 🔷 Domain 7 — Security Operations

> *"Prevention is ideal, but detection and response are essential."*

Day-to-day operational security management.

**Key Topics:**
- **Incident Management** — Identification → Containment → Eradication → Recovery → Lessons Learned
- **Logging & Monitoring** — Centralized log management, SIEM correlation
- **Digital Forensics** — Chain of custody, evidence preservation, disk imaging
- **Disaster Recovery (DR)** — RTO (Recovery Time Objective), RPO (Recovery Point Objective)
- **Business Continuity** — Hot/Warm/Cold site strategies
- **Change Management** — Controlled change processes to prevent introducing vulnerabilities
- **Physical & Environmental Security** — Data center controls, HVAC, fire suppression
- **Anti-Malware Operations** — Signature-based + behavioral detection

**Incident Response Lifecycle:**
```
Preparation → Identification → Containment → Eradication → Recovery → Lessons Learned
```

---

### 🔷 Domain 8 — Software Development Security

> *"Secure code is not an afterthought — it's a requirement from line one."*

Integrates security into the Software Development Lifecycle (SDLC).

**Key Topics:**
- **Secure SDLC** — Requirements → Design → Development → Testing → Deployment → Maintenance
- **Security in Agile & DevSecOps** — Shifting security left
- **OWASP Top 10** — Most critical web application security risks
- **Input Validation** — Preventing SQLi, XSS, command injection
- **Secure Coding Standards** — CERT, MISRA C, SEI
- **API Security** — Authentication, rate limiting, input sanitization
- **Dependency Management** — SCA (Software Composition Analysis), CVE tracking
- **Code Signing** — Verifying software integrity and authenticity

---

## 🌐 Network Security & Architecture

### 🔐 Defense-in-Depth Architecture

Modern enterprise networks use a **layered security architecture** — no single control is relied upon; instead, multiple overlapping layers ensure that if one fails, others compensate.

### 🏗️ Layered Network Zones

| Zone | Trust Level | Components |
|---|---|---|
| **INTERNET** | Untrusted (0%) | Remote Offices, Mobile Devices, Public Users |
| **DMZ** | Semi-trusted (25%) | Firewall 1, VPN Gateway, Load Balancer, Web Servers |
| **TRUSTED** | Trusted (75%) | Firewall 2, Application Servers, Internal Services |
| **PRIVILEGED** | Fully Trusted (100%) | Mainframes, Core Databases, Critical Infrastructure |

### 🔥 Firewall Types

| Type | Description |
|---|---|
| **Packet-Filtering Firewall** | Inspects individual packets (Layer 3/4) — fast but limited |
| **Stateful Inspection Firewall** | Tracks connection state for more intelligent filtering |
| **Application-Layer (WAF)** | Inspects HTTP/HTTPS content (Layer 7) |
| **Next-Generation Firewall (NGFW)** | Combines all above + DPI, IPS, and threat intelligence |

### 🔑 Common Network Attack Vectors & Mitigations

| Attack | Description | Mitigation |
|---|---|---|
| **DDoS** | Overwhelm bandwidth/resources | Rate limiting, CDN, scrubbing centers |
| **Man-in-the-Middle (MitM)** | Intercept communications | TLS/HTTPS, certificate pinning |
| **ARP Poisoning** | Link IP to wrong MAC address | Dynamic ARP Inspection (DAI) |
| **DNS Spoofing** | Redirect DNS queries | DNSSEC validation |
| **SQL Injection** | Inject malicious SQL | Parameterized queries, WAF |
| **Phishing** | Social engineering via email | Email filters, user training, SPF/DKIM/DMARC |

---

## 📐 Architecture Diagrams

This folder contains two visual representations of the **Network Security Architecture** designed during BCT Day-2.

---

### 🖼️ Diagram 1 — PlantUML Rendered Architecture

**File:** `Network Scurity Architecture - 1.jpeg`

![Network Security Architecture - PlantUML Render](Network%20Scurity%20Architecture%20-%201.jpeg)

**Description:**
This diagram is the **rendered output** of the PlantUML code (available in `Network Scurity Architecture code.txt`). It shows the full layered network architecture with **four distinct security zones**:

- **🌐 INTERNET Zone** (Top): Entry points — *Remote Office* and *Mobile Devices* — represent external actors connecting to the organization's perimeter.
- **🔶 DMZ (Demilitarized Zone)**: The first line of internal defense. **Firewall 1** (highlighted in red) filters all inbound traffic. Traffic is then routed through either the **VPN Gateway** (for authenticated remote users) or the **Load Balancer** (for web traffic distribution).
- **🔷 TRUSTED Zone**: **Firewall 2** (second red node) acts as the inner perimeter, separating DMZ from trusted internal resources. **Application Services** and **Internal Services** reside here.
- **🟣 PRIVILEGED Zone** (Bottom): The most sensitive layer — the **Mainframe** (highlighted in purple), representing core organizational infrastructure with the highest trust and strictest access controls.

**Traffic Flow:** `Internet → Firewall 1 → VPN/Load Balancer → Firewall 2 → App Services → Mainframe`

---

### 🖼️ Diagram 2 — Interactive diagrams.net (draw.io) Architecture

**File:** `Network Scurity Architecture - 2.png`

![Network Security Architecture - draw.io](Network%20Scurity%20Architecture%20-%202.png)

**Description:**
This is the **interactive diagram** built using [app.diagrams.net](https://app.diagrams.net) (draw.io), representing the same four-zone architecture in a more visual, drag-and-drop format with dark theme styling.

Key observations from this diagram:
- The **INTERNET zone** contains *Remote Office* and *Mobile Devices* as the entry nodes.
- **DMZ zone** shows *Firewall 1*, *VPN Gateway*, and *Load Balancer* — with cross-connections indicating traffic routing paths.
- **TRUSTED zone** shows *Firewall 2*, *Internal Services*, and *Application Services* with directional arrows showing data flow.
- **PRIVILEGED zone** contains the *Mainframe* as the ultimate protected resource.
- The dark theme and labeled arrows make it easy to trace traffic paths across zones.

**Purpose:** This diagram was used as a working draft/planning tool before the final PlantUML render, demonstrating how security architecture can be visualized and iterated upon using interactive diagramming tools.

---

### 📄 PlantUML Source Code

**File:** `Network Scurity Architecture code.txt`

Contains the **PlantUML DSL source** that generated Diagram 1. Key architectural decisions reflected in the code:

```plantuml
package "INTERNET" → package "DMZ" → package "TRUSTED" → package "PRIVILEGED"
```

- Color coding: `#C0504D` (Red) for Firewalls, `#5F2E60` (Purple) for the Mainframe
- Uses `skinparam linetype ortho` for clean orthogonal connection lines
- Explicit hidden connections used to enforce vertical layout hierarchy

---

## ⚖️ Compliance & Cyber Law

### 📜 Major Cybersecurity Compliance Frameworks

| Framework | Full Name | Scope |
|---|---|---|
| **GDPR** | General Data Protection Regulation | EU citizen data privacy |
| **HIPAA** | Health Insurance Portability & Accountability Act | US healthcare data |
| **PCI-DSS** | Payment Card Industry Data Security Standard | Credit card data |
| **SOX** | Sarbanes-Oxley Act | US public company financial data |
| **ISO 27001** | Information Security Management System | Global ISMS standard |
| **NIST CSF** | NIST Cybersecurity Framework | US federal & critical infrastructure |
| **SOC 2** | Service Organization Control 2 | Cloud service provider audits |

### 🌍 GDPR — General Data Protection Regulation

The GDPR (2018) is the European Union's comprehensive data protection law that applies to **any organization processing EU citizens' data**, regardless of where the organization is based.

**Key GDPR Principles:**
- **Lawfulness, Fairness, Transparency** — Clear basis for data processing
- **Purpose Limitation** — Collect data only for specific, stated purposes
- **Data Minimization** — Collect only what is necessary
- **Accuracy** — Keep data up to date
- **Storage Limitation** — Don't keep data longer than needed
- **Integrity & Confidentiality** — Protect data with appropriate security

**Your Rights under GDPR:**
- Right to Access (Article 15)
- Right to Erasure / "Right to be Forgotten" (Article 17)
- Right to Data Portability (Article 20)
- Right to Object (Article 21)

**Penalties:** Up to **€20 million** or **4% of global annual revenue**, whichever is higher.

---

### 🇮🇳 Indian Cyber Law — IT Act 2000 & DPDP Act 2023

#### Information Technology Act, 2000 (IT Act)

India's primary legislation for cybercrime and electronic commerce.

| Section | Offense | Penalty |
|---|---|---|
| **Section 43** | Unauthorized computer access / damage | Civil liability — compensation |
| **Section 66** | Computer-related offenses (hacking) | Up to 3 years imprisonment + fine |
| **Section 66C** | Identity theft | Up to 3 years + ₹1 lakh fine |
| **Section 66D** | Cheating by personation using computer | Up to 3 years + ₹1 lakh fine |
| **Section 66E** | Violation of privacy | Up to 3 years + ₹2 lakh fine |
| **Section 66F** | Cyber terrorism | Life imprisonment |
| **Section 67** | Publishing obscene material online | Up to 5 years + ₹10 lakh fine |
| **Section 70** | Unauthorized access to Protected Systems | Up to 10 years imprisonment |
| **Section 72** | Breach of confidentiality and privacy | Up to 2 years + ₹1 lakh fine |

#### Digital Personal Data Protection Act, 2023 (DPDP Act)

India's modern data privacy legislation, inspired by GDPR, applicable to digital personal data processed in India.

**Key Provisions:**
- Consent-based data processing
- Data Fiduciaries must ensure accuracy and security of data
- Data Principals (individuals) have rights to access, correction, and erasure
- Cross-border data transfer restrictions
- Data Protection Board established for adjudication

**Penalties:** Up to **₹250 crore** for breaches of data security obligations.

---

### 🌐 International Cyber Law & Conventions

| Convention/Law | Details |
|---|---|
| **Budapest Convention on Cybercrime (2001)** | First international treaty on cybercrime; covers offenses against computer data/systems |
| **CFAA (USA)** | Computer Fraud and Abuse Act — unauthorized access to protected computers |
| **NIS2 Directive (EU)** | Network and Information Security — mandatory cybersecurity for critical sectors |
| **CCPA (California)** | California Consumer Privacy Act — US state-level data privacy law |

---

### ✅ Compliance Best Practices

1. **Conduct Regular Risk Assessments** — Identify gaps against chosen frameworks
2. **Implement Security Policies** — Documented, approved, and enforced
3. **Train Employees** — Annual security awareness and compliance training
4. **Maintain Audit Trails** — Logs for all access to sensitive data
5. **Perform Third-Party Audits** — Independent verification of controls
6. **Incident Response Plan** — Documented procedures for breach notification (GDPR: 72-hour reporting requirement)
7. **Data Protection Impact Assessments (DPIA)** — For high-risk processing activities

---

## 📁 Folder Contents

| File | Description |
|---|---|
| `README.md` | This comprehensive documentation file |
| `Network Scurity Architecture - 1.jpeg` | PlantUML-rendered layered network security architecture diagram |
| `Network Scurity Architecture - 2.png` | Interactive draw.io diagram of the same architecture (dark theme) |
| `Network Scurity Architecture code.txt` | PlantUML DSL source code for the architecture diagram |

---

## 🔗 References & Further Reading

- [(ISC)² CISSP Official Study Guide](https://www.isc2.org/certifications/cissp)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GDPR Official Text](https://gdpr-info.eu/)
- [India IT Act 2000](https://www.meity.gov.in/content/information-technology-act)
- [DPDP Act 2023](https://www.meity.gov.in/data-protection-framework)
- [PlantUML Documentation](https://plantuml.com/)
- [app.diagrams.net](https://app.diagrams.net)

---

<p align="center">
  Made with ❤️ for Cybersecurity Education | <strong>JIS University BCT — Day 2</strong><br/>
  <strong>Sayuj Sur</strong> · B.Tech CSE Beyond Curriculum Training
</p>
