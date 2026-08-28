# Product Definition — Fake Data Generator

**Project**: Fake Data Generator
**Status**: Proof-of-Concept (POC)
**Version**: 1.0.0
**Document**: Product Definition
**Last Updated**: 2026-08-27

---

## 1. Product Overview

Fake Data Generator is a **general-purpose synthetic/fake dataset generation
platform**. It lets users define the structure of a dataset, configure how data
should be generated—including data types, distributions, and imperfections—and
produce validated, exportable fake datasets.

The product combines **AI/LLM semantic generation** with **deterministic
data-generation and transformation techniques** to deliver realistic,
configurable, and controlled datasets. It is deliberately general-purpose: it
is **not** architecturally restricted to text-classification datasets.

### 1.1 Primary Purpose

Generate synthetic/fake datasets based on a user-defined schema and set of
characteristics, with a strong emphasis on:

- **Correctness** — output matches the requested schema and constraints.
- **Configurability** — users control types, distributions, and imperfections.
- **Reproducibility** — deterministic seeds and full generation metadata.
- **Privacy** — synthetic, non-identifying, non-reproducing personal-like data.
- **Data-quality validation** — multi-layer validation gates every dataset.

### 1.2 Target Scenarios

| Scenario | Example |
|----------|---------|
| Customer data | Customers with addresses, demographics, contact info |
| Product data | Catalogs with names, descriptions, prices, categories |
| Transaction data | Orders, payments, line items with consistent keys |
| Business data | Companies, departments, service descriptions |
| Text data | Reviews, support tickets, product descriptions |
| Classification datasets | Labeled text/numeric rows for ML training |
| Testing datasets | Rows with controlled missing values and duplicates |
| Development datasets | Realistic-looking data for local environments |
| AI/ML training datasets | Balanced, distributed rows for model training |

---

## 2. Scope

### 2.1 In Scope (POC)

- General-purpose dataset definition and generation (not limited to text).
- Extensible data-type system supporting: **Text, Integer, Float, Boolean,
  Date, DateTime, UUID, Email, Phone, Categorical, JSON**.
- Configurable characteristics: volume, distribution (Uniform/Normal/Weighted/
  Custom), missing data (0-50%), duplicates, outliers, uniqueness, and
  categorical distribution.
- Validation at three layers: **configuration**, **generated-data**, and
  **statistical** validation, reporting actual results.
- Reproducible generation with explicit random seeds and generation metadata.
- LLM integration behind a **provider abstraction** (with a Mock provider for
  tests), using schema-constrained output and bounded retry.
- Versioned, dynamically constructed prompts (not embedded in route handlers).
- REST JSON API under `/api/v1` (FastAPI, OpenAPI docs):
  `POST /generate`, `POST /suggest-schema`, `POST /validate`,
  `GET /health`.
- Streamlit guided workflow UI: Definition -> Schema -> Characteristics ->
  Review -> Generate -> Validate -> Export.
- CSV and JSON export.
- Reasonable limits: max 10,000 rows; configurable column/retry/duration caps.
- Modular monolith, Docker Compose deployment (FastAPI + Streamlit).
- Environment-based configuration with `.env.example` (no committed secrets).
- Automated tests (pytest) with Ruff linting.

### 2.2 Out of Scope (POC)

- Microservices, Kubernetes, message brokers, distributed workers, complex
  authentication, multi-region infrastructure.
- Background/batch large-scale generation (future: background jobs).
- Parquet / Excel / SQL export (future versions).
- Persistent generation-history storage (future; POC uses memory/local files).

### 2.3 Future / Extensible Direction

- New data types: **Address, Person, Company, Currency, IP address, URL,
  geographic coordinates, structured objects, relationships between entities.**
- Relational (multi-entity, foreign-key-consistent) datasets.
- Additional export formats and storage strategies.
- New LLM providers and deterministic provider guarantees.

---

## 3. User Workflow

```text
Dataset Definition
        ↓
Schema / Columns
        ↓
Characteristics
        ↓
Review
        ↓
Generate
        ↓
Validate
        ↓
Export
```

---

## 4. Functional Requirements (High Level)

- **FR-01** Define a dataset (name, purpose, topics).
- **FR-02** Define columns: name, purpose, data type, required/optional status,
  description, allowed values, min/max, distribution, generation strategy.
- **FR-03** Configure characteristics: volume, distribution, missing data,
  duplicates, outliers, uniqueness, categorical distribution.
- **FR-04** Generate fake data using deterministic engines and/or LLM providers.
- **FR-05** Validate generated data (configuration, generated-data, statistical).
- **FR-06** Report actual dataset statistics vs. requested characteristics.
- **FR-07** Preview results.
- **FR-08** Export as CSV and/or JSON.
- **FR-09** Expose REST API under `/api/v1` with OpenAPI documentation.
- **FR-10** Support reproducible generation via explicit seeds and metadata.
- **FR-11** Enforce resource limits (rows, columns, retries, duration).

---

## 5. Non-Functional Requirements

| Category | Requirement |
|----------|-------------|
| Correctness | Generated data passes all validation layers before export |
| Reproducibility | Deterministic generators honor explicit seeds |
| Privacy | No reproduction of real personal information or credentials |
| Security | Secrets only via environment; never logged or committed |
| Extensibility | New data types/providers added without touching unrelated components |
| Modularity | Clear component boundaries; business logic not in route handlers |
| Observability | Lifecycle logging; secrets never logged |
| Performance | Enforced generation limits (10k rows max) |
| Quality | Ruff checks and pytest tests pass before DoD |
| Traceability | Every generation has a unique ID and retained metadata |

---

## 6. Stakeholders

- **End users**: Developers, QA engineers, data scientists, and ML engineers
  who need realistic fake data quickly and controllably.
- **Maintainers**: Engineering team responsible for backend (FastAPI) and
  frontend (Streamlit) development, governed by the project constitution.

---

## 7. Success Criteria (POC)

1. Users can define a schema and configure characteristics via the Streamlit UI.
2. Datasets generate within enforced limits and pass validation.
3. Deterministic datasets are reproducible given the same seed and config.
4. LLM-generated content is validated before entering the dataset with bounded
   retry.
5. Datasets export as CSV and JSON without leaking internal metadata.
6. Backend business logic is exposed through the `/api/v1` API with OpenAPI docs.
7. No secrets are committed; `.env.example` documents required variables.
8. Ruff checks and automated tests pass.

---

## Related Documents

- [Docs index](README.md)
- [Product brief](product-brief.md) — positioning and value proposition
- [Architecture](architecture.md) — technical architecture
- [Planning](planning.md) — POC implementation plan
- [Constitution](../.specify/memory/constitution.md) — governing engineering principles
