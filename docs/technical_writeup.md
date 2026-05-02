# Technical Write-up: LandCare AI

## 1. Overview

LandCare AI is a personal, non-official prototype that helps citizens understand public land-related administrative procedures through AI-generated plain-language explanations, document checklists, and draft request letters.

## 2. Why Gemma 4

Gemma 4 is suitable for this prototype because the project needs:

- multilingual Vietnamese support;
- structured outputs;
- instruction following;
- agentic workflow design;
- code/prototype assistance.

## 3. Architecture

```text
User input
   ↓
Streamlit UI
   ↓
Prompt builder
   ↓
Public/synthetic context
   ↓
Gemma-compatible model call
   ↓
Structured Vietnamese response
   ↓
Checklist / explanation / draft letter
```

## 4. Components

### 4.1 Streamlit UI

Provides a simple interface for three MVP functions:

- Explain Notice
- Document Checklist
- Draft Letter

### 4.2 Prompt Builder

Creates a controlled prompt with:

- role instruction;
- safety rules;
- task type;
- public/synthetic context;
- fixed response format.

### 4.3 Safety Layer

The prototype avoids:

- real personal data;
- internal documents;
- official legal advice;
- invented legal citations;
- administrative decision-making.

### 4.4 Offline Demo Mode

If no API key is available, the app falls back to a deterministic demo response so the prototype can still be reviewed.

## 5. Limitations

- It is not a legal advice system.
- It is not connected to any official case management platform.
- It does not verify real citizen eligibility.
- Legal citations must be curated and checked manually before public use.

## 6. Future Work

- Add RAG over verified public legal documents.
- Add document upload and OCR pipeline.
- Add citation checking.
- Add bilingual output.
- Add dashboard for common citizen questions.
