<!--
SYNC IMPACT REPORT (vN/A → v1.0.0) — INITIAL RATIFICATION
=====================================================
- Version change: (template, no prior version) → 1.0.0
- Modified principles: n/a (initial ratification)
- Added sections: Preamble; Core Principles (Principles 1-27); Non-Negotiable Rules;
  Governance (versioning policy, amendment procedure, compliance review)
- Removed sections: n/a
- Templates requiring updates:
  ✅ plan-template.md — Constitution Check gate aligned (principles-driven gates)
  ✅ spec-template.md — retains mandatory scope/requirements sections; no change required
  ✅ tasks-template.md — no change required (task types generic, apply per-feature)
- Follow-up TODOs:
  - TODO(RATIFICATION_DATE): Confirmed 2026-08-27 (initial adoption, date of this update).
-->

# Fake Data Generator Constitution

This constitution defines the fundamental principles, architectural constraints,
development standards, and quality requirements for the Fake Data Generator
application.

The application is a proof-of-concept (POC) for generating realistic,
configurable, and controlled fake datasets using AI/LLM technology combined with
deterministic data-generation and transformation techniques.

The system is intended to support multiple data-generation scenarios, including
but not limited to: customer data, product data, transaction data, business
data, text data, classification datasets, testing datasets, development
datasets, and AI/ML training datasets.

The system SHALL prioritize correctness, configurability, reproducibility,
privacy, and data-quality validation.

## Core Principles

### I. General-Purpose Fake Data Generation (NON-NEGOTIABLE)

The system SHALL generate synthetic/fake datasets based on a user-defined schema
and set of characteristics. The core workflow SHALL allow users to define a
dataset; define columns/fields; configure data types, generation rules,
distributions, and imperfections; generate fake data; validate; preview; and
export the dataset. The system SHALL NOT be architecturally restricted to
text-classification datasets.

### II. AI for Semantics, Code for Determinism

The system SHALL use AI/LLMs primarily for tasks requiring semantic or
contextual generation (e.g., natural-language text, descriptions, reviews,
addresses, business descriptions, context-aware relationships, domain-specific
content). Deterministic application code SHALL be preferred for predictable
data-generation requirements (e.g., numbers, dates, booleans, UUIDs,
percentages, distributions, missing values, duplicate records, numeric ranges,
enumerations). The system SHALL NOT unnecessarily use an LLM when deterministic
generation can satisfy the requirement.

### III. User-Defined Schema

Users SHALL be able to define the structure of the generated dataset. Each
column SHALL support, where applicable: name, purpose, data type,
required/optional status, description, allowed values, minimum value, maximum
value, distribution, and generation strategy.

### IV. Extensible Data-Type System

The application SHALL use an extensible data-type architecture. The initial POC
SHOULD support Text, Integer, Float, Boolean, Date, DateTime, UUID, Email,
Phone, Categorical, and JSON. Future versions MAY introduce Address, Person,
Company, Currency, IP address, URL, geographic coordinates, structured objects,
and relationships between entities. Adding a new data type SHOULD NOT require
modification of unrelated generation components.

### V. Configurable Data Characteristics

Users SHALL be able to control characteristics of generated datasets, including
volume (number of rows); distribution (Uniform, Normal, Weighted, Custom);
missing data (0%-50%); duplicates (exact and near duplicates); outliers
(numerical and unusual values); uniqueness (unique, mostly unique, repeated);
and categorical distribution (e.g., Category A -> 70%, B -> 20%, C -> 10%). The
system SHALL distinguish between requested characteristics and the actual
characteristics of the generated dataset.

### VI. Relational Data Generation

The architecture SHOULD support relationships between columns and entities.
Foreign-key-like relationships SHALL remain consistent when relational
generation is enabled. The POC MAY initially support a single flat dataset while
keeping the architecture extensible toward relational datasets.

### VII. Multi-Layer Validation

Generated data SHALL be validated before being presented as a completed
dataset. Validation SHALL occur at multiple levels: configuration validation
(column names, column uniqueness, data types, required fields, numeric ranges,
percentages, category definitions, row count); generated-data validation
(schema, data types, allowed values, nullability, constraints, relationships);
and statistical validation (row count, missing-value percentage, duplicate
percentage, category distribution, numerical distribution, uniqueness). The
system SHALL report actual results.

