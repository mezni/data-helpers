# Fake Data Generator — POC Implementation Plan

**Project**: Fake Data Generator
**Status**: Proof-of-Concept (POC)
**Version**: 1.0.0
**Document**: Implementation Plan (Planning)
**Last Updated**: 2026-08-27

> **Companion doc**: See `docs/architecture.md` for the system architecture,
> data types, generator/prompt/LLM design, post-processing, validation engine,
> export architecture, and project structure.

---

## 1. Planning Overview

### Project

Fake Data Generator

### Objective

Build a proof-of-concept application that allows users to visually define a
dataset schema, configure data-generation characteristics, generate fake data
using deterministic generators and LLMs where appropriate, validate the result,
and export the generated dataset.

### Primary Technologies

- Python
- FastAPI
- Streamlit
- Pydantic
- Pandas
- NumPy
- Faker
- LLM provider
- Pytest
- Ruff
- uv
- Docker
- Docker Compose

### Architecture

Modular monolith. See `docs/architecture.md`.

---

## 2. POC Goals

The POC SHALL demonstrate the complete workflow:

```text
Define Dataset
      ↓
Define Schema
      ↓
Configure Characteristics
      ↓
Generate Data
      ↓
Validate Data
      ↓
Preview Data
      ↓
Export Data
```

The POC should demonstrate that:

- Users can create a dataset without writing code.
- Users can define custom columns.
- Different data types can be generated.
- Data distributions can be configured.
- Missing values and duplicates can be introduced.
- LLMs can generate semantic fields.
- Generated data is validated.
- Users can download the resulting dataset.

---

## 3. POC Scope

### 3.1 Dataset Definition

The user SHALL be able to specify:

- Dataset name
- Dataset description
- Dataset purpose
- Number of rows

Example:

```text
Dataset:
Customer Orders

Purpose:
Testing an order management application

Rows:
1000
```

---

### 3.2 Schema Definition

The user SHALL be able to add, edit, and remove columns.

Each column SHALL support:

```text
Name
Purpose
Data type
Description
Required
```

Example:

```text
customer_id
Type: UUID
Purpose: Identifier

customer_name
Type: Text
Purpose: Personal information

age
Type: Integer
Purpose: Demographic

country
Type: Categorical
Purpose: Geographic

order_amount
Type: Float
Purpose: Transaction
```

---

## 4. Characteristics Configuration

The POC SHALL support the following configuration.

### Missing Values

```text
enabled: true
percentage: 5
```

### Duplicates

```text
enabled: true
percentage: 3
```

### Label / Category Distribution

Example:

```text
priority

low       60%
medium    30%
high      10%
```

### Numerical Distribution

The POC SHOULD support:

```text
Uniform
Normal
Weighted
Custom
```

Example:

```text
age
min: 18
max: 90
distribution: normal
```

---

## 5. API Plan

Base URL:

```text
/api/v1
```

### Health

```http
GET /api/v1/health
```

### Generate

```http
POST /api/v1/generate
```

### Schema Suggestions

```http
POST /api/v1/suggest-schema
```

### Validate

```http
POST /api/v1/validate
```

### Future

```text
GET  /api/v1/generations
GET  /api/v1/generations/{id}
POST /api/v1/generations/{id}/regenerate
```

These future endpoints SHALL NOT be required for the first POC.

---

## 6. Streamlit UI Plan

The UI SHALL use a multi-step workflow.

### Step 1 — Dataset

```text
Dataset Name
Dataset Description
Purpose
Number of Rows
```

### Step 2 — Schema

Display an editable table:

```text
┌──────────────┬─────────────┬────────────┐
│ Name         │ Type        │ Purpose    │
├──────────────┼─────────────┼────────────┤
│ customer_id  │ UUID        │ Identifier │
│ name         │ Text        │ Attribute  │
│ age          │ Integer     │ Attribute  │
└──────────────┴─────────────┴────────────┘
```

Actions:

```text
Add Column
Edit
Delete
Suggest Schema
```

### Step 3 — Characteristics

Controls SHALL depend on the selected data types.

For example:

```text
Integer
├── Min
├── Max
└── Distribution

Categorical
├── Values
└── Distribution

Text
├── Generation strategy
├── Style
└── Domain context
```

### Step 4 — Review

Display:

- Dataset configuration
- Schema
- Characteristics
- Estimated generation cost if available

### Step 5 — Generate

Show generation progress.

### Step 6 — Validate

Display validation results (row count, missing/duplicate percentages, category
and numerical distribution checks) comparing requested vs. actual
characteristics.

### Step 7 — Results / Export

Display:

- First 50 rows (preview)
- Dataset statistics
- Validation results summary
- Download buttons (CSV / JSON)

---

## 7. Development Phases

### Phase 0 — Project Bootstrap

Tasks:

- Initialize repository
- Initialize `uv`
- Configure Python
- Configure Ruff
- Configure Pytest
- Create `.env.example`
- Create README
- Create Docker configuration

Deliverable:

```text
Empty application that starts successfully.
```

---

### Phase 1 — Domain Model

Implement:

- Dataset model
- Column model
- Data type model
- Characteristics model
- Generation request
- Generation response
- Validation response

Deliverable:

```text
Valid configuration can be represented entirely with Pydantic.
```

---

### Phase 2 — Deterministic Generators

Implement:

- Integer
- Float
- Boolean
- Date
- DateTime
- UUID
- Email
- Phone
- Categorical

Deliverable:

```text
Application can generate a dataset without an LLM.
```

This phase is important because it establishes the core data-generation engine.

---

### Phase 3 — LLM Generator

Implement:

