import json
import os

def analyze():
    # Load World Data
    try:
        with open('data/world_data.json', 'r', encoding='utf-8') as f:
            world_data = json.load(f)
    except FileNotFoundError:
        print("Error: data/world_data.json not found.")
        return

    # Load External Providers Data
    try:
        with open('data/external_providers.json', 'r', encoding='utf-8') as f:
            external_data = json.load(f)
    except FileNotFoundError:
        print("Error: data/external_providers.json not found.")
        return

    # --- Report 1: Missing Plans ---
    print("\n--- REPORT: MISSING PLANS PER COUNTRY ---")
    missing_report = []
    
    # world_data values are { "name": "...", "slug": "...", ... }
    # external_data keys are slugs (mostly).
    
    total_countries = 0
    countries_with_both = 0
    countries_missing_something = 0
    
    # Iterate through all target countries
    for iso, info in world_data.items():
        slug = info['slug']
        country_name = info['name']
        total_countries += 1
        
        # Handle US special case if needed (fetch_real might use 'united-states')
        # external_provider.json uses SLUGS as keys.
        
        plans = external_data.get(slug)
        
        status = []
        if not plans:
            status.append("MISSING ALL DATA")
        else:
            yesim_count = len(plans.get('yesim', []))
            saily_count = len(plans.get('saily', []))
            
            if yesim_count == 0:
                status.append("Missing Yesim")
            if saily_count == 0:
                status.append("Missing Saily")
                
        if status:
            countries_missing_something += 1
            missing_report.append(f"{country_name} ({slug}): {', '.join(status)}")
        else:
            countries_with_both += 1

    if not missing_report:
        print("All countries have plans from both providers!")
    else:
        print(f"Total Countries Checked: {total_countries}")
        print(f"Countries with Missing Data: {len(missing_report)}\n")
        # Print top 20 missing to avoid spamming usage, or print all if user wants?
        # User asked for "a report of all the country". I will print all but format nicely.
        for line in missing_report:
            print(line)

    # --- Report 2: Low Price Plans ---
    print("\n--- REPORT: LOW PRICE PLANS (<$1, >=500MB) ---")
    low_price_plans = []
    
    for slug, providers in external_data.items():
        for provider_name, provider_plans in providers.items():
            for plan in provider_plans:
                # plan keys: data_gb, days, price, provider
                price = plan.get('price', 0)
                gb = plan.get('data_gb', 0)
                
                # Check for < $1 and >= 0.5 GB
                if price < 1.0 and gb >= 0.5:
                    low_price_plans.append({
                        "country": slug,
                        "provider": provider_name,
                        "price": price,
                        "gb": gb,
                        "days": plan.get('days')
                    })

    if not low_price_plans:
        print("[OK] No plans found with Price < $1.00 and Data >= 500MB.")
        print("This indicates they were likely filtered out by the 'Ghost Killer' logic in fetch_real_data.py.")
    else:
        print(f"[WARN] Found {len(low_price_plans)} suspicion low-price plans:")
        for p in low_price_plans:
            print(f"   [{p['country']}] {p['provider']}: {p['gb']}GB for {p['days']} Days @ ${p['price']}")

if __name__ == "__main__":
    analyze()
