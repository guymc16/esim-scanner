import os
import requests
import json
import time

# Target Directory
img_dir = "docs/static/countries" 
os.makedirs(img_dir, exist_ok=True)

# Headers to behave like a browser and avoid 403s
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.google.com/'
}

def download_file(url, filepath):
    """Attempt to download a file from a URL to a path."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        if r.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(r.content)
            return True, f"Success ({len(r.content)} bytes)"
        else:
            return False, f"Status {r.status_code}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_fallback_url(slug, name):
    """Generate a fallback URL using LoremFlickr."""
    keywords = f"{name},travel,landscape,landmark"
    return f"https://loremflickr.com/800/600/{keywords}/all"

def main():
    # Load countries
    try:
        with open("data/countries.json", "r", encoding="utf-8") as f:
            countries = json.load(f)
    except FileNotFoundError:
        print("Error: data/countries.json not found.")
        return

    print(f"--- Starting Download for {len(countries)} Countries ---")
    
    success_count = 0
    skip_count = 0
    fail_count = 0

    for country in countries:
        name = country.get("name")
        slug = country.get("slug")
        primary_url = country.get("image_source_url") # Updated Field Name
        
        if not slug:
            continue

        filename = f"{slug}.jpg"
        filepath = os.path.join(img_dir, filename)

        # 1. Check if valid file exists
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            if size > 1000 and size != 148074: # Skip if valid and NOT a placeholder
                print(f"[SKIP] {name} - Image exists and is valid.")
                skip_count += 1
                continue
            else:
                 print(f"[RETRY] {name} - Image is broken or placeholder ({size} bytes). Redownloading...")

        # 2. Try Primary URL (Unsplash / Wikimedia)
        downloaded = False
        if primary_url and primary_url.startswith("http"):
            print(f"[DOWNLOADING] {name} from Source...")
            success, msg = download_file(primary_url, filepath)
            
            # Verify result wasn't a placeholder (some sources redirect to one)
            if success and os.path.getsize(filepath) == 148074:
                success = False
                msg = "Redirected to Placeholder"
                
            if success:
                print(f"   -> {msg}")
                downloaded = True
                success_count += 1
            else:
                print(f"   -> Primary failed: {msg}")

        # 3. Fallback: Generic Search
        if not downloaded:
            print(f"[FALLBACK] {name} - Trying generative source...")
            # Try 1: Just Name (Better for specific countries)
            fallback_url = f"https://loremflickr.com/800/600/{name.replace(' ','-')}/all"
            success, msg = download_file(fallback_url, filepath)
            
            # Check for placeholder
            if success and os.path.getsize(filepath) == 148074:
                print(f"   -> Got placeholder for '{name}', trying 'travel' tag...")
                # Try 2: Travel (+ Name)
                fallback_url = f"https://loremflickr.com/800/600/travel,{name.replace(' ','-')}/all"
                success, msg = download_file(fallback_url, filepath)
                
                 # Check placeholder again
                if success and os.path.getsize(filepath) == 148074:
                     print(f"   -> Still placeholder. Giving up on specific image.")
                     # Last Resort: Just "Nature" (Guaranteed image, though generic)
                     fallback_url = f"https://loremflickr.com/800/600/nature/all"
                     success, msg = download_file(fallback_url, filepath)

            if success:
                print(f"   -> {msg}")
                success_count += 1
            else:
                print(f"   -> Fallback failed: {msg}")
                fail_count += 1

        # Be nice to servers
        time.sleep(0.5)

    print("\n--- Summary ---")
    print(f"Skipped (Already Existed): {skip_count}")
    print(f"Downloaded (New/Fixed): {success_count}")
    print(f"Failed: {fail_count}")

if __name__ == "__main__":
    main()
