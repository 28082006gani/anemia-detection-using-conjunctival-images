# Development Rules (for AI coding tools)

## General
- Use Python 3.11+, Flask, Jinja2, plain CSS, minimal vanilla JS.
- No frontend frameworks, no CSS frameworks, no CDN scripts.
- Reuse existing templates and CSS variables.
- Do not duplicate logic. Keep functions small.
- Do not modify unrelated files.

## Before Coding
- Read PRD.md, ARCHITECTURE.md, DESIGN.md, SECURITY.md and TASKS.md.
- Inspect existing code first.
- Make a plan for any change touching more than 3 files.

## UI
- Follow DESIGN.md colours exactly. Use CSS variables only; no hard-coded hex in components.
- Do not add purple, pink or neon gradients. Only the single teal gradient defined in DESIGN.md.
- Include loading, empty and error states.
- Every input has a label.

## Security (non-negotiable)
- Never hard-code secrets. Read from environment.
- Every POST form includes a CSRF token.
- Every scan query filters by `current_user.id`.
- Return 404 (not 403) when a record belongs to someone else.
- Never place uploaded images in `static/`.
- Validate every input on the server, even if JS validates too.
- Never log names, ages, places, emails or image paths with personal data.
- Use parameterised queries only.
- Auto-escape in Jinja; never use `|safe` on user data.

## Model Integration
- Only `services/predictor.py` may call the model.
- Placeholder output must set `is_placeholder: True` and show a visible "Demo result" label in the UI.

## Testing
- Add tests for auth, validation and access control.
- Run `pytest` after each task. Fix failures before continuing.

## Git
- Small commits, message format: `feat:`, `fix:`, `docs:`, `test:`.
- Never commit `.env`, `instance/`, `private_uploads/`.

## Output Report After Each Task
1. Files changed
2. What was implemented
3. Tests run
4. Remaining issues
