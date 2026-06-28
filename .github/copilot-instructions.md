# Team Coding Conventions

- Type hints on every function signature.
- Format with Ruff (line length 88); follow PEP 8.
- Prefer small, pure functions; avoid hidden side effects.
- Handle errors with specific exceptions; never a bare except.
- Write pytest tests for new logic.
- Read secrets from environment variables; never hardcode them.
- Match the structure and naming of the file you're editing.
- When unsure, ask rather than invent an API.