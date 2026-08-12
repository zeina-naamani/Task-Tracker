# 5.5D — Compare Context Strategies

## Strategy comparison table

| Strategy | What it got right | What it got wrong, missed, or invented | Best-suited task shape |
| -------- | ----------------- | -------------------------------------- | ---------------------- |
| **A — Minimal context** | Provides the broadest end-to-end account: frontend workflows, backend request flow, data model, storage, business rules, tests, and important files. Its numbered creation flow is especially useful for tracing a user action across layers. | The health endpoint is missing or not covered in its functional summary. Some operational topics remain unconfirmed. Although A makes numerous detailed claims, no invention can be established from comparison of the three documents alone; B generally corroborates them, while C explicitly lacked visibility into those areas. | Broad discovery or onboarding tasks where end-to-end coverage and concrete workflow tracing matter more than tightly bounded evidence. |
| **B — Structured context** | Produces the most balanced system overview. It covers the frontend, backend, data lifecycle, exact status transitions, filtering, tests, key files, CORS, and known architectural limits while remaining concise. Its separation of confirmed behavior from unconfirmed operational concerns is clear. | It gives less detail than A about the creation flow after the response, frontend error handling, HTML escaping, timestamps, deletion semantics, and test setup. These are missing or not covered, rather than demonstrably wrong. No invention can be established from the comparison alone. | Repository-level architecture and onboarding documentation where curated structure and summaries provide broad, organized coverage without requiring an exhaustive file-by-file account. |
| **C — Targeted context** | Gives the strongest evidence discipline. It accurately focuses on the API surface, schemas, validation, in-memory CRUD, filtering, timestamps, and overdue computation, and repeatedly marks unsupported areas as “not visible from the files I read.” | Frontend behavior, exact transition rules, tests, documentation, deployment, and wider repository structure are missing or deliberately not covered. Its “Key files” section cannot reach five fully described files. No invention can be established from the comparison alone. | Narrow implementation analysis, change planning, or component documentation where a few authoritative anchor files define the relevant boundary and unsupported claims must be minimized. |

## Verdict

Strategy B should be the basis for the final Task Tracker architecture document because it offers the best combination of repository-wide coverage, organization, concision, and explicit treatment of unknowns. Strategy A’s detailed end-to-end request trace is worth retaining as a model for explaining workflows, while Strategy C’s strict evidence boundaries are valuable whenever the supplied context is intentionally narrow.

## Context-engineering rule

> For a repository-wide Task Tracker architecture or onboarding documentation task, I use Strategy B—structured context using repository guidance and file summaries—because it exposes the frontend, backend, business rules, tests, and operational boundaries needed for an end-to-end explanation.
>
> For a bounded Task Tracker feature or change-planning task, I use Strategy C—targeted context using a small set of anchor files—because it keeps inspection focused on the directly relevant implementation path and clearly marks behavior outside that scope as unconfirmed.

## Source documents

- `docs/architecture-A.md`
- `docs/architecture-B.md`
- `docs/architecture-C.md`

The 5.5D comparison was based only on these three architecture documents.
