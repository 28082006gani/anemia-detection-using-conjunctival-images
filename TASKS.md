# Tasks

## Phase 1: Setup
- [x] TASK-001 Create folder structure from ARCHITECTURE.md
- [x] TASK-002 Create virtual environment, `requirements.txt` (Flask, Flask-WTF, Flask-Limiter, Pillow, pytest)
- [x] TASK-003 App factory, config from `.env`, `run.py`
- [x] TASK-004 Security headers + custom error pages
- [x] TASK-005 `base.css` with variables from DESIGN.md

## Phase 2: Database
- [x] TASK-006 User and Scan tables (UUID ids, user_id foreign key)
- [x] TASK-007 Helper: `get_scan_for_user(scan_id, user_id)`

## Phase 3: Authentication
- [x] TASK-008 Auth page UI (Login / Register tabs)
- [x] TASK-009 Register logic + validation + password hashing
- [x] TASK-010 Login/logout + session settings + rate limit
- [x] TASK-011 Protect private routes
- [x] TASK-012 Auth tests

## Phase 4: Dashboard
- [x] TASK-013 Dashboard layout (navbar, two columns)
- [x] TASK-014 Scan form (name, age, place)
- [x] TASK-015 Image upload zone + preview (JS)
- [x] TASK-016 Client-side hints validation

## Phase 5: Upload and Prediction
- [x] TASK-017 Server-side image validation + Pillow re-encode
- [x] TASK-018 Safe storage in `private_uploads/`
- [x] TASK-019 Predictor stub with contract
- [x] TASK-020 Save scan and show result panel (status + Hb)
- [x] TASK-021 "Demo result" label for placeholder

## Phase 6: Reports
- [x] TASK-022 Report page template
- [x] TASK-023 `print.css` (A4, black and white friendly)
- [x] TASK-024 Authenticated image route
- [x] TASK-025 History table, delete report (POST + confirm)

## Phase 7: Security and QA
- [x] TASK-026 Access-control tests (user A vs user B)
- [x] TASK-027 Upload attack tests
- [x] TASK-028 Responsive and accessibility pass
- [x] TASK-029 `pip-audit`, DEBUG off, HTTPS config notes

## Phase 8: Model Integration (later)
- [ ] TASK-030 Replace stub in `predictor.py` with trained model
- [ ] TASK-031 Remove placeholder label

## Workflow per task
Read → Plan → Implement → Test → Review → Commit → Update MEMORY.md
