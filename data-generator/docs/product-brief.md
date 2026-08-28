# Product Brief — Fake Data Generator

**Project**: Fake Data Generator
**Status**: Proof-of-Concept (POC)
**Version**: 1.0.0
**Document**: Product Brief
**Last Updated**: 2026-08-27

---

## Executive Summary

Fake Data Generator is a **general-purpose synthetic data platform** that turns a
user-defined schema and configuration into realistic, validated fake datasets. It
deliberately pairs **AI/LLM semantic generation** with **deterministic code** so
that predictable fields are generated reliably while context-rich content
descriptions, reviews, addresses, and domain text are generated naturally.

The product is a **modular monolith**: a FastAPI backend owns all business logic
and generation, a Streamlit frontend guides users through a 7-step workflow, and
everything is driven by a documented constitution of engineering principles.

## Problem Statement

Developers, testers, and ML engineers frequently need realistic data but cannot
use production data due to privacy, availability, or compliance constraints.
Existing tools are often rigid, limited to specific domains, opaque about how
data was generated, or not reproducible. Fake Data Generator solves this with a
**general-purpose**, **configurable**, **validated**, and **reproducible** fake
data pipeline.

## Value Proposition

- **General-purpose, not single-use.** Define any dataset schema — customer,
  product, transaction, business, text, classification, testing, development, or
  AI/ML training.
- **AI where it matters, code where it counts.** LLMs handle semantics;
  deterministic engines handle numbers, dates, distributions, and imperfections —
  saving cost and guaranteeing predictable fields.
- **Validated before export.** Three layers of validation (configuration, data,
  statistics) report the actual characteristics of the generated dataset.
- **Reproducible and traceable.** Explicit seeds plus full generation metadata
  (config, model, prompt, results) make every dataset auditable.
- **Privacy-safe by design.** Generates synthetic, non-identifying data; never
  reproduces real personal information.
- **Extensible architecture.** New data types, LLM providers, and relational
  datasets slot in without rewriting unrelated components.

## Target Audience

Primary users are **technical practitioners** who need trusted fake data:

- **Software developers** needing development/test fixtures.
- **QA engineers** building controlled test datasets with imperfections.
- **Data scientists / ML engineers** creating balanced training and eval sets.
- **Anyone** who needs realistic-looking but fully synthetic data quickly.

## Key Features (POC)

- User-defined datasets and columns with rich configuration (types, ranges,
  allowed values, distributions, strategies).
- Extensible data types: Text, Integer, Float, Boolean, Date, DateTime, UUID,
  Email, Phone, Categorical, JSON.
- Configurable characteristics: volume, distribution, missing data, duplicates,
  outliers, uniqueness, categorical distributions.
- Multi-layer validation and actual-statistics reporting.
- LLM provider abstraction (OpenAI / other / Mock) with schema-constrained
  output and bounded retry.
- Versioned, dynamic prompt construction.
- REST API under `/api/v1` (FastAPI + OpenAPI).
- Streamlit guided workflow and CSV/JSON export.
- Reproducible generation with environment-based secrets, resource limits, and a
  modular monolith deployment via Docker Compose.

## User Workflow

```text
Dataset Definition -> Schema / Columns -> Characteristics -> Review
      -> Generate -> Validate -> Export
```

## API Surface (v1)

| Method | Endpoint                  | Purpose                         |
|--------|---------------------------|---------------------------------|
| POST   | `/api/v1/generate`        | Generate a dataset              |
| POST   | `/api/v1/suggest-schema`  | Suggest a schema from a prompt  |
| POST   | `/api/v1/validate`        | Validate a dataset/configuration|
| GET    | `/api/v1/health`          | Health check                    |

## Architecture Principles

- **AI for semantics, code for determinism.**
- **Provider abstraction** isolates LLM SDKs from core logic.
- **Business logic lives in the backend**, never in route or UI code.
- **Pydantic** defines all schemas; **Pandas/NumPy** power deterministic
  generation and statistics.
- **Secrets never** in source code or logs.
- **Generated data always validated** before export.
- **POC stays a modular monolith** with Docker Compose (FastAPI + Streamlit).

## Constraints & Guardrails (POC)

- Maximum dataset size: **10,000 rows** (configurable columns/retries/duration).
- No microservices, Kubernetes, brokers, or distributed workers.
- Commit-as-you-go discipline; no secrets committed; `.env.example` documents
  required variables.

## Roadmap Direction (Post-POC)

- New data types (Address, Person, Company, Currency, IP, URL, coordinates,
  structured objects) and **relational datasets** with consistent keys.
- Additional export formats (Parquet, Excel, SQL).
- Background/batch generation for large-scale datasets.
- Persistent generation-history storage.
- Additional LLM providers and deterministic-generation guarantees.

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| LLM output invalid or inconsistent | Schema-constrained output + validation + bounded retry; deterministic fallback |
| LLM cost/skew for deterministic fields | Code-first determinism; LLM used only for semantic needs |
| Accidental reproduction of real PII | Privacy principle; synthetic, non-identifying generation; no credential emission |
| Scope creep (relational, infra) | POC keeps flat, single-dataset scope; extensible architecture |

## Success Metrics (POC)

- Datasets generate within limits and pass all validation layers.
- Deterministic datasets reproduce from seed + config.
- Datasets export as CSV/JSON without leaking internal metadata.
- Backend logic exposed via `/api/v1` with OpenAPI docs.
- No secrets committed; Ruff and tests pass per Definition of Done.

## Governance

Engineering decisions follow the project **constitution**
(`.specify/memory/constitution.md`) — 27 principles spanning generation
philosophy, schema, validation, reproducibility, providers, privacy,
modularity, observability, and more — with significant decisions recorded as
ADRs.

**Backend**: FastAPI &middot; **Frontend**: Streamlit &middot; **Language**:
Python (`uv`) &middot; **AI**: LLM-based generation where appropriate &middot;
**Status**: POC

---

## Related Documents

- [Docs index](README.md)
- [Product definition](product-definition.md) — complete specification and scope
- [Architecture](architecture.md) — technical architecture
- [Planning](planning.md) — POC implementation plan
- [Constitution](../.specify/memory/constitution.md) — governing engineering principles
