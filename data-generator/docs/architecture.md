# Fake Data Generator — Architecture

**Project**: Fake Data Generator
**Status**: Proof-of-Concept (POC)
**Version**: 1.0.0
**Document**: Architecture
**Last Updated**: 2026-08-27

---

## 1. Architecture Overview

### Architecture

Modular monolith.

```text
┌─────────────────────┐
│     Streamlit       │
│       Frontend      │
└──────────┬──────────┘
           │ HTTP
           ▼
┌─────────────────────┐
│       FastAPI       │
│       Backend       │
├─────────────────────┤
│ API                 │
│ Services            │
│ Generators          │
│ Validators          │
│ LLM Provider        │
│ Exporters           │
└──────────┬──────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
 Deterministic   LLM
 Generators      Provider
```

### Architectural Priorities

When making implementation decisions, use this priority order:

```text
1. Correctness
2. Data validity
3. Deterministic constraints
4. Security and privacy
5. Testability
6. Maintainability
7. User experience
8. Performance
9. Infrastructure scalability
```

The POC SHALL optimize for learning and validation of the product concept
rather than production-scale throughput.

### Final POC Architecture

```text
                    ┌───────────────┐
                    │   Streamlit   │
                    │      UI       │
                    └───────┬───────┘
                            │
                         REST API
                            │
                    ┌───────▼───────┐
                    │    FastAPI    │
                    └───────┬───────┘
                            │
                 ┌──────────▼──────────┐
                 │  Generation Service │
                 └──────────┬──────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        Deterministic     LLM          Validation
         Generators     Provider        Engine
              │             │             │
              └─────────────┼─────────────┘
                            ▼
                    Post Processing
                            │
                            ▼
                       Statistics
                            │
                            ▼
                         Export
                       ┌────┴────┐
                       ▼         ▼
                      CSV       JSON
```

---

## 2. Data Types

The POC SHALL support the following generators:

| Data Type   | Generator            |
| ----------- | -------------------- |
| Text        | LLM / deterministic  |
| Integer     | NumPy                |
| Float       | NumPy                |
| Boolean     | Random               |
| Date        | Python               |
| DateTime    | Python               |
| UUID        | UUID generator       |
| Email       | Faker/deterministic  |
| Phone       | Faker/deterministic  |
| Categorical | Configured values    |
| JSON        | Structured generator |

The architecture SHALL allow additional generators to be added later.

---

## 3. Generator Architecture

Each data type SHOULD have an isolated generator.

```text
Generator
│
├── TextGenerator
├── IntegerGenerator
├── FloatGenerator
├── BooleanGenerator
├── DateGenerator
├── DateTimeGenerator
├── UUIDGenerator
├── EmailGenerator
├── PhoneGenerator
├── CategoricalGenerator
└── JSONGenerator
```

A common interface SHOULD be used:

```text
generate(config, count) -> values
```

This allows the generation service to remain independent of individual
generator implementations.

---

## 4. LLM Integration

The LLM SHALL only be used where semantic generation is beneficial.

Examples:

```text
product_description
customer_review
company_description
support_ticket
article_summary
```

The LLM provider SHALL be isolated behind an abstraction:

```text
LLMProvider
    │
    ├── OpenAIProvider
    └── MockLLMProvider
```

The POC SHALL support a mock provider for testing.

---

## 5. Prompt Generation

Create a dedicated prompt builder.

```text
PromptBuilder
      │
      ├── Dataset context
      ├── Column definitions
      ├── Constraints
      ├── Domain description
      └── Generation instructions
```

Example input:

```text
Dataset:
Customer Support Tickets

Columns:
ticket_id: UUID
subject: Text
description: Text
priority: Categorical
status: Categorical
```

The prompt builder produces an LLM request appropriate for the schema.

Prompts SHALL be versioned.

---

## 6. Post-Processing Pipeline

After generation:

```text
Generated Dataset
       ↓
Missing Value Processor
       ↓
Duplicate Processor
       ↓
Distribution Processor
       ↓
Constraint Processor
       ↓
Final Dataset
```

Post-processing SHALL be deterministic where possible.

A random seed SHOULD be supported.

---

## 7. Validation Engine

The validator SHALL verify:

```text
Schema
  ↓
Data Types
  ↓
Required Fields
  ↓
Allowed Values
  ↓
Ranges
  ↓
Missing Values
  ↓
Duplicates
  ↓
Distributions
```

Example validation result:

```json
{
  "valid": true,
  "row_count": {
    "requested": 1000,
    "actual": 1000
  },
  "missing_percentage": {
    "requested": 5,
    "actual": 5
  },
  "duplicate_percentage": {
    "requested": 3,
    "actual": 3
  }
}
```

---

## 8. Export Architecture

The POC SHALL support:

```text
CSV
JSON
```

The exporter architecture SHOULD be:

```text
Exporter
│
├── CSVExporter
└── JSONExporter
```

Future:

```text
ParquetExporter
ExcelExporter
SQLExporter
```

---

## 9. Project Structure

Recommended backend structure:

```text
backend/
└── app/
    ├── api/
    │   └── routes/
    │       ├── generation.py
    │       ├── validation.py
    │       ├── schema.py
    │       └── health.py
    │
    ├── core/
    │   ├── config.py
    │   └── logging.py
    │
    ├── models/
    │   ├── dataset.py
    │   ├── column.py
    │   ├── characteristics.py
    │   └── generation.py
    │
    ├── generators/
    │   ├── base.py
    │   ├── text.py
    │   ├── numeric.py
    │   ├── categorical.py
    │   ├── datetime.py
    │   └── identifiers.py
    │
    ├── services/
    │   ├── generation.py
    │   ├── prompt_builder.py
    │   ├── post_processing.py
    │   ├── validation.py
    │   └── statistics.py
    │
    ├── providers/
    │   └── llm/
    │       ├── base.py
    │       ├── openai.py
    │       └── mock.py
    │
    ├── exporters/
    │   ├── base.py
    │   ├── csv.py
    │   └── json.py
    │
    └── main.py
```

Frontend:

```text
frontend/
└── streamlit_app/
    ├── app.py
    ├── pages/
    │   ├── dataset.py
    │   ├── schema.py
    │   ├── characteristics.py
    │   ├── review.py
    │   └── results.py
    └── services/
        └── api_client.py
```

---

## Related Documents

- [Docs index](README.md)
- [Planning](planning.md) — POC implementation plan, phases, sprints, acceptance criteria
- [Product definition](product-definition.md) — scope and requirements
- [Product brief](product-brief.md) — positioning and value proposition
- [Constitution](../.specify/memory/constitution.md) — governing engineering principles
