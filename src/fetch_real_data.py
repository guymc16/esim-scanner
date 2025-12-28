from DrissionPage import ChromiumPage
import time
import random
import re
import os
import json

# --- CONFIGURATION ---
PROVIDERS_CONFIG = {
    "yesim": {
        "url_template": "https://yesim.app/country/{}", 
        "card_selector": "*[class*='PlanPlate']", 
        "provider_name": "Yesim"
    },
    "saily": {
        "url_template": "https://saily.com/esim-{}",
        "provider_name": "Saily"
    }
}

# Specific overrides for countries where internal slug != provider slug
SLUG_EXCEPTIONS = {
    "yesim": {
        "usa": "united-states",
        "republic-of-the-congo": "congo",
        "reunion": "reunion-islands"
    },
    "saily": {
        "usa": "united-states",
        "cote-divoire": "cote-d-ivoire",
        "dr-congo": "democratic-republic-of-congo",
        "republic-of-the-congo": "republic-of-the-congo",
        "timor-leste": "east-timor",
        "saint-vincent-and-the-grenadines": "saint-vincent-and-grenadines",
        "north-macedonia": "macedonia"
    }
}



TEST_COUNTRIES = ['japan', 'united-states', 'israel']

def random_sleep(min_sec=2, max_sec=5):
    """Sleeps for a random anti-detect interval."""
    time.sleep(random.uniform(min_sec, max_sec))




def parse_yesim(page):
    plans = []
    print("   [Yesim] Scanning for plans (Card Integrity Mode)...")
    seen_plans_for_country = set() # Deduplication set
    
    try:
        # Strategy: Find Price -> Walk Up -> Check if parent has Data info
        # This guarantees the Price belongs to the Data.
        
        # 1. Find all potential price elements
        candidates = page.eles("@@class:f20-bold")
        
        seen_cards = set()
        
        for price_ele in candidates:
            if "$" not in price_ele.text: continue
            
            # Walk up to 3 levels to find the card container
            current = price_ele
            card_found = None
            
            for _ in range(4): # Check parent, grand-parent, great-grand...
                parent = current.parent()
                if not parent: break
                
                p_text = parent.text.replace("\n", " ")
                
                # Check if this parent has "GB" or "Day" stats
                if ("GB" in p_text or "Unlimited" in p_text) and "day" in p_text.lower():
                    card_found = parent
                    break
                current = parent
            
            if card_found:
                # Deduplicate by text content (HTML Card integrity)
                full_text = card_found.text.replace("\n", " ").strip()
                if full_text in seen_cards: continue
                seen_cards.add(full_text)
                
                # DEBUG: Uncomment to see card text
                # print(f"      [DEBUG] Yesim Card: '{full_text}'")
                
                # Now Parse THIS SPECIFIC CARD
                # Days
                days = 0
                days_match = re.search(r"(\d+)\s?days?", full_text, re.IGNORECASE)
                if days_match: days = int(days_match.group(1))
                
                # GB
                gb = 0
                if "∞" in full_text or "Unlimited" in full_text:
                    gb = 9999
                else:
                    gb_match = re.search(r"(\d+)\s?GB", full_text, re.IGNORECASE)
                    if gb_match: gb = int(gb_match.group(1))
                    else:
                        mb_match = re.search(r"(\d+)\s?MB", full_text, re.IGNORECASE)
                        if mb_match: gb = float(mb_match.group(1)) / 1000.0

                # Price Extraction (Advanced)
                # Issue: Yesim shows "$20.40" AND "$2.04 / GB". We want $20.40.
                
                price = 0.0 # Initialize variable
                valid_prices = []
                iter_prices = re.finditer(r"\$\s?(\d+[\.,]?\d*)", full_text)
                
                for match in iter_prices:
                    val_str = match.group(1)
                    end_idx = match.end()
                    
                    # Strict Lookahead: Check immediate context
                    # We slice the next 20 chars
                    context = full_text[end_idx:end_idx+20].strip().lower()
                    
                    # If it STARTS with '/' or 'per', it is a unit price.
                    # Example 1: "$2.04 / GB" -> context starts with "/" -> SKIP
                    # Example 2: "$20.40 $2.04" -> context starts with "$2.04..." -> KEEP
                    
                    if context.startswith('/') or context.startswith('per'):
                        continue
                        
                    raw = float(val_str.replace(",", ""))
                    
                    # Normalize cents (if > 100, likely cents)
                    if raw > 100: 
                        norm = raw / 100.0 
                    # Handle "$054" case (Superscript cents starting with 0, no dot)
                    elif val_str.startswith('0') and '.' not in val_str and raw > 0:
                        norm = raw / 100.0
                    else: 
                        norm = raw
                        
                    # Sanity Check: Price ghost killer
                    # e.g. 15 Days cannot be $1.26 (Old Price artifact $126)
                    # Increased threshold to $0.10/day to catch the $1.26 case (1.26/15 = 0.08)
                    if days > 0 and norm < (0.10 * days):
                         continue
                    
                    valid_prices.append(norm)
                
                if valid_prices: 
                    price = min(valid_prices) # Capture the Sale Price
                
                if days > 0 and gb > 0 and price > 0:
                    # Deduplication Check (Logical Plan Integrity)
                    plan_key = (gb, days)
                    if plan_key not in seen_plans_for_country:
                        seen_plans_for_country.add(plan_key)
                        
                        p_data = {"data_gb": gb, "days": days, "price": round(price, 2), "provider": "Yesim"}
                        plans.append(p_data)
                        print(f"      [OK] Verified Card: {gb}GB | {days} Days | ${p_data['price']}")
                    
    except Exception as e:
        print(f"   [Yesim Loop Error] {e}")
            
    return plans

