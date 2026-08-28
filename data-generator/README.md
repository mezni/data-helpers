# Fake Data Generator

> A proof-of-concept (POC) for generating realistic, configurable, and controlled
> fake datasets using AI/LLM technology combined with deterministic
> data-generation and transformation techniques.

The Fake Data Generator is a **general-purpose synthetic data platform**. Given a
user-defined schema and a set of characteristics, it produces validated fake
datasets across many domains — customer data, product data, transactions,
business data, natural-language text, classification datasets, and more.

The system uses **AI only where semantic generation adds value** (descriptions,
reviews, addresses, domain-specific text) and **deterministic code** for
predictable requirements (numbers, dates, booleans, distributions, missing
values, duplicates, enumerations). Every dataset is **validated before export**,
and every generation is **traceable**.

## Why Fake Data Generator?

- **General-purpose, not just text classification.** Build any dataset from a
  user-defined schema.
- **AI for semantics, code for determinism.** LLMs generate context-rich content;
  deterministic engines handle predictable fields.
- **Always validated.** Configuration, generated-data, and statistical validation
  gate every output before it reaches you.
- **Reproducible.** Deterministic generators accept explicit seeds; generation
  metadata captures configuration, model, prompts, and results.
- **Privacy-safe.** The system generates synthetic, non-identifying data and never
  reproduces real personal information.
- **Extensible.** New data types, providers, and relational datasets can be added
  without rewriting unrelated components.

## Quick Start

The POC runs as a modular monolith using Docker Compose (FastAPI backend +
Streamlit frontend). See `docs/product-brief.md` for the full positioning and
`docs/product-definition.md` for the complete product specification.

## Architecture (High Level)

```text
Streamlit (UI)
    │  REST /api/v1
    ▼
FastAPI (Backend)
    ├── Generators      → deterministic + semantic data creation
    ├── Providers       → LLM provider abstraction (OpenAI, other, Mock)
    ├── PromptBuilder   → versioned prompt construction
    ├── PostProcessor   → transformations
    ├── Validators      → multi-layer validation
    ├── Statistics      → dataset characteristic reporting
    ├── Exporters       → CSV / JSON
    └── Core / Models   → Pydantic schemas & configuration
```

## Repository Layout

```text
app/
├── api/            # REST endpoints (/api/v1)
├── core/           # configuration, settings, logging
├── models/         # Pydantic schemas
├── generators/     # data generation logic
├── services/       # business logic services
├── providers/      # LLM provider abstraction
├── validators/     # validation logic
├── exporters/      # CSV/JSON export
└── main.py         # FastAPI entrypoint
docs/
├── README.md              # docs index
├── product-brief.md
├── product-definition.md
├── architecture.md
└── planning.md
```

## Project Governance

Engineering decisions follow the project **constitution** (see
`.specify/memory/constitution.md`), which defines 27 principles covering
generation philosophy, schema design, validation, reproducibility, provider
abstraction, privacy, modular design, observability, and more. Significant
architectural decisions are recorded as Architecture Decision Records (ADRs).

**Backend**: FastAPI &middot; **Frontend**: Streamlit &middot; **Language**:
Python (`uv`) &middot; **AI**: LLM-based generation where appropriate &middot;
**Status**: POC
