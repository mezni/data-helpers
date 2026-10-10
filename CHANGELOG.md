# Changelog

## [0.0.6] — Structured LLM Outputs
- Enforced structured LLM outputs.

## [0.0.5] — LLM Ticket Classification
- Integrated LLM ticket classification.

## [0.0.4]
- Edge cases, regression tests, and logging implemented.

## [0.0.3] — Data Contracts
- Implemented TicketInput and TicketOutput.
- Integrated validation into the classifier.
- Added schema tests and updated classifier tests.

## [0.0.2] — Business Logic
- Implement the ticket classifier

## [0.0.1] — Foundation
Initialized uv project (pyproject.toml, uv.lock, virtualenv) with a src layout.
Added runtime dependencies: anthropic, pydantic, python-dotenv.
Added development dependency: pytest.
Added .env.example and gitignored local .env.
Scaffolded package layout under src/support_agent/ and tests/.
Added sample datasets data/knowledge_base.json and data/tickets/tickets.json.

## Version History

| Version | Feature Domain | Key Objectives |
| --- | --- | --- |
| 0.0.1 | Project Foundation | Scaffold uv project (pyproject.toml, uv.lock, virtualenv) with a src layout; add runtime dependencies; add pytest; add .env.example and gitignored local .env. |
| 0.0.2 | Business Logic | Implement the ticket classifier: extract category, order_id, and needs_order_lookup from unformatted ticket text. |
| 0.0.3 | Data Contracts | Implement TicketInput/TicketOutput Pydantic schemas; integrate validation into the classifier; add schema tests and update classifier tests. |
| 0.0.4 | Edge Cases, Regression Tests, and Logging | Edge cases, regression tests, and logging implemented. |
| 0.0.5 | LLM Ticket Classification | Integrate LLM ticket classification. |
| 0.0.6 | Structured LLM Outputs | Enforce structured LLM outputs. |