# LandCare AI

Created by: **Tôn Thất Minh Cường**  
Project type: **Personal non-official prototype**  
Status: **Usable MVP with legal-source manifest and Legal RAG roadmap**

Live demo:

```text
https://landcare-ai-cuong.streamlit.app/
```

GitHub repository:

```text
https://github.com/CuongTob/LandCare-AI
```

---

## 1. Overview

**LandCare AI** is a personal, non-official AI prototype designed to help citizens understand public land procedures, especially matters related to land acquisition, inventory, compensation, support, and resettlement.

The project focuses on transforming complex legal and administrative language into practical guidance, including:

- plain-language explanations;
- legal-basis-aware document checklists;
- suggested questions to ask competent authorities;
- draft request letters for reference;
- legal source tracking through an official-source manifest;
- a future Legal RAG pipeline for article / clause / point retrieval.

---

## 2. Disclaimer

This project is for educational, research, and demonstration purposes only.

LandCare AI:

- does **not** represent any government agency;
- does **not** provide official legal advice;
- does **not** issue administrative decisions;
- does **not** replace professional legal consultation;
- does **not** replace responses from competent authorities.

The project should only use:

- public legal documents;
- synthetic sample cases;
- non-confidential reference materials.

The app must not process real citizen records, personal data, confidential files, or internal government documents.

---

## 3. Problem Statement

Citizens often receive land-related notices or draft documents but may not understand:

- what stage of the procedure they are in;
- what documents they should prepare;
- what legal basis may be relevant;
- what questions they should ask competent authorities;
- how to write a request for clarification, supplementation, or review.

LandCare AI aims to reduce this information gap by helping citizens prepare better before working with competent authorities.

---

## 4. MVP Scope

The current MVP focuses on one practical scenario:

> A citizen receives a land acquisition, inventory, compensation, support, or resettlement-related notice and wants to understand what stage they are in, what documents they should prepare, and what questions they should ask.

The MVP does not attempt to solve all land-law issues.

---

## 5. Key Features

### 5.1 Legal Situation Classifier

The app classifies the user’s situation into groups such as:

- land acquisition notice;
- inventory / measurement / asset verification;
- compensation and support plan;
- resettlement;
- lack of land-origin documents;
- request for review / petition / complaint-related preparation.

### 5.2 Legal-Basis-Aware Checklist

The app generates practical checklists and links each checklist item to a legal basis or source category where available.

Example output:

```text
Document to prepare:
- Land use right certificate, if available

Legal basis to check:
- Land Law 2024
- Decree 88/2024/ND-CP
```

### 5.3 Suggested Questions

The app suggests questions citizens should ask competent authorities, for example:

- Which stage of the procedure am I currently in?
- Which documents are missing?
- What article, clause, or point is being applied?
- What is the deadline for submitting comments or supplementary documents?
- Which authority or unit should receive the request?

### 5.4 Draft Request Letter

The app can generate reference request letters, including:

- request for document guidance;
- request for inventory review;
- request for clarification of compensation/support/resettlement plan;
- request for resettlement guidance.

### 5.5 Legal Sources Manifest

The project includes a legal-source manifest that tells the app which official legal documents should be added, verified, indexed, and used.

Manifest path:

```text
data/legal_sources/legal_sources_manifest.json
```

### 5.6 Legal RAG Roadmap

The next major step is connecting the legal-source manifest with a retrieval layer so the app can automatically create a **Legal Evidence Pack** before generating answers.

---

## 6. Legal Answer Rule

LandCare AI should not provide a legal conclusion unless the answer can be traced back to:

- legal document;
- article;
- clause;
- point, if available;
- source excerpt or verified legal basis.

If the legal basis is not available, the app must state:

> Chưa đủ căn cứ để kết luận; cần đối chiếu hồ sơ/văn bản gốc.

The app must not invent legal citations.

---

## 7. Legal Sources Manifest

LandCare AI now includes a legal-source manifest located at:

