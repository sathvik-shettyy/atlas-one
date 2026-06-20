# Contributing to Atlas One

Thank you for helping improve Atlas One.

## Development Principles

- Keep protected applications hidden behind Atlas One Gateway.
- Do not expose internal service ports.
- Prioritize security, maintainability, and clarity.

## Local Setup

1. Copy `.env.example` to `.env`.
2. Run `docker compose up -d --build`.
3. Use `http://localhost:8080` for all user interactions.

## Pull Requests

- Open PRs against `main`.
- Ensure CI passes.
- Include security impact notes when identity or policy behavior changes.