def parse_saily(page):
    plans = []
    print("   [Saily] Scanning for plans (Deep Scan)...")
    seen_plans_for_country = set() # Deduplication

    try:
        # Broad scan of all text-containing elements with "GB"
        candidates = page.eles('text:GB')
        seen_texts = set()
        
        for cand in candidates:
            # Go up to finding the card
            current = cand
            card_found = None
            
            for _ in range(5):
                parent = current.parent()
                if not parent: break
                txt = parent.text.replace("\n", " ")
                if "days" in txt.lower() and "US$" in txt:
                    card_found = parent
                    break 
                current = parent
            
            if card_found:
                 full_text = card_found.text.replace("\n", " ").strip()
                 
                 # 0. Length Guard (Ghosts often come from grabbing big containers)
                 if len(full_text) > 350:
                     continue
                     
                 # 1. footer Guard
                 if "activation period" in full_text.lower():
                     continue

                 if full_text in seen_texts: continue
                 seen_texts.add(full_text)
                 
                 # DEBUG: Uncomment to see what text we are parsing
                 # print(f"      [DEBUG] Raw Card Text: '{full_text}'")
                 
                 # Parse GB
                 gb = 0
                 
                 # 1. Try to find explicit GB number first (Prioritize "1 GB" over "Unlimited")
                 gb_match = re.search(r"(\d+)\s?GB", full_text, re.IGNORECASE)
                 if gb_match:
                     gb = int(gb_match.group(1))
                 
                 # 2. If NO number found, check for "Unlimited"
                 if gb == 0 and "Unlimited" in full_text:
                     gb = 9999
                 
                 # Parse Days
                 days = 0
                 days_match = re.search(r"(\d+)\s?days?", full_text, re.IGNORECASE)
                 if days_match:
                     days = int(days_match.group(1))

                 all_prices = re.findall(r"US\$(\d+\.\d+)", full_text)
                 real_price = 0.0
                 if all_prices: real_price = min([float(p) for p in all_prices])
                 
                 if gb > 0 and days > 0 and real_price > 0:
                     plan_key = (gb, days)
                     if plan_key not in seen_plans_for_country:
                         seen_plans_for_country.add(plan_key)
                         
                         p_data = {
                            "data_gb": gb,
                            "days": days, 
                            "price": real_price, 
                            "provider": "Saily"
                         }
                         plans.append(p_data)
                         print(f"      [OK] Validated Card: {p_data['data_gb']}GB | {p_data['days']} Days | ${p_data['price']}")

    except Exception as e:
        print(f"   [Saily Error] {e}")
            
    return plans

def load_countries():
    """Loads country slugs from world_data.json"""
    try:
        with open('data/world_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Return list of slugs (e.g. 'japan', 'united-states')
            return [info['slug'] for info in data.values()]
    except Exception as e:
        print(f"Error loading world_data.json: {e}")
        return []

def fetch_data(mode='test'):
    page = ChromiumPage()
    
    # Decide which countries to scrape
    if mode == 'all':
        print("--- [GLOBAL MODE] RUNNING IN FULL GLOBAL MODE (ALL COUNTRIES) ---")
        countries = load_countries()
        if not countries:
            print("Failed to load countries. Exiting.")
            return
    else:
        print("--- [TEST MODE] RUNNING IN TEST MODE (3 COUNTRIES) ---")
        countries = TEST_COUNTRIES
        
    # Load Existing Data to Merge (Permanent Feature)
    output_file = 'data/external_providers.json'
    all_data = {}
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                all_data = json.load(f)
            print(f"[OK] Loaded existing data for {len(all_data)} countries. (Merge Mode)")
        except:
            print("Warning: Could not load existing data, starting fresh.")
            all_data = {}
            
    # all_data = {} # Structure: { "japan": { "yesim": [...], "saily": [...] } }
    
    try:
        for country in countries:
            print(f"\n--- Harvesting {country.upper()} ---")
            country_plans = {"yesim": [], "saily": []}
            
            # YESIM
            try:
                # Check for override
                target_slug = SLUG_EXCEPTIONS["yesim"].get(country, country)
                
                url = PROVIDERS_CONFIG["yesim"]["url_template"].format(target_slug)
                print(f"[Yesim] Navigating: {url}")
                page.get(url)
                random_sleep(3, 5)
                page.scroll.down(600)
                random_sleep(1, 2)
                
                plans = parse_yesim(page)
                country_plans["yesim"] = plans
            except Exception as e:
                print(f"   [Yesim] Error: {e}")

            # SAILY
            try:
                # Check for override
                target_slug = SLUG_EXCEPTIONS["saily"].get(country, country)
                
                url = PROVIDERS_CONFIG["saily"]["url_template"].format(target_slug)
                print(f"[Saily] Navigating: {url}")
                page.get(url)
                random_sleep(3, 5)
                page.scroll.down(600)
                random_sleep(1, 2)
                
                plans = parse_saily(page)
                country_plans["saily"] = plans
            except Exception as e:
                 print(f"   [Saily] Error: {e}")
            
            # Save to memory
            all_data[country] = country_plans

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
            
    finally:
        print("\n--- HARVEST FINISHED ---")
        
        # Save to JSON
        output_file = 'data/external_providers.json'
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, indent=2)
            print(f"[OK] Data saved to {output_file}")
            print(f"Total Countries Scraped: {len(all_data)}")
        except Exception as e:
            print(f"[FAIL] Failed to save JSON: {e}")

        # page.quit() 

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['test', 'all'], default='test', help='Scrape mode')
    args = parser.parse_args()
    
    fetch_data(args.mode)
