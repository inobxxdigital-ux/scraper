# Project Constitution (gemini.md)

## Data Schemas
### Article Payload Schema (JSON)
```json
{
  "id": "string (uuid)",
  "source": "string (e.g., 'The AI Rundown', 'Hypebot')",
  "title": "string",
  "url": "string",
  "published_at": "string (ISO 8601 timestamp)",
  "summary": "string",
  "content": "string (optional full text or html)",
  "image_url": "string (optional)",
  "is_saved": "boolean (default: false)"
}
```

## Behavioral Rules
- Prioritize reliability over speed.
- Never guess at business logic.
- The Golden Rule: If logic changes, update SOP before updating code.
- Data-First Rule: Define JSON Data Schema before coding tools.
- Deliverables vs Intermediates: `.tmp/` is ephemeral, globals go to Cloud.
- Design Rule: Gorgeous art aesthetics.

## Architectural Invariants
- 3-Layer Architecture (A.N.T.):
  - Layer 1: Architecture (`architecture/`) - SOPs
  - Layer 2: Navigation - Reasoning layer
  - Layer 3: Tools (`tools/`) - Deterministic Python scripts

## Maintenance Log
(Pending Deployment)
