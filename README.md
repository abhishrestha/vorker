# Vorker — Swedish Business Compliance Agent

An AI-powered compliance advisor for Swedish SMEs, built with Google ADK. Vorker bridges the "Compliance Gap" by grounding every answer in authoritative Swedish legal sources — Skatteverket, Bolagsverket, Verksamt.se, and Riksdagen.se.

Built at the Vorker Hackathon (120-minute sprint).

---

## The Problem

General-purpose AI models give generic or outdated advice when asked about Swedish corporate law and tax regulations. For a business owner, a wrong answer about VAT or labor law is a significant liability.

Vorker solves this by combining a deeply specialized system prompt with live grounding tools that fetch real content from official Swedish government sources before answering.

---

## How It Works

```
User query
    ↓
ADK Agent (Gemini / LLaMA via NVIDIA)
    ↓
search_swedish_sources()   ← searches official .se domains
    ↓
fetch_official_page()      ← fetches actual legal text from the best URL
    ↓
Cited answer with source links + accountant disclaimer
```

---

## Features

- **Two-tool grounding pipeline** — searches then fetches actual page content
- **Source-restricted** — only fetches from skatteverket.se, bolagsverket.se, verksamt.se, riksdagen.se, arbetsmiljoverket.se
- **Hardcoded direct pages** for common topics (karensavdrag, moms, aktieägaravtal)
- **Always cites sources** — every answer includes the URL it was grounded in
- **Built-in disclaimer** — reminds users to verify with a certified Swedish accountant (revisor)

---

## Example Queries

```
Explain the specific requirements for an aktieägaravtal regarding 
the hembudsförbehåll in a Swedish AB.
```

```
How do I calculate karensavdrag for a part-time employee according 
to the latest Swedish labor laws?
```

```
What are the VAT implications for a Swedish company selling SaaS to 
a B2B customer in Norway compared to a B2C customer in Germany?
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Agent framework | [Google ADK](https://adk.dev) 2.2.0 |
| LLM | Gemini 2.0 Flash / LLaMA 3.1 70B via NVIDIA NIM |
| Web scraping | requests + BeautifulSoup4 |
| Environment | Python 3.11, venv |

---

## Project Structure

```
phase1/
├── vorker/
│   ├── __init__.py
│   ├── agent.py          # ADK agent definition + root_agent
│   ├── tools.py          # search_swedish_sources + fetch_official_page
│   └── system_prompt.py  # Expert persona and mandatory behavior rules
├── .env                  # API keys (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/vorker.git
cd vorker/phase1
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install google-adk requests beautifulsoup4 python-dotenv
```

For NVIDIA/LiteLLM support:
```bash
pip install "google-adk[extensions]" litellm
```

### 4. Configure environment variables

Create a `.env` file in `phase1/`:

```
# Option A: Google Gemini
GOOGLE_API_KEY=your_google_api_key

# Option B: NVIDIA NIM
NVIDIA_NIM_API_KEY=your_nvidia_api_key
```

Get a Google API key at [https://aistudio.google.com](https://aistudio.google.com)  
Get an NVIDIA API key at [https://build.nvidia.com](https://build.nvidia.com)

### 5. Run the agent

```bash
adk web vorker
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## Authoritative Sources

| Source | Domain | Used For |
|--------|--------|----------|
| Skatteverket | skatteverket.se | Tax, VAT, karensavdrag |
| Bolagsverket | bolagsverket.se | Company law, aktieägaravtal |
| Verksamt.se | verksamt.se | Business registration guidance |
| Riksdagen | riksdagen.se | Legislative text |
| Arbetsmiljöverket | arbetsmiljoverket.se | Labor law |

---
