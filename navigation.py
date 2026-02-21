import subprocess
import os
import sys

# Layer 2: Routing / Navigation
# This script manages the decision logic, running the correct tools in the correct order.

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(PROJECT_ROOT, "tools")

def run_scraper():
    print("Layer 2 [Nav]: Routing execution to tools/ai_rundown_scraper.py...")
    scraper_path = os.path.join(TOOLS_DIR, "ai_rundown_scraper.py")
    
    try:
        result = subprocess.run(
            [sys.executable, scraper_path],
            check=True,
            capture_output=True,
            text=True
        )
        print("Success:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Scraper Execution Failed!")
        print(e.stderr)
        # Self-Annealing rule: Do not guess. Log and halt.
        sys.exit(1)

def run_uploader():
    print("Layer 2 [Nav]: Routing execution to tools/supabase_uploader.py...")
    uploader_path = os.path.join(TOOLS_DIR, "supabase_uploader.py")
    
    try:
        result = subprocess.run(
            [sys.executable, uploader_path],
            check=True,
            capture_output=True,
            text=True
        )
        print("Success:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Uploader Execution Failed!")
        print(e.stderr)
        sys.exit(1)

def main():
    print("--- System Pilot: Initiating A.N.T. Pipeline ---")
    
    # 1. Trigger the Scraper (Fetch new articles)
    run_scraper()
    
    # 2. Trigger the Uploader (Cloud Transfer)
    run_uploader()
    
    print("Layer 2 [Nav]: Pipeline Complete. Payload successfully synced to Supabase.")

if __name__ == "__main__":
    main()
