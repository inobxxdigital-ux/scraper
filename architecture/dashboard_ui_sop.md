# Layer 1: SOP - Dashboard UI & UX

## Objective
To provide a gorgeous, deterministic visual interface rendering the local `.tmp/ai_rundown_articles.json` feed into an interactive, art-focused aesthetic.

## Assets Location
- `index.html` (DOM Structure)
- `style.css` (Glassmorphism & Brand Theme parameters)
- `app.js` (DOM injection logic & State)
- `Designguideline/` (Logo & Brand directives)

## Processing Rules
1. The DOM must fail gracefully if `ai_rundown_articles.json` is missing or corrupted. 
2. Local Storage (`localStorage`) is the singular source of truth for "Saved Reports" until Supabase is activated.
3. No hardcoded data in HTML. All data rendering strictly operates via `app.js`.

## Known Constraints / Edge Cases
- **Refresh State:** Force-refresh currently relies on the user pressing the button to invoke a new fetch from `.tmp/`.
- **CORS Issues:** Loading local JSON via `fetch()` without a server will cause CORS errors on some browsers. A local python server (`python -m http.server 8000`) is mandatory during local testing.
