# Test Plan

## Authentication
- [ ] User can register with valid details
- [ ] Duplicate email shows error
- [ ] Weak password shows error
- [ ] User can login / logout
- [ ] Wrong credentials show generic error
- [ ] Logged-out user cannot open /dashboard, /report/<id>, image route

## Scan Form
- [ ] Name, age, place required
- [ ] Age outside 0–120 rejected
- [ ] PNG accepted
- [ ] JPG / JPEG accepted
- [ ] GIF, PDF, SVG, EXE rejected
- [ ] Fake .jpg (text file renamed) rejected
- [ ] File over 5 MB rejected
- [ ] Preview shown before submit
- [ ] Loading state shown while analysing

## Results
- [ ] Status shows Anemia or Non-anemia
- [ ] Hb value shown with 1 decimal and g/dL
- [ ] "Demo result" label shown while predictor is placeholder
- [ ] Disclaimer visible

## Report / Print
- [ ] Report shows name, age, place, image, status, Hb, date, report ID
- [ ] Print preview hides buttons and navbar
- [ ] Readable in black and white
- [ ] Fits one A4 page

## History
- [ ] User sees only their own reports
- [ ] Delete asks for confirmation
- [ ] Deleted report and image are gone

## Access Control (critical)
- [ ] User A opening User B's report ID → 404
- [ ] User A requesting User B's image → 404
- [ ] Delete another user's report → 404

## Security
- [ ] CSRF token required on all forms
- [ ] Rate limit triggers after 5 failed logins
- [ ] Security headers present
- [ ] Session expires after idle timeout
- [ ] No cache after logout

## Responsive
- [ ] 375px, 768px, 1440px

## Accessibility
- [ ] Keyboard-only usage works
- [ ] Focus visible
- [ ] Contrast ≥ 4.5:1
- [ ] Status not conveyed by colour alone

## Commands
```
pytest
flake8 app
pip-audit
```
