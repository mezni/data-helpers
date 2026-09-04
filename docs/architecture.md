# omni-connect Architecture

## 1. Overview

omni-connect is an AI-Powered Telecom Retail Transformation platform. It unifies customer, product, promotion, and operational data into a single intelligent experience for both retail representatives and customers. By embedding AI into every stage of the retail journey, the platform reduces operational complexity, improves decision-making, and delivers personalized customer engagement at scale.

This document describes the target architecture and how the current codebase maps to it across each delivery phase.

## 2. Architectural Goals & Principles

| Principle | Description |
|---|---|
| **Unified experience** | One interface for representatives (end to multi-app context switching, 5–10 apps today) |
| **Real-time intelligence** | Customer 360, recommendations, and next-best-action computed at the point of interaction |
| **Omnichannel** | Same intelligence surfaced across web, mobile, kiosk, and in-store |
| **Phased delivery** | Foundation → Representative Copilot → Customer AI Assistant → Intelligent Automation |
| **AI-assisted, human-in-the-loop** | AI recommends and guides; representative/customer stays in control until full automation in Phase 4+ |
| **Governance-first** | Security, privacy, and data governance established in Phase 1 |
| **Extensible** | New tools, services, and specialist agents plug in without re-architecting |

## 3. High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                           │
│                                                                      │
│   app/representative.py        app/customer_portal.py               │
│   AI Sales Copilot UI          Customer Self-Service UI             │
│   (Streamlit)                  (Streamlit)                          │
│         │                            │                              │
└─────────┼────────────────────────────┼──────────────────────────────┘
          │                            │
          ▼                            ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         INTERACTION LAYER                           │
│   Query validation / sanitization · session context · routing        │
│                                                                      │
│   Coordinator Agent ──── routes to a specialist ────┐                │
│      · Decision Engine: route_query / select_action │                │
│      · Session Manager: conversation memory         │                │
│      · Response Validator: field & format checks    │                │
└───────────────────────┬─────────────────────────────┴───────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────────────────────────────┐
│                          AGENT LAYER                                │
│                                                                     │
│   Sales Copilot Agent      Customer Assistant Agent                 │
│   (representative-facing)  (customer-facing)                        │
│        └────────────┬─────────────┘                                 │
│                     ▼                                              │
│   Specialist Agents (Phase 4+): diagnostics · triage · churn        │
└───────────────┬──────────────────────┬──────────────────────────────┘
                │                      │
                ▼                      ▼
