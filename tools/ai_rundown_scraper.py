import os
import json
import uuid
import requests
from bs4 import BeautifulSoup
from datetime import datetime

TMP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.tmp')
OUTPUT_FILE = os.path.join(TMP_DIR, 'ai_rundown_articles.json') # Same file to keep UI simple

def fetch_mbw(articles_list):
    print("Fetching live data from Music Business Worldwide...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    
    try:
        response = requests.get('https://musicbusinessworldwide.com/', headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Parse MBW homepage articles
        article_blocks = soup.select('article')
        
        valid_articles = 0
        for block in article_blocks:
            if valid_articles >= 5: break
            
            # MBW structure is a bit scattered, try finding headlines in h4 or looking for direct links
            title_el = block.select_one('h4 a') or block.select_one('h3 a') or block.select_one('h2 a')
            if not title_el:
                # Fallback to finding any prominent link that isn't an image
                links = block.select('a')
                for link in links:
                    if link.get_text(strip=True) and len(link.get_text(strip=True)) > 20: # Likely a title
                        title_el = link
                        break
                        
            if not title_el: continue
            
            title = title_el.get_text(strip=True)
            url = title_el.get('href', '')
            
            summary_el = block.select_one('p')
            summary = summary_el.get_text(strip=True) if summary_el else f"Daily analysis: {title}"
            if len(summary) > 200: summary = summary[:197] + "..."
            
            img_el = block.select_one('img')
            img_url = img_el.get('data-src') or img_el.get('src') if img_el else "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&q=80&w=1000"

            articles_list.append({
                "id": str(uuid.uuid4()),
                "source": "Music Business Worldwide",
                "title": title,
                "url": url,
                "published_at": datetime.now().isoformat(),
                "summary": summary,
                "content": "",
                "image_url": img_url,
                "is_saved": False,
                "category": "Analysis"
            })
            valid_articles += 1
            
    except Exception as e:
        print(f"Error fetching MBW: {e}")

def fetch_hypebot(articles_list):
    print("Fetching live data from Hypebot...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    
    try:
        response = requests.get('https://www.hypebot.com/', headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Parse Hypebot homepage articles
        article_blocks = soup.select('article')
        
        valid_articles = 0
        for block in article_blocks:
            if valid_articles >= 5: break
            
            title_el = block.select_one('.c-card__headline a') or block.select_one('h3 a') or block.select_one('h2 a') or block.select_one('h1 a')
            if not title_el: continue
            
            title = title_el.get_text(strip=True)
            url = title_el.get('href', '')
            if url and url.startswith('/'):
                url = f"https://www.hypebot.com{url}"
            
            summary_el = block.select_one('.c-card__excerpt') or block.select_one('p')
            summary = summary_el.get_text(strip=True) if summary_el else f"Music tech news: {title}"
            if len(summary) > 200: summary = summary[:197] + "..."
            
            img_el = block.select_one('img')
            img_url = img_el.get('src') if img_el else "https://images.unsplash.com/photo-1611162617474-5b21e879e113?auto=format&fit=crop&q=80&w=1000"

            articles_list.append({
                "id": str(uuid.uuid4()),
                "source": "Hypebot",
                "title": title,
                "url": url,
                "published_at": datetime.now().isoformat(),
                "summary": summary,
                "content": "",
                "image_url": img_url,
                "is_saved": False,
                "category": "News"
            })
            valid_articles += 1
    except Exception as e:
        print(f"Error fetching Hypebot: {e}")

def fetch_reddit(articles_list):
    print("Fetching live data from Reddit (Artist/Indie/Growth communities)...")
    # Added FreeSounds, Drumkits, and musicproduction for free beats and samples
    subreddits = "ArtistDevelopment+Songwriting+WeAreTheMusicMakers+musicmarketing+makinghiphop+AdvancedProduction+FreeSounds+Drumkits+musicproduction"
    # Fetching top 20 posts of the week
    url = f"https://www.reddit.com/r/{subreddits}/top.json?t=week&limit=20"
    
    headers = {
        'User-Agent': 'python:artist_dashboard_scraper:v1.1 (by /u/system_pilot)'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        posts = data.get('data', {}).get('children', [])
        
        valid_posts_added = 0
        
        # Keywords to filter out self-promotion and unhelpful content
        exclude_phrases = [
            "listen to my", "check out my", "my new song", "my latest release", 
            "my first track", "feedback on my", "what do you think of my", 
            "my ep", "my album", "stream my", "presave", "my new single",
            "check my beat", "roast my", "rate my"
        ]
        
        for post in posts:
            if valid_posts_added >= 10: # Cap at 10 reddit posts
                break
                
            post_data = post.get('data', {})
            title = post_data.get('title', '')
            selftext = post_data.get('selftext', '')
            
            # Combine title and text to check for unhelpful keywords
            full_text = (title + " " + selftext).lower()
            
            is_unhelpful = any(phrase in full_text for phrase in exclude_phrases)
            if is_unhelpful:
                continue # Skip self promo / unhelpful posts
                
            post_data = post.get('data', {})
            title = post_data.get('title', '')
            permalink = post_data.get('permalink', '')
            post_url = f"https://www.reddit.com{permalink}" if permalink else post_data.get('url', '')
            selftext = post_data.get('selftext', '')
            subreddit = post_data.get('subreddit_name_prefixed', '')
            score = post_data.get('score', 0)
            
            # Shorten summary
            summary = selftext[:150] + "..." if len(selftext) > 150 else selftext
            if not summary.strip():
                summary = f"Top discussion from {subreddit} with {score} upvotes."
            
            # Use Reddit Logo for image
            reddit_logo = "https://www.iconpacks.net/icons/2/free-reddit-logo-icon-2436-thumb.png"
            
            articles_list.append({
                "id": str(uuid.uuid4()),
                "source": f"Reddit ({subreddit})",
                "title": title,
                "url": post_url,
                "published_at": datetime.now().isoformat(),
                "summary": summary,
                "content": "",
                "image_url": reddit_logo,
                "is_saved": False,
                "category": "Community"
            })
            valid_posts_added += 1
            
    except Exception as e:
        print(f"Error fetching Reddit: {e}")

def fetch_latest_articles():
    import random
    os.makedirs(TMP_DIR, exist_ok=True)
    articles = []

    # Fetch from sources
    fetch_mbw(articles)
    fetch_hypebot(articles)
    fetch_reddit(articles)

    # Scramble them by slightly adjusting the published_at time so they interleave on the dashboard
    import random
    from datetime import timedelta
    
    base_time = datetime.now()
    random.shuffle(articles) # Shuffle list
    
    for i, article in enumerate(articles):
        # Subtract i minutes so the first in shuffled list is newest, second is 1 min older, etc.
        staggered_time = base_time - timedelta(minutes=i)
        article['published_at'] = staggered_time.isoformat()

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2)
        
    print(f"Successfully scraped {len(articles)} live industry/reddit articles and saved payload.")

if __name__ == "__main__":
    fetch_latest_articles()
