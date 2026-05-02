# LandCare AI

**Created by:** Tôn Thất Minh Cường  
**Project type:** Personal non-official prototype  
**Status:** Early MVP scaffold  

LandCare AI is a personal, non-official AI prototype that helps citizens understand public land acquisition, compensation, and resettlement procedures.

The system transforms complex administrative documents and synthetic case descriptions into:

- plain-language explanations;
- document checklists;
- suggested questions to ask the competent authority;
- draft request letters for reference.

## Disclaimer

This project is for educational and demonstration purposes only. It does **not** represent any government agency. It uses only public legal documents and synthetic sample cases. It does **not** provide official legal advice or administrative decisions.

## MVP Scope

The first version focuses on one practical scenario:

> A citizen receives a land acquisition / inventory / compensation-related notice and wants to understand what stage they are in, what documents they should prepare, and what questions they should ask.

## Key Features

1. **Explain Notice**  
   Summarize an administrative document or case description in plain language.

2. **Document Checklist**  
   Generate a practical checklist of documents that a citizen may need to prepare.

3. **Draft Letter**  
   Draft a reference request letter for clarification, document supplementation, or re-checking information.

## Project Structure

```text
LandCare-AI/
├─ README.md
├─ requirements.txt
├─ .env.example
├─ app/
│  ├─ app.py
│  ├─ prompts.py
│  └─ utils.py
├─ data/
│  ├─ synthetic_cases/
│  │  └─ cases_vi.json
│  ├─ sample_forms/
│  │  └─ draft_request_letter_vi.md
│  └─ public_legal_notes/
│     └─ notes_vi.md
├─ docs/
│  ├─ project_brief.md
│  ├─ technical_writeup.md
│  ├─ demo_script.md
│  └─ submission_checklist.md
└─ outputs/
   ├─ sample_checklists/
   └─ sample_letters/
```

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Optional: configure API key

Copy `.env.example` to `.env` and add your model API key.

```bash
cp .env.example .env
```

The app can run in offline demo mode without an API key.

### 3. Run the app

```bash
streamlit run app/app.py
```

## Safety Principles

- No real citizen data.
- No internal government data.
- No official legal advice.
- No administrative decision-making.
- Always show a non-official disclaimer.
- Use public legal documents and synthetic cases only.

## Author

**Tôn Thất Minh Cường**  
Independent builder / Personal project
