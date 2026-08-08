# Module 4 — Final Deliverables Checklist and Tool-Fit Reflection

**Project:** Task Tracker (Module 4)
**Branch:** `module-4`
**Date:** 2026-08-08

---

## 1. Deliverable checklist

| # | Category | Status | Evidence |
|---|---|---|---|
| 1 | Claude Code setup | **Complete** | `CLAUDE.md` is a committed, git-tracked project-guidance file (commit `a23ca2c`), opening with *"This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository."* |
| 2 | CLAUDE.md verification notes | **Complete** | 7 inline `(verified)` annotations in `CLAUDE.md` covering Python version, empty placeholder packages, `TaskStatus` values, status-transition rules, the overdue rule, CORS config, and frontend UI states. |
| 3 | CI green/red/green evidence | **Complete** | `docs/module4/ci-green-red-green-verification.md` — real commit hashes and GitHub Actions run URLs for the full green→red→green cycle. |
| 4 | Docker `/health` and `whoami` evidence | **Complete** | `/health` + container-healthy status documented in `docs/decisions/Technical_Notes.md`. **`whoami` verified live this session:** `docker exec tt-verify whoami` → `app`, confirming the running container used the non-root `app` user declared by the Dockerfile. |
| 5 | Documentation claim-vs-reality | **Complete** | `docs/decisions/Technical_Notes.md` §1 — the docstring `+00:00`/`Z` timestamp mismatch and the `CLAUDE.md` pytest/httpx stale-pinning claim, both verified and corrected. |
| 6 | AI review triage | **Complete** | `docs/decisions/Technical_Notes.md` — three review findings: one fixed, two classified Noise, with reasoning. |
| 7 | Technical note and README link | **Complete** | `docs/decisions/Technical_Notes.md` (`Status: Final`); linked from `README.md` §10 and listed in §8's tree. Committed and pushed as `5a3255a`. |

---

## 2. Tool-fit reflection

**Cursor:**
I used Cursor initially as an AI-focused development editor for interactive, in-IDE coding and editing, with prompt refinement and inspection/testing of generated changes before accepting them. I moved to VS Code with GitHub Copilot when that became the course-instructed workflow, then returned to my still-active paid Cursor subscription once my Copilot Free usage limit ended — a practical constraint, not a technical judgment against either tool. Cursor helped me with larger implementation loops: working through broader coding changes iteratively inside the development environment by prompting, implementing/editing, inspecting, testing, and refining.

**GitHub Copilot in VS Code:**
I used GitHub Copilot after switching to VS Code as instructed, mainly for focused implementation — generating and modifying functions, and frontend/backend coding tasks — with the same practice of structured prompts, inspection, and testing before accepting output. I stopped using Copilot when my Free-tier usage limit ended and returned to my still-active paid Cursor subscription. Copilot fit as continuous editor pairing: AI assistance integrated into my normal VS Code coding workflow while I worked on focused code changes.

**Claude Code:**
I used Claude Code extensively throughout Module 4, and it fit well with the repository-wide, multi-step nature of that work: searching files/sections/exact lines, inspecting implementation details, verifying documentation claims against source code, tests, runtime behavior, Docker output, and Git history, editing only after verification, reviewing diffs, running tests and commands (including the CI and Docker `/health`/`whoami` checks), and controlling documentation and Git work through to commit and push — a repeated search → inspect → verify → edit → review diff → test pattern. Clear prompting, inspection, verification, and approval weren't unique to Claude Code — I used those same practices with Cursor and Copilot; what suited Claude Code was terminal delivery work: repository-wide, command-line-oriented, multi-file and multi-step verification and delivery tasks.

**On overlap:** these workflows overlap across tools — this describes how I actually used each one, not a ranking, and no single tool is declared better overall.

---

## 3. Missing evidence I still need to collect

I have firsthand usage evidence for all three tools from my actual project work. For Cursor and GitHub Copilot, that evidence comes primarily from my direct development experience: writing and refining prompts, generating or modifying code, inspecting generated changes, testing and verifying results, and approving or refining the output. Claude Code additionally has extensive repository-recorded evidence from the Module 4 work — committed files, Git history, CI evidence, Docker/runtime verification, documentation verification, file/line inspection, diffs, and command output. This difference in evidence type does not mean Cursor or Copilot were not actually used — it reflects that this project's Module 4 phase was done with Claude Code, so that's where the repository artifacts accumulated.

Based on the evidence currently available, no additional material evidence is currently required for this reflection.
