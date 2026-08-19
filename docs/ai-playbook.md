# AI Playbook

## When I reach for AI first

I reach for AI when the task is bounded and I can give it clear evidence: reviewing a known diff, brainstorming edge cases after requirements are settled, suggesting focused tests, comparing implementation options, or drafting technical documentation that I will check against the repository. In this course, AI was useful for reviewing code and plans, identifying gaps, comparing architecture approaches, and drafting CI, Docker, and documentation work. I also use it for debugging after I have collected a real error, failing test, or runtime observation.

AI helps me explore and review; it does not make my final product or architecture decisions. My working loop is **Ask → Inspect → Run → Test → Refine**.

## When I do not reach for AI first

I do not start with AI when requirements are unclear, when I need to inspect the repository before forming a question, or when the learning objective is for me to reason through the problem myself. I pause before using AI for security-sensitive or high-risk changes unless I have concrete evidence and a narrow scope. I also avoid asking AI to decide when it lacks the local context needed to distinguish an intended behavior from a defect.

I do not use AI to expand a task into authentication, a production database, deployment architecture, unrelated frontend work, or broad refactoring when those are outside the requirements. A technically true production-hardening suggestion is not automatically an actionable defect in a small learning project.

## My non-negotiables

- I never paste credentials, tokens, `.env` values, real personal or customer data, production-sensitive logs, or secrets into an AI tool.
- I keep the task and changed files within the approved scope and preserve existing work.
- I inspect proposed changes and remain responsible for every decision; AI does not stage, commit, or push without my approval.
- I verify important claims with repository evidence, focused checks, and the appropriate full test suite.
- I do not submit a change that I cannot explain, verify, and defend as my own work.

## My review rules

I inspect the actual diff, confirm which files changed, and compare every recommendation with the current requirements and code. I run focused verification for the changed behavior, then the appropriate full test suite; I add a human API or UI check when it provides evidence that automated tests do not. I grade code-review findings as **Useful / Noise / Wrong** and security findings as **Valid / False Positive / Noise** instead of accepting every suggestion.

CR-1 showed why semantic judgment matters. AI initially grouped description, status, and priority null values together as values to reject. Repository inspection showed that descriptions are intentionally empty strings, while status and priority must remain non-null; assignee and due date are intentionally nullable. I therefore chose field-specific behavior, verified it with focused and full tests, and checked it separately through Swagger. That experience reinforced my rule to distinguish a plausible AI pattern from the product semantics actually supported by the repository.

## What I am still figuring out

I am still learning when production hardening is proportionate for a small project, when different AI coding tools best fit a task, and what team conventions are most useful for recording AI assistance. I also want more experience deciding how much automated browser or UI testing is justified for a project of this size.

## Decision Card

### New feature

AI may help clarify requirements, identify edge cases, compare options, and suggest tests. Before implementation, I inspect the repository, confirm the scope and acceptance criteria, and make the final design decision myself.

### Code review

I ask AI to review a specific diff, then grade each finding and verify useful comments against the code, requirements, and tests. A confident comment is still only a candidate until the evidence supports it.

### Debugging

I collect the real error, failing test, request/response, or runtime behavior before asking for possible causes. I test the smallest supported explanation before accepting a fix.

### Infrastructure

I check CI, Docker, and configuration suggestions against the actual project requirements and documented commands. I verify them through configuration inspection and safe runtime commands, and I reject deployment or hardening work that is outside scope.

### Never paste

I never paste credentials, tokens, `.env` values, secrets, real personal or customer data, or production-sensitive logs.

### One rule

If I cannot read, understand, explain, and verify an AI-generated change, I do not consider it my own work and I do not submit it.