### VIII. Reproducible Generation

The system SHOULD support reproducible dataset generation. Generation metadata
SHOULD include generation ID, configuration, random seed, generator version,
model, model parameters, prompt version, and timestamp. Deterministic
generators SHALL support explicit random seeds. LLM-generated content SHALL be
considered probabilistic unless the selected provider guarantees deterministic
behavior.

### IX. Provider Abstraction (NON-NEGOTIABLE)

LLM integration SHALL be isolated behind a provider abstraction (e.g.,
LLMProvider with OpenAI, other providers, and a Mock provider). The core
data-generation workflow SHALL NOT depend directly on a specific LLM SDK, so
providers can be changed without rewriting the application architecture.

### X. Schema-Constrained AI Generation

When an LLM is used to generate structured data, the application SHOULD use
structured output/schema enforcement whenever supported by the provider. LLM
output SHALL be validated before entering the main dataset. Invalid output SHALL
NOT silently enter the final dataset. The system MAY retry generation when
validation fails, subject to a bounded retry policy.

### XI. Dynamic Prompt Construction

Prompts SHALL be constructed from structured dataset configuration and SHALL NOT
be embedded directly inside API route handlers. The prompt system SHOULD
consider dataset purpose, column definitions, data types, relationships,
allowed values, domain context, desired characteristics, and generation
quantity. Prompts SHALL be versioned.

### XII. Privacy and Safety (NON-NEGOTIABLE)

The system SHALL generate fake data and SHALL NOT intentionally reproduce real
individuals' personal information. Generated personal-like information SHOULD be
synthetic and non-identifying. The system SHALL NOT require users to provide
real personal information in order to generate datasets. Secrets and
credentials SHALL NEVER be included in generated datasets unless explicitly
required for a controlled test case, and even then SHALL be clearly fake.

### XIII. Input Validation

All user-provided configuration SHALL be validated, including dataset names,
topics, column names, descriptions, category values, and generation
instructions. The system SHALL protect prompt construction from unintended
instruction injection. User-provided text SHALL NOT override system-level
generation rules.

### XIV. Generation Traceability (NON-NEGOTIABLE)

Every generation SHALL receive a unique identifier. The system SHOULD retain
generation ID, configuration, schema, prompt, prompt version, LLM model,
generation parameters, random seed, validation results, and dataset statistics.
For the POC, this information MAY be stored in memory or local files. Persistent
storage MAY be introduced later.

### XV. REST API

The backend SHALL expose a RESTful JSON API using FastAPI. The API SHALL use
versioning under `/api/v1`. Initial endpoints SHOULD include
`POST /api/v1/generate`, `POST /api/v1/suggest-schema`, `POST /api/v1/validate`,
and `GET /api/v1/health`. FastAPI SHALL provide OpenAPI documentation.

### XVI. Streamlit User Experience

Streamlit SHALL provide the primary POC user interface using a guided workflow:
Dataset Definition -> Schema/Columns -> Characteristics -> Review -> Generate ->
Validate -> Export. The frontend SHALL communicate with the backend through the
API. Core generation logic SHALL remain in the backend.

### XVII. Standard Data Formats

The POC SHALL support exporting generated datasets as CSV and JSON. Future
versions MAY support Parquet, Excel, and SQL. Exported datasets SHALL contain
the generated data and SHALL NOT expose internal application metadata unless
explicitly requested.

### XVIII. Automated Testing

Critical generation logic SHALL be covered by automated tests, including schema
validation, data-type validation, constraint validation, distribution
calculations, missing-value generation, duplicate generation, deterministic
generation, LLM output validation, API endpoints, and export functionality.
LLM-dependent tests SHOULD use mock providers whenever possible.

### XIX. Modern Python Development

The project SHALL use modern Python development practices. Preferred tooling
includes Python, `uv`, FastAPI, Pydantic, Pandas, NumPy, Pytest, and Ruff. The
project SHALL use type hints for application code. Business logic SHALL NOT be
concentrated inside API route functions.

