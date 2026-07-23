# Task Tracker API — Module 1

A learning-project REST API built with **Python**, **FastAPI**, and **Pydantic**.

This module implements the foundational application skeleton as defined in
**ADR-001: Use FastAPI with In-Memory Storage for Module 1**. The backend
currently exposes only a health check endpoint. Task CRUD endpoints,
business rules, and status-transition validation will be added in
subsequent modules.

## Architecture

Per ADR-001, the project uses **in-memory storage** (a Python dictionary)
rather than a database, to keep Module 1 focused on:

- Building REST API endpoints with FastAPI
- Using Pydantic for request validation
- Implementing CRUD operations (upcoming)
- Applying business rules (upcoming)

The codebase is structured to separate concerns, even though most layers
are currently empty placeholders: