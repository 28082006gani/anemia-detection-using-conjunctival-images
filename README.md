# AnemiaScan – Non-invasive Anemia Screening (Frontend)

Deep learning based anemia detection using conjunctival images. This repository contains the **frontend** (HTML, CSS, Python/Flask). The trained model plugs in through `app/services/predictor.py`.

## Features
- Register / Login
- Dashboard with scan form (name, age, place, PNG/JPG image)
- Result: Anemia / Non-anemia + hemoglobin (g/dL)
- Printable report
- Private per-user history

## Tech
Python 3.11+, Flask, Jinja2, HTML5, CSS3, Pillow, SQLite

## Setup
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then set SECRET_KEY
python run.py
```
Open http://127.0.0.1:5000

## Project Docs
Read these before coding (also give them to your AI tool):
`docs/PRD.md`, `docs/ARCHITECTURE.md`, `docs/DESIGN.md`, `docs/RULES.md`, `docs/SECURITY.md`, `docs/TEST_PLAN.md`, `TASKS.md`

## Tests
```bash
pytest
```

## Disclaimer
This tool is a screening aid, not a medical diagnosis. Results must be confirmed by a laboratory blood test and a qualified doctor.
