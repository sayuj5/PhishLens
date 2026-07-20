# PhishLens

<p align="center">
  <img src="images/logo.png" alt="PhishLens Logo" width="200" />
</p>

> ## 🎓 Academic Project Notice
>
> **PhishLens** was developed as part of the **Bachelor of Computer Applications (BCA/BCT) Training Program** under **JIS University**.
>
> Developed by **Sayuj Sur**.
>
> This repository is intended for cybersecurity education, research, and demonstration of explainable heuristic phishing URL detection.

---

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="MIT License" />
  <img src="https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB" alt="React" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat&logo=FastAPI&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/TypeScript-007ACC?style=flat&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white" alt="TailwindCSS" />
  <img src="https://img.shields.io/badge/Framer_Motion-0055FF?style=flat&logo=framer&logoColor=white" alt="Framer Motion" />
  <img src="https://img.shields.io/badge/Vite-B73BFE?style=flat&logo=vite&logoColor=FFD62E" alt="Vite" />
  <img src="https://img.shields.io/badge/Open_Source-Yes-success.svg" alt="Open Source" />
  <img src="https://img.shields.io/github/stars/sayuj5/PhishLens-?style=social" alt="GitHub Stars" />
  <img src="https://img.shields.io/github/forks/sayuj5/PhishLens-?style=social" alt="GitHub Forks" />
  <img src="https://img.shields.io/github/last-commit/sayuj5/PhishLens-" alt="Last Commit" />
</p>

## Project Overview

**PhishLens** is a completely stateless, privacy-first cybersecurity platform that analyzes URLs using a proprietary explainable heuristic engine.

### Why does it exist?
Most modern URL scanners (like VirusTotal or Google Safe Browsing) operate as black boxes—they check a URL against a database of known malicious domains and return a binary safe/unsafe result. PhishLens solves the problem of **explainability**. Instead of relying on reputation APIs or databases, it analyzes the structural anatomy of the URL in real-time, explaining *why* a URL is suspicious.

### The PhishLens Difference
- **No Third-Party APIs**: Every score is deterministically calculated through our own heuristic algorithms.
- **Privacy First**: URLs are never stored, sent to third-party providers, or aggregated.
- **Fully Stateless**: Analysis happens locally, leaving zero footprint.
- **Explainable Scoring**: Every point added to the risk score is justified with direct evidence and mitigation recommendations.

## Features

- 🧠 **Explainable Heuristic Engine**: Real-time evaluation of structural anomalies.
- 🎯 **Risk Meter**: Animated gauge displaying the exact severity score.
- 📊 **Confidence Score**: Algorithmic certainty measurement.
- 🌌 **Modern UI**: Dark Premium SaaS aesthetic with glassmorphism.
- 📄 **Export Capabilities**: Download reports as JSON or PDF.
- 🔤 **Entropy Analysis**: Shannon entropy calculation to detect Domain Generation Algorithms (DGA).
- 🔑 **Keyword Detection**: Identification of deceptive social engineering tokens.
- 🌐 **Suspicious TLD Detection**: Checking against historically abused Top Level Domains.
- 🧩 **Modular Detection Engine**: Easily extendable pipeline for new heuristics.
- 📱 **Responsive Design**: Flawless experience on desktop, tablet, and mobile.

## Tech Stack

### Frontend
| Technology | Description |
|---|---|
| **React** | Component-based UI rendering |
| **Vite** | Lightning-fast build tool |
| **TypeScript/JS** | Application logic |
| **TailwindCSS** | Utility-first styling (v4) |
| **Framer Motion** | 60fps fluid UI animations |
| **Lucide Icons** | Premium vector iconography |

### Backend
| Technology | Description |
|---|---|
| **FastAPI** | High-performance Python web framework |
| **Python** | Core backend language |
| **Pydantic** | Data validation and serialization |
| **Uvicorn** | ASGI server for asynchronous execution |

### Architecture
| Pattern | Implementation |
|---|---|
| **Clean Architecture** | Strict separation of UI, business logic, and API layers |
| **Modular Engine** | Pluggable heuristic detectors evaluated in sequence |
| **Stateless Backend** | Zero database requirements; purely functional transformations |

## Project Structure

```text
PhishLens/
├── backend/
│   ├── app/
│   │   ├── engine/
│   │   │   └── heuristics.py
│   │   └── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── engine/
│   ├── index.html
│   └── vite.config.js
├── images/
│   └── logo.png
├── README.md
└── LICENSE
```

## Screenshots

### Landing Page
![Landing Page](images/Screenshot_2026_07_20-2.png)

### URL Analysis
![URL Analysis](images/Screenshot_2026_07_20-3.png)

### Risk Report
![Risk Report](images/Screenshot_2026_07_20-4.png)

### Explainability Panel
![Explainability Panel](images/Screenshot_2026_07_20-5.png)

## Workflow

```mermaid
graph TD;
    A[User enters URL] --> B[URL Parser & Normalizer];
    B --> C[Heuristic Engine Pipeline];
    C --> D[Entropy Detector];
    C --> E[Keyword Detector];
    C --> F[Subdomain & TLD Detectors];
    D --> G[Scoring Engine];
    E --> G;
    F --> G;
    G --> H[Animated Risk Meter];
    H --> I[Detailed Report & Recommendations];
```

## Heuristics

| Rule | Description | Severity | Weight (PTS) |
|---|---|---|---|
| **IP Address Host** | Detects if the URL uses an IP instead of a domain name. | Critical | +80 |
| **Suspicious Length** | Flags URLs intentionally elongated to hide payloads. | Warning | Variable (max 40) |
| **Deceptive Keywords** | Detects social engineering tokens (e.g., 'login', 'secure'). | High/Warning | +30 per keyword |
| **Excessive Subdomains** | Evaluates subdomain depth to detect spoofing attempts. | Warning | Variable |
| **Suspicious TLD** | Flags abuse-heavy top level domains (.xyz, .top, etc.). | High | +45 |
| **High Character Entropy** | Calculates structural Shannon entropy to detect DGA domains. | High | +35 |

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/sayuj5/PhishLens-.git
cd PhishLens-
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 3. Backend Setup (Optional API)
```bash
cd backend
python -m venv venv
```

**Activate environment:**
- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Requirements
- Node.js (v18+)
- Python (3.10+)
- npm
- Git
- Modern Web Browser (Chrome, Firefox, Safari, Edge)

## How It Works
1. **Parsing & Normalization**: The URL is broken down into its fundamental anatomical parts (protocol, domain, path, query).
2. **Analysis Pipeline**: The modular heuristic detectors execute concurrently, analyzing specific threat vectors.
3. **Scoring**: Each triggered heuristic contributes a deterministic point value.
4. **Confidence**: The system computes algorithmic certainty based on the combination of triggered rules.
5. **Recommendations**: Direct, actionable steps are generated based on the specific evidence captured.

## Security & Privacy Guarantee
- URLs are **never** stored.
- **No database** exists in the architecture.
- **No third-party reputation APIs** are queried.
- **No telemetry** or analytics tracking.
- The entire system is **100% stateless**.

## Roadmap
- [ ] Browser Extension Integration
- [ ] Public REST API Release
- [ ] Desktop Application (Electron/Tauri)
- [ ] Email Phishing Body Detection
- [ ] QR Code Malicious Link Scanner

---

## 👨‍💻 Developer

**Sayuj Sur**

Developed as part of the **JIS University BCA/BCT Training Program**.

If you found this project useful, consider giving the repository a ⭐ on GitHub.

---

Made with ❤️ for Cybersecurity Education.
