import json
import os
import shutil
from src.fetch_real_data import parse_yesim, parse_saily, PROVIDERS_CONFIG, random_sleep
from DrissionPage import ChromiumPage

# Configuration for the Patch
OUTPUT_FILE = 'data/external_providers.json'
BACKUP_FILE = 'data/external_providers_backup.json'

# The specific list of fixes
# Format: "internal_slug": { "provider": "slug_override" }
TARGETS = {
    "usa": {
        "yesim": "united-states", 
        "saily": "united-states"
    },
    "cote-divoire": {
        "saily": "cote-d-ivoire"
    },
    "dr-congo": {
        "saily": "democratic-republic-of-congo"
    },
    "republic-of-the-congo": {
        "yesim": "congo",
        "saily": "republic-of-the-congo"
    },
    "northern-cyprus": {
         # User said "really dont support", but let's double check if we can skipping or if there is a slug.
         # User reported: "really dont support" -> So we might SKIP this if confirmed.
         # But in the request they just listed it. Let's assume user wants to try if I found a slug? 
         # User said "really dont support" so I will SKIP it to save time, unless I have a better slug.
         # Actually user listed 8 countries. Let's stick to the ones with urls provided or mentioned "has plans".
         # User provided links for: USA, Cote, DR Congo, Rep Congo, Timor, Reunion, St Vincent, Macedonia.
    },
    "timor-leste": {
        "saily": "east-timor"
    },
    "reunion": {
        "yesim": "reunion-islands"
    },
    "saint-vincent-and-the-grenadines": {
        "saily": "saint-vincent-and-grenadines"
    },
    "north-macedonia": {
        "saily": "macedonia"
    }
}

def run_patch():
    print("--- STARTING QUICK PATCH ---")
    
    # 1. Backup Existing Data
    if os.path.exists(OUTPUT_FILE):
        shutil.copy(OUTPUT_FILE, BACKUP_FILE)
        print(f"[OK] Backed up data to {BACKUP_FILE}")
    else:
        print("[FAIL] Original data file not found! stopping.")
        return

    # 2. Load Data
    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        all_data = json.load(f)

    # 3. Initialize Browser
    page = ChromiumPage()
    
    try:
        for internal_slug, overrides in TARGETS.items():
            if not overrides: continue
            
            print(f"\n--- Patching {internal_slug} ---")
            
            # Ensure country entry exists
            if internal_slug not in all_data:
                all_data[internal_slug] = {"yesim": [], "saily": []}
            
            for provider_key, url_slug in overrides.items():
                provider_name = "Yesim" if provider_key == "yesim" else "Saily"
                template = PROVIDERS_CONFIG[provider_key]["url_template"]
                
                # Construct URL with OVERRIDE slug
                url = template.format(url_slug)
                print(f"   [{provider_name}] Fetching: {url}")
                
                try:
                    page.get(url)
                    random_sleep(3, 5)
                    page.scroll.down(600)
                    random_sleep(1, 2)
                    
                    plans = []
                    if provider_key == "yesim":
                        plans = parse_yesim(page)
                    else:
                        plans = parse_saily(page)
                    
                    if plans:
                        all_data[internal_slug][provider_key] = plans
                        print(f"      [OK] Updated {len(plans)} plans.")
                    else:
                        print(f"      [WARN] No plans found (Page might be empty).")

                except Exception as e:
                    print(f"      [ERR] Error processing {provider_name}: {e}")

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
    finally:
        print("\n--- SAVING PATCHED DATA ---")
        try:
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, indent=2)
            print(f"[OK] Successfully saved patched data to {OUTPUT_FILE}")
        except Exception as e:
            print(f"[ERR] Failed to save: {e}")
        
        # page.quit()

if __name__ == "__main__":
    run_patch()
