# Findings

## Research
- The AI Rundown newsletter scraping is the first prototype focus.

## Discoveries & Constraints
### Discovery Answers
1. **North Star:** Build a beautiful interactive dashboard aggregating latest articles (<24h) from Hypebot, Water & Music, artist growth platforms, AI Rundown, and Reddit.
2. **Integrations:** Web Scraping (initial), Supabase (future database).
3. **Source of Truth:** Initially within the website (local storage/memory), eventually Supabase.
4. **Delivery Payload:** Runs every 24 hours. Presents new articles. Includes functionality to save articles (persisting on refresh).
5. **Behavioral Rules:** The design must feature gorgeous art aesthetics.
