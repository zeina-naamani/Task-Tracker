# Personal AI Coding Playbook

## When I reach for AI first

- I first use AI to review the instructor-provided improved prompt and check whether it needs additional constraints or specifications based on my project. If refinements are suggested, I review them and decide whether to approve them, reject them, or keep the instructor's original prompt.
- I also reach for AI for planning, reviewing work, debugging, generating an initial draft, and comparing choices.
- **Course evidence:** During the Comments feature planning in 5.4B/5.4C, I used AI to refine and review the plan and identify gaps, but I reviewed its suggestions, made refinements when needed, and made the final decisions before accepting changes. After choosing Architecture Option A for the Task Tracker, I used AI to generate an initial ADR draft based on my decision and reasoning. I then reviewed and refined the draft before using the revised version as the final project documentation. During the Task Tracker frontend/backend integration work, I used ChatGPT and Cursor to troubleshoot the CORS problem, then verified the fix myself by running the application and confirming that the Kanban board loaded and appeared correctly. In 5.5, comparing the three architecture strategies helped me refine the conclusion that Strategy B was best for repository-wide architecture/onboarding work, while Strategy C was better for bounded feature or change-planning tasks.

## When I do not reach for AI

- I do not let AI independently make final decisions, modify files before I review and approve the proposed changes, or commit and push changes without my approval.
- I do not want AI making assumptions about the repository when it can inspect the actual files, and I independently verify important results before accepting them.
- **Course evidence:** In 5.4C, I had Codex show me the exact proposed changes before modifying the Comments feature plan. I reviewed and approved the changes first, then reviewed the resulting diff before allowing the commit and push. In 5.5A, I checked the claim about task deletion and confirmed that deletion exists in the backend API but is not exposed as a frontend UI action. I had Codex correct that distinction before I approved the architecture document.

## My Non-Negotiables

- I want AI to stick to what I asked for, use the actual project files as evidence, and tell me when something cannot be confirmed instead of assuming or inventing it.
- Important decisions remain my final decisions. Existing working behavior should not be changed unnecessarily, and sensitive information must not be exposed to AI.
- **Course evidence:** In Architecture Strategy C (5.5C), I limited Codex to `app/main.py`, `app/models.py`, and `app/storage.py`. Information outside those files had to be marked “not visible from the files I read” rather than inferred. During the Task Tracker frontend work, I checked that existing creation, editing, validation, and drag-and-drop behavior still worked after changes. During the course, when using AI coding tools such as Codex, Cursor, GitHub Copilot, and Claude Code, I kept their access and the information I provided project-specific and limited to what was relevant to the current task, following my existing security practice of keeping unrelated or sensitive information outside the approved scope.

## My Review Rules

- I review AI output against the original task and requirements, check proposed diffs before approving changes, verify that only intended files changed, and check Git status before committing.
- I refine or reject AI suggestions when needed, run relevant tests when application code changes, and commit or push only after reviewing and approving the result.
- **Course evidence:** In 5.4C, I reviewed the proposed changes and resulting diff before approving the commit and push. In 5.5A, I independently checked the task-deletion claim and required a correction before approving the architecture document. During the Task Tracker backend work, I ran the automated test suite and confirmed that all 44 tests passed instead of relying only on the AI-generated implementation. During Module 5 documentation work, I used `git status --short` before committing and checked it again after pushing to confirm that the working tree was clean.

## What I am still figuring out

- How much context should I give AI?
- When is it better for me to work with AI through the terminal, such as Claude Code, versus directly with the repository/folder, such as Codex?
- When should I test manually vs. use automated tests?

## Decision Card

- **For a new feature I reach for:** ChatGPT for planning and refining requirements, then the appropriate repository-aware tool for repository-grounded planning or implementation.
- **For a code review I reach for:** Codex for repo-grounded code review, then I review and verify its findings before accepting any changes.
- **For debugging I reach for:** ChatGPT to help me understand the problem and narrow down possible causes, then Cursor when the debugging requires working through the actual project code.
- **For infrastructure I reach for:** Claude Code for terminal-based infrastructure work; I still review the proposed changes and risks before approving them.
- **I will never paste** passwords, API keys, access tokens, login credentials, private keys, secrets from `.env` files, or other sensitive information into an AI tool.
- **My one rule is:** Use AI as a partner, not as the final decision-maker: I inspect, verify, reject, revise, and own the final result.
- **Decision evidence:** In **Module 1 (Requirements & Architecture)**, I used browser-based AI tools, including ChatGPT and Claude, to help with reasoning, drafting, comparing choices, and refining project requirements and architecture decisions, while I reviewed and made the final decisions myself. In **Module 2 (Backend Development)**, I used Cursor while developing the FastAPI backend and working through the implementation, validation, and business rules. In **Module 3 (Frontend & Testing)**, I initially used GitHub Copilot for continuous editor assistance while developing and reviewing the frontend and testing work. After reaching its usage limit, I continued the development work with Cursor. I also used ChatGPT and Cursor while troubleshooting the frontend/backend CORS integration and verified the fix myself by running the application and confirming that the Kanban board loaded and appeared correctly. In **Module 4 (DevOps & CI/CD)**, I used Claude Code for terminal-based work involving Docker and CI/CD, then verified the results myself through the terminal and Docker Desktop. In **Module 5 (Security & Governance)**, I used Codex for repository-grounded planning, review, and governance work; during the security review, I graded its findings as Valid, False Positive, or Noise and compared them with my manual scan.

## 30-Day Re-Read Commitment

I will re-read this playbook in 30 days, review whether these rules still match how I actually use AI, and update them based on what I have learned.
