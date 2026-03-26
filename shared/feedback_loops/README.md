# Feedback Loops

These files make the first-pass cross-family and intra-family feedback structure explicit.
They are intentionally coarse enough to stay reusable, but specific enough to prevent
silent loop drift.

Conventions:
- `node` names a pipeline, authority, or family.
- `trigger` names the condition that moves control.
- `response` names the next node or smallest sufficient intervention.
- `purpose` names why the loop exists.