┌────────────────────────────┐  ┌──────────────────────────────────────┐
│        TOOL LAYER          │  │          DATA LAYER                 │
│   Tool Registry (tool_name │  │   Customer 360 (CRM + billing sync) │
│   → function) with retry   │  │   Product catalog (plans/devices)   │
│                            │  │   Promotion engine                  │
│   Services:                │  │   Operational data (store/queue/     │
│    · profile lookup        │  │              workforce)              │
│    · usage analysis        │  │   Invoice history                    │
│    · upgrade eligibility   │  │                                     │
│    · plan recommendation   │  │   data/business_data/*.json        │
│    · offer matching        │  │   data/knowledge_base/*.md.txt      │
│    · service request       │  │                                     │
└────────────────────────────┘  └──────────────────────────────────────┘
```

## 4. Components

### 4.1 Presentation Layer

Two Streamlit front-ends, one per persona:

- **`app/representative.py` — AI Sales Copilot (Representative-Facing)**
  - Customer Case panel (Customer 360 summary, plan, usage, eligibility)
  - Agent System run trace (what the AI did, step by step, for transparency)
  - Decision panel (recommended next step, evidence, confidence, next-best-action)
  - Inputs: customer selection, representative questions
  - Outputs: plan / promotion recommendations, next best action

- **`app/customer_portal.py` — Customer AI Assistant (Customer-Facing)**
  - Self-service plan and device recommendations
  - Digital check-in, wait-time estimation, issue triage
  - Digital account management and bill optimization guidance
  - Inputs: customer queries, customer ID
  - Outputs: answers, offers, digital resolutions

### 4.2 Interaction Layer

| Component | Responsibility |
|---|---|
| **Coordinator Agent** | Entry point for every turn; orchestrates the pipeline end-to-end |
| **Decision Engine** | One LLM call to pick a specialist (`route_query`); function-calling for structured actions (`select_action`) |
| **Session Manager** | Persists conversation turns and context per customer/session |
| **Response Validator** | Ensures replies have required fields and non-empty content before returning |

### 4.3 Agent Layer

| Agent | Persona | Capabilities |
|---|---|---|
| **Sales Copilot Agent** | Representative | Customer 360, usage analysis, upgrade eligibility, plan/promotion matching, conversational sales guidance |
| **Customer Assistant Agent** | Customer | Recommendations, self-service plan/device advice, bill optimization, issue triage |
| **Specialist Agents (Phase 4+)** | Slotted in later | Diagnostics, churn prediction, workforce planning, demand forecasting |

### 4.4 Tool Layer

A registry maps tool names (e.g., `lookup_customer_profile`, `check_upgrade_eligibility`, `recommend_plan`, `open_service_request`) to concrete functions. Calls are wrapped with retry logic for transient failures.

### 4.5 Data Layer

| Dataset | Source | Used By |
|---|---|---|
| Customer 360 | CRM records (`CUST-*`) | Sales Copilot, Customer Assistant |
| Billing & invoice history | Billing accounts (`BILL-*`, `INV-*`) | Upgrade eligibility, bill optimization, churn signals |
| Product catalog | Plans & devices | Plan/device recommendations |
| Promotions | Offers & device promos | Offer matching, upsell |
| Operational data | Store, queue, workforce | Digital check-in, wait-time, staffing (Phase 4+) |
| Knowledge base | Policies, processes, eligibility terms (markdown) | Cited answers, guidelines for rep & customer |

Synthetic business data is generated by `scripts/business_data_generator.py` into `data/business_data/` as linked CRM + billing pairs with six months of invoice history each, plus a product catalog and promotions. Knowledge documents are generated by `scripts/knowledge_data_generator.py` into `data/knowledge_base/`.

## 5. Representative Interaction Flow

1. Representative selects a customer → Customer 360 is assembled from CRM + billing data.
2. Representative asks a question (e.g., "What is the best plan for this customer?").
3. Coordinator receives the query with session context.
4. Decision Engine routes to the Sales Copilot Agent.
5. Agent selects an action via function-calling (e.g., `recommend_plan`).
6. Tool executes against the data layer.
7. Response is validated and returned with recommendation, evidence, and confidence.
8. Representative reviews the Decision panel and proceeds with the next best action.

## 6. Security, Privacy & Governance (Phase 1 Baseline)

- **Authentication & authorization** at the portal boundary per persona (representative vs. customer).
- **Least-privilege tool access** — agents can only call tools appropriate to their persona.
- **Data masking** for PII in logs and traces.
- **Prompt/input validation** — queries sanitized before entering the agent layer.
- **Audit trail** — every recommendation (run trace) recorded for accountability.
- **Consent & retention** rules applied to customer data before any AI processing.

## 7. Phase Mapping

| Phase | Focus | Architecture Impact |
|---|---|---|
| **Phase 1 — Foundation (M0–2)** | KPIs, journey map, data blueprint, governance | Data layer, schema, security baseline |
| **Phase 2 — Representative Copilot (M3–5)** | Sales Copilot | Interaction + Agent + Tool layers for representative persona; `app/representative.py` |
| **Phase 3 — Customer AI Assistant (M6–9)** | Omnichannel self-service | Customer persona agents; `app/customer_portal.py`; web/mobile/kiosk touchpoints |
| **Phase 4+ — Intelligent Automation (M10+)** | Provisioning, diagnostics, predictive ops | Specialist agents; automation services; predictive models |

## 8. Status of Current Codebase

| Artifact | Status | Role |
|---|---|---|
| `docs/brief.md` | Done | Business brief, KPIs, roadmap |
| `data/business_data/*`, `data/knowledge_base/*` | Done | Synthetic business data + knowledge base |
| `scripts/business_data_generator.py` | Done | Generates synthetic datasets |
| `app/representative.py` | Layout only | Sales Copilot UI scaffold (no backend) |
| `app/customer_portal.py` | Layout only | Customer portal UI scaffold (no backend) |
| `src/omni_connect/` | Boilerplate | Application source root |

## 9. Tech Stack

| Layer | Choice |
|---|---|
| Front-ends | Streamlit (Python) |
| Language | Python ≥ 3.13 (managed with `uv`) |
| Data validation | Pydantic |
| Synthetic data | Faker |
| Agent orchestration | (To be implemented — see `src/`) |
| Data persistence | (To be implemented — JSON today, DB in later phases) |