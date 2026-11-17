# ⚖️ NyayaSutra (न्यायसूत्र)
### *Democratizing Legal & Citizen Entitlements across Bharat via Voice-First Vernacular AI & BNS Knowledge Graphs*

<div align="center">

[![CI Pipeline](https://github.com/prachizala/NyayaSutra/actions/workflows/ci.yml/badge.svg)](https://github.com/prachizala/NyayaSutra/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

</div>

---

## 📌 Problem & Mission

Over **85% of citizens in Bharat** face severe information asymmetry when dealing with court notices, police FIRs, land revenue records (7/12 Satbara, Hakku Patra, Registry deeds), and government entitlement schemes. Legal legalese in India is predominantly drafted in English or complex bureaucratic language, forcing citizens to pay steep middleman fees.

Existing legal AI solutions exclusively serve corporate law firms in English ($1,000+/mo). **NyayaSutra** bridges this gap as an **offline-ready, voice-first multimodal AI system** designed for Indian vernacular languages (Gujarati, Hindi, Marathi, etc.) with automated **IPC-to-BNS 2023 law mapping**.

```
    Citizen Voice Note (Gujarati/Hindi)
                    OR
    Scanned Court / Land Document Photo
                    │
                    ▼
       ┌────────────────────────┐
       │   NyayaSutra Ingestion  │ (Bhashini OCR + Layout Engine)
       └────────────┬───────────┘
                    ▼
       ┌────────────────────────┐
       │   BNS Knowledge Engine │ (Automatic IPC 1860 ➔ BNS 2023 concordance)
       └────────────┬───────────┘
                    ▼
       ┌────────────────────────┐
       │ Vernacular Synthesizer │ (Audio voice summary + 1-Click Legal Notice PDF)
       └────────────────────────┘
```

---

## 🚀 Key Features

- **IPC to BNS 2023 Concordance Engine:** Maps legacy Indian Penal Code sections (e.g. IPC 420, IPC 302, IPC 441) to newly enacted Bharatiya Nyaya Sanhita 2023 provisions (BNS 318, BNS 103, BNS 329) with plain-language vernacular explanations.
- **Vernacular Voice Bridge:** Translates complex legal legalese into natural conversational audio in Gujarati, Hindi, and regional dialects.
- **Automated Citizen Notice Drafting:** Generates formal, legally compliant grievance and land dispute notices in seconds.
- **Zero-Leak Enterprise Security:** Standardized configuration templates, strict environment isolation, and comprehensive test suites.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.10+, FastAPI, Pydantic v2
- **Testing & Quality:** Pytest, Pytest-Asyncio, Ruff, GitHub Actions CI
- **Templating & Drafting:** Jinja2 Legal Document Generation
- **Vernacular AI Integrations:** Bhashini API, Gemini Multimodal Vision API, Whisper

---

## 📦 Quickstart

```bash
# Clone the repository
git clone https://github.com/prachizala/NyayaSutra.git
cd NyayaSutra

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies in editable mode
pip install -e ".[dev]"

# Configure environment
cp .env.example .env

# Run test suite
pytest

# Start local API server
uvicorn nyayasutra.api:app --reload --port 8000
```

---

## ⚖️ Legal Disclaimer

NyayaSutra provides informational analysis, translation, and automated administrative drafting assistance. It does not constitute formal advocate-client privilege or licensed legal representation under the Advocates Act, 1961.

---

## 👩‍💻 Author & Engineering

**Prachi Zala**  
*Full Stack Developer*  
GitHub: [@prachizala](https://github.com/prachizala) • [LinkedIn](https://www.linkedin.com/in/prachi-zala-74a08b334/)
