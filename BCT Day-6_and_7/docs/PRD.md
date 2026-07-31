# BLACKFALCON - Product Requirement Document (PRD)

## Vision
BlackFalcon is a full enterprise vulnerability management platform for organisations to continuously monitor their infrastructure. It is designed to be a modern, defensive, authorised vulnerability assessment capability.

## Primary Users
- Security Teams
- SOC Analysts
- System Administrators
- Compliance Teams
- IT Departments
- Penetration Testers (authorised assessments)
- MSPs
- Researchers

## Major Modules

### Dashboard
- Executive Dashboard, Risk Score, Critical Vulnerabilities, Top Assets, Recent Scans, Trending CVEs, Threat Intelligence Summary, Live Scan Status, Risk Heatmap, Remediation Progress, Compliance Overview

### Asset Discovery
- Discover: IPv4, IPv6, Subnets, Domains, Hostnames, Servers, Cloud Instances, Containers, Virtual Machines, Network Devices, IoT Devices, Web Servers, Operating Systems, Services, Installed Software, Technologies, TLS Certificates, DNS, Reverse DNS, MAC Vendor.

### Scan Engine
- Fast Scan, Full Scan, Credentialed Scan, Network Scan, Web Scan, Compliance Scan, Patch Audit, Configuration Audit, Scheduled Scan, Recurring Scan, Custom Scan Profiles. Bandwidth Limiting, Timeout Control, Concurrent Scans.

### Vulnerability Detection
- Missing patches, Outdated software, Misconfigurations, Weak SSL/TLS, Weak Ciphers, Default Credentials, Expired Certificates, Open Ports, Insecure Services. CVEs, CVSS Scores, CPE Detection, CWE Mapping.

### Compliance
- PCI DSS, CIS Benchmarks, NIST, ISO 27001, SOC 2, HIPAA, GDPR, DISA STIG, Custom Policies.

### Reporting & Asset Management & Remediation
- PDF/HTML/CSV reports. Asset Inventory, Grouping, Tagging, Risk Classification. Assign Owner, Due Dates, Priority, Patch Tracking, Risk Acceptance.

### User Management & Notifications
- RBAC, SSO, LDAP, Active Directory, 2FA, Audit Logs, API Tokens. Email, Slack, Teams, Discord, Webhooks.

### Plugin Framework
- Plugin SDK, Marketplace, Loader, Versioning, Testing.
