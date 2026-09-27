# 🚀 VERA Engine — magicpin AI Challenge

An intelligent, deterministic merchant growth messaging engine built for **magicpin's VERA AI Challenge**. The engine analyzes real-time contextual triggers, merchant performance metrics, active offer catalogs, and industry-specific nuances to compose highly personalized, high-conversion outreach messages.

---

## 🌟 Key Features

- **Context-Aware Message Composition (`/v1/tick`):** Dynamically parses 5 business verticals (*Dentists, Salons, Restaurants, Gyms, Pharmacies*) and generates personalized engagement campaigns grounded in real-time triggers.
- **Stateful Interaction & Intent Handoff (`/v1/reply`):** Automatically detects merchant commitments ("YES", "Proceed"), handles objection/hostile messages gracefully, and detects auto-reply patterns to prevent unnecessary loops.
- **Zero Hallucination & High Specificity:** Uses strict fallback templates and real entity payloads (offers, dates, recall guidelines) to achieve top-tier specificity scores on LLM evaluation harnesses.
- **FastAPI Core Architecture:** Lightweight, asynchronous, and designed to seamlessly pass the official `judge_simulator` test suit with sub-200ms API latency.

---

## 🏗️ Architecture & Supported Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/v1/healthz` | `GET` | Health check and server status |
| `/v1/metadata` | `GET` | Team metadata and model scope information |
| `/v1/context` | `POST` | Ingests merchant, customer, category, and trigger context |
| `/v1/tick` | `POST` | Processes pending triggers and returns actionable campaigns |
| `/v1/reply` | `POST` | Statefully handles merchant conversation replies and transitions |

---

## 🛠️ Tech Stack

- **Framework:** FastAPI / Uvicorn (Python 3.10+)
- **Testing & Evaluation Harness:** LLM-Powered `judge_simulator.py`
- **Deployment Platform:** Render / ngrok (Public HTTPS Endpoint)

---

## ⚡ Quickstart

1. **Clone & Install Dependencies:**
   ```bash
   git clone [https://github.com/krishna2720/magicpin-vera-engine.git](https://github.com/krishna2720/magicpin-vera-engine.git)
   cd magicpin-vera-engine
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt