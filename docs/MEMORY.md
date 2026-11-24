# Project Memory

## Current Status
Frontend application completely built, secured, styled, and validated against the PRD, ARCHITECTURE, DESIGN, and SECURITY specifications. All unit and integration test suites passing (19/19 tests).

## Completed Tasks
- **Phase 1: Setup (TASK-001 - TASK-005)**: Folder structure, virtualenv & dependencies, app factory (`app/__init__.py`), `.env`, `run.py`, security headers, custom error pages (400, 403, 404, 413, 500), and `base.css` design system tokens.
- **Phase 2: Database (TASK-006 - TASK-007)**: SQLite schema (`users`, `scans`) with foreign keys, index optimization, and ownership query helper (`get_scan_for_user`).
- **Phase 3: Authentication (TASK-008 - TASK-012)**: Split clinical auth layout (`auth.html`, `auth.css`), Werkzeug password hashing, rate limiting, session fixation protection, `login_required` decorator, and comprehensive auth tests.
- **Phase 4: Dashboard (TASK-013 - TASK-016)**: Two-column responsive dashboard (`dashboard.html`, `dashboard.css`), drag-and-drop file upload with live preview (`preview.js`), and live input validation hints (`validate.js`).
- **Phase 5: Upload & Prediction (TASK-017 - TASK-021)**: Magic byte checking, Pillow re-encoding and EXIF stripping, isolated storage in `private_uploads/`, `predictor.py` contract stub, and prominent "Demo result" label.
- **Phase 6: Reports (TASK-022 - TASK-025)**: Dedicated printable report view (`report.html`), black-and-white print stylesheet (`print.css`), authenticated image streaming route (`/report/<id>/image`), history table, and permanent report/image deletion.
- **Phase 7: Security & QA (TASK-026 - TASK-029)**: Access control tests confirming User A cannot view User B records (returns 404), upload attack prevention tests, CSRF rejection, and payload size restriction verification.

## Next Step
- Phase 8: When trained deep learning weights are available, replace stub in `app/services/predictor.py` and remove placeholder demo label (TASK-030, TASK-031).
