import os
import json
import urllib.request
import urllib.parse
from dotenv import load_dotenv

# Layer 3 Tool: Cloud Transfer
# Responsible for uploading the .tmp/ai_rundown_articles.json payload to Supabase

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
TMP_FILE = os.path.join(PROJECT_ROOT, ".tmp", "ai_rundown_articles.json")
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")

load_dotenv(dotenv_path=ENV_PATH)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def upload_to_supabase():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Error: Missing Supabase credentials in .env")
        return

    if not os.path.exists(TMP_FILE):
        print(f"Error: Target payload not found at {TMP_FILE}")
        return

    with open(TMP_FILE, 'r', encoding='utf-8') as f:
        articles = json.load(f)

    if not articles:
        print("No articles to upload.")
        return

    # Supabase REST API endpoint for the 'articles' table
    endpoint = f"{SUPABASE_URL}/rest/v1/articles"
    
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates" # Upsert behavior
    }

    # Convert to JSON bytes
    data = json.dumps(articles).encode('utf-8')

    req = urllib.request.Request(endpoint, data=data, headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req) as response:
            if response.status in [200, 201]:
                print(f"Successfully uploaded/upserted {len(articles)} articles to Supabase.")
            else:
                print(f"Supabase API returned unexpected status: {response.status}")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        error_body = e.read().decode('utf-8')
        print(f"Response: {error_body}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    upload_to_supabase()
