# Product Requirements Document

## Product
**AnemiaScan** – Deep learning based anemia screening using conjunctival (eye) images.

## Problem
Traditional anemia detection needs a blood sample and a laboratory test. This causes discomfort, costs money and is hard to access in rural and low-resource areas. A non-invasive screening method that uses an image of the conjunctiva (inner lower eyelid) is needed.

## Target Users
- Patients / general public (self-screening)
- Health workers, ANMs, ASHA workers, camp volunteers
- Students and researchers demonstrating the project

## Goal
Provide a simple, secure web interface where a user uploads a conjunctival image, enters basic details, and receives an anemia / non-anemia result with an estimated hemoglobin (Hb) value, plus a printable report.

## Scope Note (Frontend Only)
This repository contains only the **frontend application** (HTML, CSS, Python/Flask templating and session handling). The trained deep learning model is a separate component. The frontend talks to it through one function, `predict(image_path)` in `app/services/predictor.py`, which currently returns **clearly labelled placeholder values** until the real model is plugged in.

## Core Features
1. Register / Login page (single entry page)
2. Dashboard (main working screen)
3. New scan form: Name, Age, Place, Image upload (PNG, JPG/JPEG)
4. Result panel: Anemia / Non-anemia + Hemoglobin value (g/dL)
5. Printable report
6. Scan history (only the logged-in user's own records)
7. Logout

## MVP
- Register with email + password
- Login / Logout
- Dashboard with scan form and image preview
- Image validation (type, size)
- Show result (status + Hb value)
- Print report (browser print with print-optimised stylesheet)
- View and delete own past reports

## Out of Scope
- Training or hosting the deep learning model
- Mobile application
- Payments
- Doctor/admin portals
- Chat or social features
- Real-time camera capture (upload only, in v1)
- Multi-language (planned later)

## Inputs
| Field | Type | Rule |
|---|---|---|
| Name | text | required, 2–80 chars |
| Age | number | required, 0–100 |
| Place | text | required, 2–80 chars |
| Conjunctival image | file | required, PNG or JPG/JPEG, max 5 MB |

## Outputs
| Output | Description |
|---|---|
| Status | Anemia or Non-anemia |
| Hemoglobin | Estimated value in g/dL (1 decimal) |
| Report | Printable page with patient details, image, result, date, disclaimer |

## Success Criteria
A user should be able to:
1. Create an account and log in
2. Upload a PNG/JPG conjunctival image with name, age and place
3. See Anemia / Non-anemia and Hb value
4. Print the report
5. See only their own reports; another user can never open them
6. Log out and be unable to reach the dashboard

## Medical Disclaimer (must appear on result and report)
This is a screening aid and not a diagnosis. Confirm any result with a laboratory blood test and a qualified doctor.

## Remember
PRD = WHAT + WHY