```text
data/legal_sources/legal_sources_manifest.json
```

This manifest tells the app:

- which legal documents are required;
- which documents are official sources;
- which documents are only reference materials;
- which documents should be excluded from legal reasoning;
- which file is missing;
- which file has been added;
- which file has been indexed;
- which file has been verified.

---

## 8. Source Folders

```text
data/legal_sources/official/
data/legal_sources/reference/
data/legal_sources/excluded/
```

### Source Classification

| Folder | Purpose |
|---|---|
| `official/` | Official legal documents used as primary legal authority |
| `reference/` | Articles, explanations, and secondary materials used only for background reference |
| `excluded/` | Sources that should not be used for legal reasoning, such as videos, SEO articles, or unverified summaries |

---

## 9. Source Status Values

Each source in the manifest may have one of the following statuses:

| Status | Meaning |
|---|---|
| `missing_file` | The document is listed in the manifest but the actual file has not been added yet |
| `file_added` | The official file has been added to the repository |
| `indexed` | The file has been indexed by the retrieval layer |
| `verified` | Article / clause / point retrieval has been checked |
| `deprecated` | The source is no longer used because it has been replaced or superseded |

---

## 10. Core Legal Sources

The initial legal-source manifest includes the following priority sources:

| Priority | Document | Role |
|---:|---|---|
| 1 | Land Law No. 31/2024/QH15 | Core law for land acquisition, inventory, compensation, support, and resettlement |
| 2 | Law No. 43/2024/QH15 | Checks amendments and effective-date issues related to the Land Law |
| 3 | Decree No. 88/2024/ND-CP | Core decree on compensation, support, and resettlement when the State recovers land |
| 4 | Decree No. 101/2024/ND-CP | Land registration, certificates, land information system, and land-origin document issues |
| 5 | Decree No. 102/2024/ND-CP | Detailed implementation of several articles of the Land Law |
| 6 | Decree No. 151/2025/ND-CP | Competence allocation under the two-level local government model |
| 7 | Decree No. 226/2025/ND-CP | Amendment layer for decrees guiding the Land Law |
| 8 | Decree No. 49/2026/ND-CP | Mechanism for resolving difficulties in implementing the Land Law |
| 20 | Decision No. 222/QD-TTg | Official implementation plan for the Land Law, used as official reference only |

---

## 11. How to Add Official Legal Documents

### Step 1: Download the official file

Download the official PDF, DOCX, or TXT file from a trusted official source.

### Step 2: Place the file in the official folder

```text
data/legal_sources/official/
```

### Step 3: Update the manifest

Open:

```text
data/legal_sources/legal_sources_manifest.json
```

Find the corresponding source item and update:

```json
"status": "missing_file"
```

to:

```json
"status": "file_added"
```

### Step 4: Index the file

After the retrieval layer is connected, index the file.

Then update:

```json
"status": "indexed"
```

### Step 5: Verify retrieval

After checking that the app can retrieve the correct article / clause / point, update:

```json
"status": "verified"
```

---

## 12. Legal RAG Roadmap

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

The retrieval layer should help the app find:

- the relevant legal document;
- article;
- clause;
- point;
- excerpt;
- application note;
- uncertainty or missing facts.

---

## 13. Legal Evidence Pack

Before Gemini generates a final answer, the app should build a **Legal Evidence Pack**.

Suggested structure:

```json
{
  "case_group": "inventory_review",
  "legal_bases": [
    {
      "document": "Land Law 2024",
      "article": "Article 87",
      "clause": "",
      "point": "",
      "excerpt": "Relevant excerpt from the official source",
      "application_note": "Used to identify the inventory step in the land acquisition procedure",
      "confidence": "direct"
    }
  ],
  "missing_facts": [
    "Original notice date",
    "Issuing authority",
    "Whether the citizen signed the inventory record"
  ]
}
```

Gemini should only answer based on this evidence pack.

---

