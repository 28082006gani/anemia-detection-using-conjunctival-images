# Security Requirements

Health-related personal data is sensitive. Treat all user input and all stored data as confidential.

## Goals
1. No user can see another user's information.
2. No data theft or leakage (database, images, logs, URLs).
3. Safe handling of uploads.

## Authentication
- Passwords hashed with Werkzeug (scrypt/pbkdf2). Never store plain text.
- Minimum 8 characters, at least one letter and one number.
- Generic login error: "Email or password is incorrect."
- Rate limit login (5 attempts/minute per IP) and register.
- Short lockout after repeated failures.
- Session cookie: `HttpOnly`, `Secure` (in production), `SameSite=Lax`.
- Session expires after 30 minutes idle. Logout clears session.
- Regenerate session on login.

## Authorization (core privacy rule)
- Every scan row has `user_id`.
- Every read, print, image-serve and delete checks `scan.user_id == current_user.id`.
- If not owner → 404.
- Use random UUIDs for report IDs, not sequential numbers.
- Dashboard, report and image routes require login.

## CSRF
- CSRF token on all POST/DELETE forms (Flask-WTF).
- Delete uses POST, never GET.

## File Upload
- Allowed: `.png`, `.jpg`, `.jpeg` only.
- Max size 5 MB (`MAX_CONTENT_LENGTH`).
- Check file signature (magic bytes), not only extension or MIME header.
- Open with Pillow, verify, then **re-encode** to strip EXIF/GPS metadata and any embedded payload.
- Save with random UUID filename; ignore the original filename.
- Store in `private_uploads/` outside the web root.
- Serve only via authenticated route with ownership check and `Content-Disposition: inline`, `X-Content-Type-Options: nosniff`.
- Limit image dimensions (e.g. max 4000×4000) to avoid decompression bombs.

## Data Protection
- Database file outside static; not committed.
- Per-user data only; no public listing endpoints.
- "Delete my report" removes the DB row and the image file.
- "Delete my account" removes all the user's rows and files.
- Minimise data: only name, age, place, image, result.
- Backups (if any) encrypted and access-restricted.

## Transport & Headers
- HTTPS only in production, HSTS enabled.
- Headers on all responses:
  - `Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; frame-ancestors 'none'`
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `Referrer-Policy: no-referrer`
  - `Cache-Control: no-store` on report and dashboard pages (prevents back-button viewing after logout)

## Input Validation
- Name: letters, spaces, `.`, `-`, `'` only, 2–80 chars.
- Age: integer 0–100.
- Place: 2–80 chars, no control characters.
- Email: valid format, lowercase, unique.
- SQL: parameterised queries only.
- XSS: Jinja auto-escape; no `|safe`.

## Secrets
- `SECRET_KEY` from `.env` (long random value). Never committed.
- No secrets in client-side code or templates.

## Logging
- Log events (login failure, upload rejected) with user ID only.
- Never log passwords, names, ages, places, images or full emails.

## Errors
- Custom 403/404/413/500 pages. No stack traces or debug mode in production (`DEBUG=False`).

## Dependencies
- Pin versions in `requirements.txt`. Run `pip-audit` before release.

## Pre-release Security Checklist
- [ ] User A cannot open User B's report URL (gets 404)
- [ ] User A cannot fetch User B's image URL
- [ ] Logged-out user redirected from every private route
- [ ] CSRF missing → request rejected
- [ ] Non-image file renamed to .jpg is rejected
- [ ] File over 5 MB rejected
- [ ] No secrets in Git history
- [ ] DEBUG off, HTTPS on
- [ ] Security headers present
- [ ] Back button after logout shows no data
