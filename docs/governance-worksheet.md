# Module 5 Governance Worksheet

## 1. What I Shared with AI

| # | Item shared | Risk | Reason | Safer future version | Ambiguity to resolve |
|---:|---|---|---|---|---|
| 1 | Task Tracker requirements and scope | Low | Course-project requirements contained no evidenced secrets, PII, or proprietary logic. | Share a concise requirements summary without unrelated institutional details. | None material. |
| 2 | User stories, acceptance criteria, and business rules | Low | Ordinary business rules for a course Task Tracker. | Share only the acceptance criteria relevant to the current task. | None material. |
| 3 | Backend source and implementation | Medium | Complete source exposes implementation details if the repository is private. | Share only the relevant route, model, or storage excerpt. | Whether the repository was public and authorized for sharing. |
| 4 | Frontend source and implementation | Medium | The complete frontend exposes more implementation detail than most questions require. | Share only the relevant HTML or JavaScript function. | Whether the repository was public and authorized for sharing. |
| 5 | Automated tests and behavior | Medium | Tests reveal expected behavior, edge cases, and internal assumptions. | Share only the relevant test, fixture, and sanitized result. | Whether the tests were already public. |
| 6 | Repository structure and development configuration | Medium | Complete structure and configuration reveal internal development context. | Provide a reduced file tree and only relevant dependencies or commands. | Whether the repository material was public. |
| 7 | Architecture and design documentation | Medium | ADRs and technical notes can expose non-public reasoning and rejected alternatives. | Summarize the relevant decision, constraints, and outcome. | Whether the documentation was public or course-internal. |
| 8 | Prompts and AI-assisted development records | Medium | Prompt logs can expose development history, mistakes, and unrelated contextual information. | Share only the necessary sanitized prompt excerpt. | Whether the records contained additional personal or institutional details. |
| 9 | Terminal output and development logs | Medium | Logs may expose local paths, usernames, IDs, and environment details. | Share only relevant lines after removing paths, identifiers, and environment values. | Whether every shared log was fully sanitized. |
| 10 | Screenshots of the running Task Tracker | Medium | Although task data was synthetic, some screenshots exposed local paths, terminal details, or development-environment information. | Crop screenshots and remove or obscure local paths, terminal details, and unrelated screen content. | None; exposure of local development details is established. |
| 11 | Swagger/API request and response evidence | Low | Requests used synthetic task data, random assignee names, and local Task Tracker IDs. | Continue using synthetic values and omit local IDs when unnecessary. | None; the data is confirmed synthetic and local. |
| 12 | Security-review source/configuration context | Medium | Security and configuration details expose a potentially private security posture and system assumptions. | Share only relevant configuration lines and state the local course scope. | Whether the repository was public. |
| 13 | Manual security/governance observations | Low | These were course-project design suggestions and a documentation defect, not sensitive operational information. | Share categorized observations without unrelated context. | None material. |
| 14 | Git/repository history evidence | Medium | History can reveal authors, development chronology, mistakes, and abandoned approaches. | Share only relevant hashes, paths, and summarized conclusions. | Whether the repository history was public. |
| 15 | Docker and CI configuration | Medium | Build and workflow details can expose repository identifiers and operational assumptions. | Share only relevant steps with repository and account identifiers removed. | Whether the configuration was public. |
| 16 | Course/project documentation | Medium | Complete documentation may contain non-public course context and verification history. | Share only the necessary section after removing local and institutional details. | Whether the documentation was public or authorized for redistribution. |

### Important business-rule context

- `ToDo → InProgress`: allowed
- `InProgress → Done`: allowed
- `Done → InProgress`: allowed
- Same-status updates: allowed as no-ops
- `ToDo → Done`: rejected
- `InProgress → ToDo`: rejected
- `Done → ToDo`: rejected

### Git-history clarification

Git history was reviewed after AI-generated documentation incorrectly claimed that a frontend “Delete Task” feature existed and had been manually browser-verified. The history confirmed that Delete existed only in the backend/API and was tested through Swagger using the task ID; no frontend Delete functionality had ever been implemented.

### Final totals

- Low: 4
- Medium: 12
- High: 0

No High-risk sharing was evidenced. The main lesson is to minimize context, sanitize logs and screenshots, and confirm whether repository material is public/private and authorized before sharing complete source or internal documentation.

## 2. Medium-item governance-habit prioritization

| Priority | Item | Current risk | Habit to change | Why change this habit first | Concrete future practice |
|---:|---|---|---|---|---|
| 1 | Terminal output and logs | Medium | Sanitize logs | Logs commonly expose paths, usernames, IDs, environment details, or accidental secrets. | Share only relevant lines and remove local identifiers, headers, paths, and environment values. |
| 2 | Screenshots | Medium | Crop and sanitize screenshots | Images can unintentionally expose terminal details, paths, notifications, and unrelated screen content. | Crop tightly, use synthetic data, and inspect the entire visible image before sharing. |
| 3 | AI-development records | Medium | Minimize prompt context | Prompt records can combine code, decisions, mistakes, and personal or institutional context. | Share only the necessary prompt excerpt after removing unrelated history and identifiers. |
| 4 | Backend source | Medium | Share minimal code excerpts | This reduces implementation disclosure while preserving necessary technical context. | Provide only the relevant function, model, and smallest required dependencies. |
| 5 | Frontend source | Medium | Share minimal code excerpts | Complete frontend files reveal more implementation detail than most questions require. | Extract only the relevant HTML, JavaScript, and surrounding context. |
| 6 | Security-review context | Medium | Limit configuration exposure | Combined security details can reveal system assumptions and weaknesses. | Share only the relevant sanitized configuration lines. |
| 7 | Git history | Medium | Remove identities and unrelated history | Repository history may disclose authors, mistakes, chronology, and abandoned work. | Provide only relevant commit hashes, paths, and conclusions. |
| 8 | Docker and CI configuration | Medium | Sanitize operational configuration | Workflow files may expose repository identifiers and operational assumptions. | Share relevant stages or steps with account and repository identifiers replaced. |
| 9 | Architecture documentation | Medium | Summarize decisions | Complete ADRs may reveal unnecessary internal reasoning and alternatives. | Share the relevant decision, constraints, and outcome. |
| 10 | Tests and test behavior | Medium | Share focused tests | Full test suites reveal extensive behavior and edge cases. | Share only the relevant test, fixture, and sanitized output. |
| 11 | Course/project documentation | Medium | Extract relevant sections | Complete documents may expose unrelated course and verification context. | Paste only the necessary section after removing local details. |
| 12 | Repository structure and configuration | Medium | Reduce structural disclosure | Full trees and environment information are rarely necessary for a bounded question. | Provide a trimmed file tree and only relevant dependencies or commands. |

### Top three habits

1. Sanitize terminal output and logs.
2. Crop and inspect screenshots before sharing.
3. Share only the minimum code, prompt, and contextual information necessary.

## 3. What I Received from AI

To be completed in the next Part 5.3 step.
