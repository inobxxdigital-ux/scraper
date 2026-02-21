# Artist Intelligence Scraper & Dashboard

A professional A.N.T. (Auto-Navigated Tools) pipeline for scraping and visualizing music industry intelligence.

## Features
- **Live Scrapers**: Fetches real-time data from Music Business Worldwide (Analysis), Hypebot (Industry News), and specialized Reddit communities (Artisr Development, Music Marketing, etc.).
- **Categorized Feed**: Smart filtering by Analysis, News, and Community.
- **Supabase Integration**: Centralized cloud database for persistent storage.
- **Modern Dashboard**: High-end glassmorphism UI with responsive design.
- **Auto-Mix Engine**: Interleaves sources using staggered timestamps for a dynamic feed experience.

## Tech Stack
- **Python**: Scraper logic and orchestration (`BeautifulSoup`, `requests`).
- **Supabase**: Cloud backend and REST API.
- **Vanilla JS/HTML/CSS**: Frontend dashboard with premium aesthetics.

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/inobxxdigital-ux/scraper.git
   ```

2. **Setup Environment**:
   Create a `.env` file in the root directory with:
   ```env
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_anon_key
   ```

3. **Install Dependencies**:
   ```bash
   pip install requests beautifulsoup4 python-dotenv
   ```

4. **Run the Pipeline**:
   ```bash
   python navigation.py
   ```

5. **View Dashboard**:
   Open `index.html` in your browser (preferably via a local server like `python -m http.server 8000`).

## Architecture
This project follows the **B.L.A.S.T.** protocol for reliable data ingestion and the **A.N.T.** 3-layer architecture:
1. **Layer 1 (Interaction)**: `index.html` / `app.js`
2. **Layer 2 (Navigation)**: `navigation.py`
3. **Layer 3 (Tools)**: `tools/ai_rundown_scraper.py`, `tools/supabase_uploader.py`

---
Developed by System Pilot.