- LLM provider interface
- OpenAI provider
- Mock provider
- Prompt builder
- Structured output
- Retry logic

Deliverable:

```text
Application can generate semantic fields using an LLM.
```

---

### Phase 4 — Post-Processing

Implement:

- Missing values
- Duplicates
- Category distributions
- Numerical distributions
- Random seed

Deliverable:

```text
Generated datasets follow configured characteristics.
```

---

### Phase 5 — Validation

Implement:

- Schema validation
- Data-type validation
- Constraint validation
- Statistical validation
- Validation report

Deliverable:

```text
Every generated dataset receives a validation result.
```

---

### Phase 6 — FastAPI

Implement:

```text
GET  /api/v1/health
POST /api/v1/generate
POST /api/v1/validate
POST /api/v1/suggest-schema
```

Deliverable:

```text
Complete backend API.
```

---

### Phase 7 — Streamlit

Implement:

```text
Dataset
Schema
Characteristics
Review
Generate
Results
```

Deliverable:

```text
Complete end-to-end UI.
```

---

### Phase 8 — Export

Implement:

```text
CSV
JSON
```

Deliverable:

```text
Users can download generated datasets.
```

---

### Phase 9 — Traceability

Implement generation metadata:

```text
generation_id
timestamp
configuration
schema
prompt
prompt_version
model
parameters
seed
statistics
validation
```

Deliverable:

```text
Every generation is traceable.
```

---

### Phase 10 — Testing & Hardening

Implement:

- Unit tests
- API tests
- Generator tests
- Validation tests
- Post-processing tests
- Mock LLM tests
- End-to-end test

Also verify:

```text
Ruff
Pytest
Docker build
Docker Compose
```

Deliverable:

```text
Demonstrable POC ready for review.
```

---

## 8. Sprint Plan

### Sprint 1 — Foundation

**Goal**: Create the project foundation.

Tasks:

- Repository structure
- `uv` setup
- FastAPI skeleton
- Streamlit skeleton
- Pydantic
- Ruff
- Pytest
- Docker Compose
- Configuration management

---

### Sprint 2 — Dataset Schema

**Goal**: Create the dataset-definition system.

Tasks:

- Dataset model
- Column model
- Data type enumeration
- Column validation
- Characteristics model
- Schema API
- Streamlit schema UI

---

### Sprint 3 — Data Generation Engine

**Goal**: Generate fake data without AI.

Tasks:

- Generator interface
- Numeric generators
- Date generators
- Identifier generators
- Categorical generator
- Basic text generator
- Generator registry

---

### Sprint 4 — AI Generation

**Goal**: Add LLM-powered semantic generation.

Tasks:

- LLM abstraction
- Provider implementation
- Mock provider
- Prompt builder
- Structured output
- Retry handling
- LLM configuration

---

### Sprint 5 — Data Characteristics

**Goal**: Apply configurable imperfections and distributions.

Tasks:

- Missing values
- Duplicates
- Numerical distributions
- Categorical distributions
- Random seed
- Post-processing pipeline

---

### Sprint 6 — Validation & Statistics

**Goal**: Verify generated datasets.

Tasks:

- Schema validator
- Constraint validator
- Statistical validator
- Dataset statistics
- Validation report

---

### Sprint 7 — Complete UI

**Goal**: Connect the complete Streamlit workflow.

Tasks:

- Dataset page
- Schema page
- Characteristics page
- Review page
- Generation progress
- Results page
- Dataset preview

---

### Sprint 8 — Export & POC Release

**Goal**: Make the application demonstrable.

Tasks:

- CSV export
- JSON export
- Generation metadata
- Error handling
- Logging
- End-to-end tests
- Docker Compose
- README
- Demo dataset scenarios

---

## 9. POC Acceptance Criteria

The POC SHALL be considered successful when a user can perform the following
workflow without writing code:

```text
1. Open Streamlit

2. Create:
   Customer Dataset

3. Define:
   1,000 rows

4. Add columns:
   customer_id → UUID
   name        → Text
   age         → Integer
   country     → Categorical
   email       → Email

5. Configure:
   age range 18-90
   country distribution
   5% missing values
   3% duplicates

6. Generate

7. View:
   first 50 rows

8. View:
   actual statistics

9. Validate:
   dataset passes validation

10. Download:
    CSV or JSON
```

---

## 10. Future Roadmap

The following features are explicitly outside the initial POC:

### Dataset Relationships

```text
Customer
   ↓
Orders
   ↓
Order Items
```

### Dataset Templates

```text
E-commerce
CRM
Banking
Healthcare
IoT
```

### Database Export

```text
PostgreSQL
MySQL
MongoDB
```

### Advanced Generation

```text
Correlated columns
Foreign keys
Conditional fields
Custom constraints
Business rules
```

### AI Features

```text
AI schema suggestion
AI constraint suggestion
AI data-quality scoring
AI dataset explanation
AI anomaly generation
```

### Persistence

```text
Generation history
Dataset versions
Saved schemas
User projects
```

---

## POC Definition

The first release is successful when the application demonstrates:

> **A user can define a dataset schema, configure how its data should look,
> generate realistic fake data using the appropriate combination of
> deterministic generators and AI, validate the result, inspect statistics, and
> export the dataset.**

This is the boundary of the first POC. Everything else should be treated as a
future extension.

---

## Related Documents

- [Docs index](README.md)
- [Architecture](architecture.md) — system architecture, data types, generators,
  LLM integration, project structure
- [Product definition](product-definition.md) — scope and requirements
- [Product brief](product-brief.md) — positioning and value proposition
- [Constitution](../.specify/memory/constitution.md) — governing engineering principles
