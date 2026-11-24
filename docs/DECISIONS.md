# Architecture Decisions

## ADR-001
**Decision:** Use Flask with Jinja templates, plain HTML and CSS.
**Reason:** Requested stack (HTML, CSS, Python). Simple, easy to explain in a project review, no build tools.

## ADR-002
**Decision:** Model is separate; frontend calls `predict()` stub.
**Reason:** Project scope is frontend only. A stable contract lets the trained model be dropped in later.

## ADR-003
**Decision:** SQLite for storage.
**Reason:** Zero setup, adequate for a project demo. Can migrate to PostgreSQL later.

## ADR-004
**Decision:** Store uploads outside `static/` and serve through an authenticated route.
**Reason:** Prevents anyone with a URL from viewing another person's medical image.

## ADR-005
**Decision:** Return 404 instead of 403 for other users' records.
**Reason:** Does not reveal that a record exists.

## ADR-006
**Decision:** Teal–blue palette with one restrained gradient; flat green/red for results.
**Reason:** Matches clinical environment; avoids decorative gradients that reduce trust.

## ADR-007
**Decision:** Use UUIDs for report IDs.
**Reason:** Sequential IDs are guessable.

## ADR-008
**Decision:** Re-encode every uploaded image with Pillow.
**Reason:** Strips EXIF/GPS and hidden payloads.