### XX. Modular Design

The backend SHALL follow a modular structure (e.g., `app/api`, `app/core`,
`app/models`, `app/generators`, `app/services`, `app/providers`,
`app/validators`, `app/exporters`, `app/main.py`). Responsibilities SHALL be
separated between Generator, LLMProvider, PromptBuilder, PostProcessor,
Validator, Statistics, and Exporter.

### XXI. Observability

The application SHALL provide sufficient logging to understand the generation
lifecycle, including generation started, configuration validated, generation
strategy selected, LLM request started/completed, post-processing completed,
validation completed, generation completed, and generation failed. API keys,
credentials, and other secrets SHALL never be logged.

### XXII. Controlled Resource Usage

The POC SHALL enforce reasonable generation limits: maximum dataset size of
10,000 rows; maximum column count configurable; maximum retry count
configurable; and maximum generation duration configurable. Large-scale
generation SHALL be addressed in a future version using background jobs or batch
processing.

### XXIII. Simplicity First

The initial implementation SHALL remain intentionally simple. The POC SHALL NOT
require microservices, Kubernetes, message brokers, distributed workers,
complex authentication, or multi-region infrastructure. The initial deployment
SHALL use Docker Compose (FastAPI and Streamlit). The architecture SHALL remain
extensible without introducing unnecessary infrastructure.

### XXIV. Environment-Based Configuration (NON-NEGOTIABLE)

Secrets SHALL be provided through environment variables (e.g.,
`OPENAI_API_KEY`, `LLM_MODEL`, `API_HOST`, `API_PORT`). Real credentials SHALL
never be committed to source control. A `.env.example` file SHALL document
required variables.

### XXV. Definition of Done

A feature SHALL be considered complete when: requirements are implemented;
appropriate Pydantic models exist; input validation is implemented; business
logic is tested; API behavior is documented; errors are handled appropriately;
generated data passes validation; required UI behavior is functional; export
functionality works where applicable; no secrets are committed; Ruff checks
pass; and tests pass.

### XXVI. Architecture Decision Records

Significant architectural decisions SHALL be documented through ADRs (e.g., LLM
provider selection, data-generation strategy, schema representation, storage
strategy, relational data strategy, validation strategy, export formats,
background processing, deployment architecture). ADRs SHALL explain context,
decision, alternatives, and consequences.

## Non-Negotiable Rules

The following rules are mandatory:

1. The application is a general-purpose fake data generator.
2. Text classification is only one possible use case.
3. FastAPI owns backend business logic.
4. Streamlit owns presentation and user interaction.
5. Pydantic defines application schemas.
6. Deterministic code handles deterministic requirements.
7. LLMs are used where semantic generation provides value.
8. Generated data is always validated before export.
9. Generation must be traceable.
10. Secrets must never be stored in source code.
11. LLM providers must be abstracted from core business logic.
12. The POC remains a modular monolith.
13. The architecture must remain extensible toward multiple data types and
    relational datasets.
14. The system must generate fake data rather than reproduce real personal
    information.

## Governance

**Constitution Supremacy**: This constitution defines the project's fundamental
engineering principles. Implementation decisions SHALL comply with these
principles unless the constitution is explicitly amended.

**Versioning Policy**: The constitution version SHALL follow semantic versioning
(MAJOR.MINOR.PATCH). MAJOR: backward-incompatible governance/principle removals
or redefinitions. MINOR: a new principle/section added or materially expanded
guidance. PATCH: clarifications, wording, and typo fixes.

**Amendment Procedure**: Changes to this constitution SHALL (1) identify the
affected principle, (2) explain the reason for the change, (3) evaluate
architectural consequences, (4) update affected ADRs, and (5) update
specifications and implementation plans where required.

**Compliance Review**: All plans and reviews SHALL verify compliance with this
constitution via the Constitution Check gate. Complexity SHALL be justified
where it conflicts with simplicity principles. CI quality gates (Ruff, tests)
SHALL pass before a feature is considered complete.

**Version**: 1.0.0 | **Ratified**: 2026-08-27 | **Last Amended**: 2026-08-27
