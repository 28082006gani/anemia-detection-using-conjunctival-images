# Architecture

## Frontend
HTML5 + Jinja2 templates, CSS3 (plain CSS with variables), minimal vanilla JavaScript (image preview, form validation hints only).

## Backend (thin, frontend-serving layer)
Python 3.11+ with **Flask**. It renders pages, handles sessions, validates uploads and calls the predictor.

## Database
SQLite (file `instance/app.db`) via Python `sqlite3` or SQLAlchemy.

## Authentication
Flask-Login style session auth, passwords hashed with Werkzeug (`generate_password_hash`).

## Security Libraries
- Flask-WTF (CSRF protection)
- Flask-Limiter (rate limiting)
- Pillow (verify and re-encode uploaded images)

## Deployment
Local first. Later: any Python host behind HTTPS (Render, Railway, VPS with Nginx).

## Request Flow
```
User
 ↓
Browser (HTML/CSS)
 ↓
Flask route (auth + CSRF check)
 ↓
Validation service (form + image)
 ↓
Predictor service (placeholder now, DL model later)
 ↓
SQLite (record owned by user_id)
 ↓
Result page / Printable report
```

## Folder Structure
```
anemia-detect/
├── app/
│   ├── __init__.py          # app factory, config, security headers
│   ├── routes/
│   │   ├── auth.py          # register, login, logout
│   │   ├── dashboard.py     # dashboard, new scan, history
│   │   └── reports.py       # view/print/delete report, image serving
│   ├── services/
│   │   ├── predictor.py     # predict(image_path) -> {status, hb}
│   │   ├── validation.py    # form + image validation
│   │   └── storage.py       # safe file save/read
│   ├── models.py            # User, Scan tables
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth.html        # login + register (tabs)
│   │   ├── dashboard.html
│   │   ├── report.html      # printable
│   │   └── errors/{403,404,413,500}.html
│   └── static/
│       ├── css/{base,auth,dashboard,print}.css
│       ├── js/{preview,validate}.js
│       └── img/             # logo, icons only (never user data)
├── private_uploads/         # user images, OUTSIDE static, gitignored
├── instance/                # database, gitignored
├── docs/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

## Pages
1. **Auth page** (`/`): Login and Register tabs.
2. **Dashboard** (`/dashboard`): scan form on left, result panel on right, history below.
3. **Report** (`/report/<id>`): printable view.

## Architectural Rules
- Templates contain no business logic.
- Routes stay thin; logic goes in `services/`.
- Every database query for scans MUST filter by the current `user_id`.
- Uploaded images are never placed in `static/`; they are served only through an authenticated route.
- The predictor is the only place that knows about the model. Swapping the model must not change templates.
- Secrets only from environment variables.

## Predictor Contract
```python
def predict(image_path: str) -> dict:
    """
    Returns:
      {"status": "Anemia" | "Non-anemia",
       "hemoglobin": float,       # g/dL
       "confidence": float,       # 0-1, optional
       "is_placeholder": bool}    # True until real model is connected
    """
```

## Remember
Architecture = HOW