## 14. Planned v4 Architecture

```text
Citizen input
→ Streamlit UI
→ Case classifier
→ Legal source manifest reader
→ Official legal document retriever
→ Legal Evidence Pack builder
→ Gemini constrained response
→ Legal basis checker
→ Final answer
```

---

## 15. Project Structure

```text
LandCare-AI/
├─ README.md
├─ requirements.txt
├─ .env.example
├─ .gitignore
├─ app/
│  ├─ app.py
│  ├─ prompts.py
│  └─ utils.py
├─ data/
│  ├─ legal_sources/
│  │  ├─ legal_sources_manifest.json
│  │  ├─ official/
│  │  │  └─ .gitkeep
│  │  ├─ reference/
│  │  │  └─ .gitkeep
│  │  └─ excluded/
│  │     └─ .gitkeep
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

---

## 16. Quick Start

### 16.1 Install dependencies

```bash
pip install -r requirements.txt
```

### 16.2 Optional: configure API key locally

Copy `.env.example` to `.env` and add your model API key.

```bash
cp .env.example .env
```

The app can run in demo mode without an API key.

### 16.3 Run the app

```bash
streamlit run app/app.py
```

---

## 17. Streamlit Secrets

For deployment on Streamlit Community Cloud, API keys should be stored in Streamlit Secrets, not in GitHub.

Example:

```toml
GEMINI_API_KEY = "your_api_key_here"
GEMINI_MODEL = "gemini-2.5-flash"
```

Do not commit `.env`, API keys, or private credentials to the repository.

---

## 18. Safety Principles

LandCare AI must follow these safety rules:

- Do not upload real citizen records.
- Do not upload internal or confidential documents.
- Do not commit API keys or `.env` files.
- Do not use articles, videos, or summaries as final legal authority.
- Official legal documents always take priority over reference materials.
- Do not provide final legal conclusions without verified legal basis.
- Do not create or invent article / clause / point citations.
- Always show a non-official disclaimer.

---

## 19. Development Roadmap

### v1 - Initial Scaffold

- Basic Streamlit app
- README
- Sample data folders
- Demo outputs

### v2 - Usable MVP

- Case input
- Sample scenarios
- Checklist generation
- Draft letter generation
- Demo UI

### v3 - Legal Citation Matrix

- Legal basis matrix
- Article / clause / point fields
- Legal-basis-aware outputs
- Safer prompt rules

### v4 - Manifest-Connected Legal RAG

Planned next step:

- read `legal_sources_manifest.json`;
- add a `Kho pháp lý` tab;
- show missing / added / indexed / verified sources;
- connect official legal files to a retrieval layer;
- build Legal Evidence Pack before generating final answers.

### v5 - Full Legal Retrieval

Planned future step:

- retrieve source excerpts;
- extract article / clause / point;
- check output grounding;
- export legal guidance reports with verified citations.

---

## 20. Example Use Case

Citizen input:

```text
Tôi đã ký biên bản kiểm đếm nhưng sau đó phát hiện số lượng cây trồng và một số vật kiến trúc có thể chưa được ghi nhận đầy đủ. Tôi muốn đề nghị kiểm tra lại nhưng chưa biết viết văn bản thế nào.
```

Expected app output:

- classify as inventory review / request for re-checking;
- identify possible legal sources;
- generate a document checklist;
- suggest questions to ask the competent authority;
- draft a request letter;
- clearly state that final legal conclusions require official review.

---

## 21. Data Policy

This project should only use:

- official public legal documents;
- synthetic case descriptions;
- public non-confidential reference materials.

This project must not use:

- real citizen records;
- personal data;
- confidential government documents;
- internal administrative records;
- API keys committed to the repository.

---

## 22. Author

**Tôn Thất Minh Cường**  
Independent builder / Personal project

---

## 23. License

No license has been selected yet.

Before reuse, redistribution, or public deployment beyond demonstration purposes, a suitable open-source license should be added.
