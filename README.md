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

## Legal Sources Manifest

LandCare AI now includes a legal-source manifest located at:

```text
data/legal_sources/legal_sources_manifest.json

## Legal Sources Manifest

LandCare AI now includes a legal-source manifest located at:

```text
data/legal_sources/legal_sources_manifest.json
```

This manifest tells the app which official legal documents should be added, verified, indexed, and used as legal sources.

### Source folders

```text
data/legal_sources/official/
data/legal_sources/reference/
data/legal_sources/excluded/
```

### Source classification

| Folder | Purpose |
|---|---|
| `official/` | Official legal documents used as primary legal authority |
| `reference/` | Articles, explanations, and secondary materials used only for background reference |
| `excluded/` | Sources that should not be used for legal reasoning, such as videos, SEO articles, or unverified summaries |

### Legal answer rule

LandCare AI should not provide a legal conclusion unless the answer can be traced back to:

- legal document;
- article;
- clause;
- point, if available;
- source excerpt or verified legal basis.

If the legal basis is not available, the app must state:

> Chưa đủ căn cứ để kết luận; cần đối chiếu hồ sơ/văn bản gốc.

## Legal RAG Roadmap

The next technical step is to connect the legal-source manifest with a retrieval layer.

Planned flow:

```text
User question
→ Case classification
→ Legal source manifest
→ Official legal document retrieval
→ Legal Evidence Pack
→ Gemini response constrained by evidence
→ Final answer with legal basis
```

## How to add official legal documents

1. Download the official PDF/DOCX/TXT file from a trusted official source.
2. Place the file in:

```text
data/legal_sources/official/
```

3. Update the corresponding item in:

```text
data/legal_sources/legal_sources_manifest.json
```

Change:

```json
"status": "missing_file"
```

to:

```json
"status": "file_added"
```

4. After indexing, update the status to:

```json
"status": "indexed"
```

5. After checking that article/clause/point retrieval works correctly, update the status to:

```json
"status": "verified"
```

## Safety rules

- Do not upload real citizen records.
- Do not upload internal or confidential documents.
- Do not commit API keys or `.env` files.
- Do not use articles, videos, or summaries as final legal authority.
- Official legal documents always take priority over reference materials.

## Author

**Tôn Thất Minh Cường**  
Independent builder / Personal project
