# Fake Data Generator — Documentation

Central index for the Fake Data Generator project documentation.

All documents describe the same **Proof-of-Concept (POC)** system: a modular
monolith (FastAPI backend + Streamlit frontend) that generates general-purpose,
validated, reproducible fake datasets using deterministic generators and LLMs
where appropriate. Engineering decisions comply with the project constitution
(`.specify/memory/constitution.md`, 27 principles).

## Document Set

| Document | Purpose |
|----------|---------|
| [`product-brief.md`](product-brief.md) | Concise positioning: problem, value proposition, audience, features, roadmap |
| [`product-definition.md`](product-definition.md) | Complete product specification: scope, requirements, non-functional requirements, success criteria |
| [`architecture.md`](architecture.md) | System architecture: components, data types, generators, LLM integration, validation, project structure |
| [`planning.md`](planning.md) | POC implementation plan: goals, scope, characteristics, API, UI, development phases, sprints, acceptance criteria |

## How the Documents Relate

```text
product-brief.md      → why we build it (positioning)
product-definition.md → what we build (specification/scope)
architecture.md       → how it is designed (technical architecture)
planning.md           → how it gets built (phases, sprints, acceptance)
```

The **constitution** (`.specify/memory/constitution.md`) is the governing source
of truth. These documents describe how the POC satisfies it. If a document
conflicts with the constitution, the constitution governs.
