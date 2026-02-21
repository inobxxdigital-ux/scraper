# Layer 1: SOP - Feed Scraper Engine

## Objective
To consistently fetch the latest (<24h) news articles from predetermined sources and output them identically against the `Article Payload Schema`.

## Tool Location
`tools/ai_rundown_scraper.py`

## Inputs
- `None` directly required for invocation (runs statelessly).

## Processing Rules
1. Must not error if a source is momentarily down or changes layout; it should skip and log.
2. Output strictly JSON array to `.tmp/ai_rundown_articles.json`.
3. Adhere to Data Schema established in `gemini.md`.

## Output Expectations (The Payload)
```json
[
  {
      "id": "uuid",
      "source": "Source Name",
      "title": "String",
      ...
  }
]
```

## Known Constraints / Edge Cases
- **Dynamic CSS:** If the source site alters HTML structure, the script will default to an empty feed.
- **Dependencies:** Requires `beautifulsoup4` and `requests`. (Currently mocked via JSON to prevent dependency lockups during prototype phase).
