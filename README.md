# omni-connect

AI-Powered Telecom Retail Transformation — a unified AI Retail Copilot platform that empowers telecom retail representatives and customers with real-time intelligence, personalized recommendations, and seamless omnichannel experiences.

## Overview

Telecom retail stores struggle with fragmented systems, forcing representatives to switch between 5–10 applications during a single customer interaction. This leads to long handling times (35–50 min), high queue walk-outs (~22%), inconsistent experiences, and long onboarding cycles.

The AI Retail Copilot platform unifies customer, product, promotion, and operational data into a single intelligent experience across two core capabilities:

- **AI Sales Copilot (Representative-Facing):** Real-time customer info, plan recommendations, upgrade opportunities, and next-best actions in one interface.
- **Customer AI Assistant (Customer-Facing):** Personalized recommendations, omnichannel engagement, and self-service support across web, mobile, and in-store.

## Business Outcomes

| Metric / KPI | Current State | Phase 2 Target | Phase 3 Target | Long-Term Target |
|---|---|---|---|---|
| Average Handling Time | 35–50 min | 20–25 min | 15–18 min | 10–12 min |
| Queue Walk-Out Rate | ~22% | ~15% | <5% | <3% |
| Employee Onboarding | 4–6 weeks | 1–2 weeks | 1–2 weeks | <1 week |
| Customer Satisfaction (CSAT) | Baseline | +10 to +15 pts | +20 to +25 pts | +25+ pts |
| Sales Conversion Rate | Baseline | +10–15% | +12–18% | +20% |
| Upsell Revenue | Baseline | +10–15% | +15–20% | +20%+ |

## Roadmap

- **Phase 1 — Foundation & Data Readiness (Months 0–2):** KPI baselines, journey mapping, data architecture, governance.
- **Phase 2 — Representative Copilot (Months 3–5):** Customer 360, usage analysis, plan/promotion recommendations, conversational sales guidance.
- **Phase 3 — Customer AI Assistant (Months 6–9):** Self-service across web, mobile, kiosk; digital check-in; bill optimization.
- **Phase 4+ — Intelligent Automation:** Digital identity/provisioning, smart diagnostics, predictive retail optimization.

See [docs/brief.md](docs/brief.md) for the full executive brief.

## Project Structure

```
omni-connect/
├── data/                             # Generated synthetic data
│   ├── business_data/                # JSON datasets (CRM, billing, catalog, promos)
│   └── knowledge_base/               # Markdown knowledge docs (policies, processes)
├── scripts/
│   ├── business_data_generator.py    # Generates synthetic business JSON data
│   └── knowledge_data_generator.py   # Generates markdown knowledge base
├── src/
│   └── omni_connect/                # Application source
│       └── __init__.py
└── docs/
    ├── brief.md                     # Executive brief
    └── architecture.md              # System architecture
```

## Getting Started

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (package manager)

### Setup

```bash
uv sync
```

### Regenerate Synthetic Data

Generates JSON datasets under `data/business_data/` (linked CRM + billing pairs with 6 months of invoice history per customer, plus the product catalog and promotions) and the markdown knowledge base under `data/knowledge_base/`.

```bash
cd scripts
uv run python business_data_generator.py
uv run python knowledge_data_generator.py
```

### Run

```bash
uv run omni-connect
```

## License

&copy; M.Mezni. See author info in [pyproject.toml](pyproject.toml).
