import json
import os
import random
import datetime
from jinja2 import Environment, FileSystemLoader

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
# SRC_DATA_DIR REMOVED - using DATA_DIR
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, 'templates')
DOCS_DIR = os.path.join(PROJECT_ROOT, 'docs')

# --- Helper Functions ---

def load_json(path):
    if not os.path.exists(path):
        print(f"WARNING: {path} not found.")
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_countries():
    # Load the new Senior SSOT Structure
    # world_data.json is Key=ISO, Val={Data}
    data_path = os.path.join(DATA_DIR, 'world_data.json')
    if not os.path.exists(data_path):
        print("ERROR: world_data.json missing.")
        return []
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    # Convert Dict (ISO -> Data) to List for iteration
    # Inject ISO code into the object
    countries_list = []
    for iso, info in data.items():
        # Inject code if not present (though it might be)
        info['code'] = iso.upper()
        countries_list.append(info)
        
    return countries_list

def calculate_discount(price, provider_name):
    """Calculates discounted price based on provider rules."""
    p_lower = provider_name.lower()
    if 'airalo' in p_lower:
        return price * 0.85
    if 'yesim' in p_lower:
        return price * 0.80
    return None

def generate_dummy_plans(country_slug, provider):
    """Generates realistic dummy plans for non-Airalo providers."""
    plans = []
    
    # 2. Add 2GB size -> Fixed for Fair Comparison
    sizes = [
        {"gb": 1, "days": 7, "base": 4.5},
        {"gb": 2, "days": 15, "base": 6.5}, 
        {"gb": 3, "days": 30, "base": 9.0},
        {"gb": 5, "days": 30, "base": 13.0},
        {"gb": 10, "days": 30, "base": 22.0},
        {"gb": 20, "days": 30, "base": 34.0},
        {"gb": -1, "days": 10, "base": 35.0} # Unlimited
    ]
    
    # Provider-specific price modifiers
    modifier = 1.0
    name = provider['name']
    if name == 'Maya Mobile': modifier = 0.95
    if name == 'Saily': modifier = 0.98
    if name == 'Klook': modifier = 0.90
    
    link_template = provider.get('affiliate_link', '#')
    
    for s in sizes:
        # small random variation
        variance = random.uniform(0.95, 1.05)
        price = round(s['base'] * modifier * variance, 2)
        
        link = link_template.replace('{country_slug}', country_slug)
        
        plans.append({
            "provider": name,
            "data_gb": float(s['gb']),
            "days": s['days'],
            "price": price,
            "link": link,
            "is_popular": False
        })
        
    return plans

def get_grouped_plans(country_code, country_slug, all_airalo_plans, providers):
    """
    Groups plans by data size for the template.
    Returns: list of group objects
    """
    # 1. Get Real Airalo Plans for this country
    country_plans = [p for p in all_airalo_plans if p['country_iso'].upper() == country_code.upper()]
    if country_code in ['PT', 'AU', 'US']:
        print(f"DEBUG: Found {len(country_plans)} Airalo plans for {country_code}")
        if not country_plans:
            print(f"DEBUG: Sample Airalo ISOs: {[p['country_iso'] for p in all_airalo_plans[:5]]}")
    
    # 2. Get Dummy Plans for others
    for prov in providers:
        p_name = prov['name']
        if p_name == 'Airalo': continue
        
        # 3. Drimsim Logic: Real Data Only (skip dummy generation)
        if p_name == 'Drimsim': continue 
        
        country_plans.extend(generate_dummy_plans(country_slug, prov))
        
    # 3. Group by Data Size
    sizes = sorted(list(set(p['data_gb'] for p in country_plans)))
    
    # Custom Sort for Sizes: 1, 2, 3... -1 (Unlimited) last
    def size_sorter(s):
        if s == -1: return 999999 # Unlimited at end
        return s
    sizes.sort(key=size_sorter)
    
    grouped_sections = []
    
    for size in sizes:
        if size == 0: continue
        
        # Title
        if size == -1:
            title = "Unlimited Data Plans"
            filter_val = -1
        else:
            if size.is_integer():
                title = f"{int(size)}GB Plans"
            else:
                 title = f"{size}GB Plans"
            filter_val = size
            
        # Group raw plans for this size by provider
        # to find the "Best Match" for each provider card
        
        section_plans = [] 
        
        # Map: Provider Name -> List of Plans for this size
        plans_for_size_by_prov = {}
        
        # Filter all plans to just this size first
        relevant_plans = [p for p in country_plans if abs(p['data_gb'] - size) < 0.1]
        
        for p in relevant_plans:
            p_name = p['provider'].strip()
            if p_name not in plans_for_size_by_prov: 
                plans_for_size_by_prov[p_name] = []
            plans_for_size_by_prov[p_name].append(p)
            
        # Now Key: We need to render ONE card per Provider that has plans in this size.
        # We also need the "All Plans" JSON for the dropdown/toggle (if implemented).
        # We'll use the FULL `country_plans` for the JSON payload, filtered by provider.
        
        # Full Plan Map for JSON payload
        all_plans_by_prov = {}
        for p in country_plans:
             p_name = p['provider']
             if p_name not in all_plans_by_prov: all_plans_by_prov[p_name] = []
             all_plans_by_prov[p_name].append({
                "data": p['data_gb'],
                "day": p['days'],
                "price": p['price'],
                "link": p['link']
             })
             
        # Sort each provider's plan list by price to ensure JS .find() picks the cheapest
        for p_name in all_plans_by_prov:
            all_plans_by_prov[p_name].sort(key=lambda x: x['price'])


        # Iterate Config Providers to create cards (if they have relevant plans)
        for prov_conf in providers:
            p_name = prov_conf['name']
            
            # Do we have plans for this size?
            prov_plans_for_size = plans_for_size_by_prov.get(p_name, [])
            
            if prov_plans_for_size:
                # Find the representative plan (Cheapest for this size)
                prov_plans_for_size.sort(key=lambda x: x['price'])
                best_match = prov_plans_for_size[0]
                
                discounted = calculate_discount(best_match['price'], p_name)
                final_price = discounted if discounted else best_match['price']
                
                # Logo Logic
                logo_filename = f"static/logos/{p_name.lower().replace(' ', '_').replace('.', '')}.png"
                if 'maya' in p_name.lower(): logo_filename = "static/logos/maya_mobile.png"
                if 'airalo' in p_name.lower(): logo_filename = "static/logos/airalo.png"
                if 'yesim' in p_name.lower(): logo_filename = "static/logos/yesim.png"
                if 'saily' in p_name.lower(): logo_filename = "static/logos/saily.png"
                if 'klook' in p_name.lower(): logo_filename = "static/logos/klook.png"
                if 'drimsim' in p_name.lower(): logo_filename = "static/logos/drimsim.png"
                
                # JSON payload for this provider
                json_payload = json.dumps(all_plans_by_prov.get(p_name, []))
                
                card_model = {
                    "name": p_name,
                    "json_data": json_payload,
                    "duration": best_match['days'],
                    "price": best_match['price'],
                    "discounted_price": discounted,
                    "logo_url": logo_filename,
                    "rating": prov_conf.get('base_rating', 4.5),
                    "benefits": prov_conf.get('benefits', []),
                    "coupons": prov_conf.get('coupons'),
                    "link": best_match['link'],
                    "sort_price": final_price
                }
                
                section_plans.append(card_model)
        
        # 1. Fix Sorting (Price Priority)
        # Sort cards strictly by effective price
        section_plans.sort(key=lambda x: x['sort_price'])
        
        if section_plans:
            grouped_sections.append({
                "title": title,
                "filter_value": filter_val,
                "plans": section_plans
            })
            
    return grouped_sections

def main():
    print("--- STARTING GENERATOR (SENIOR MODE: SSOT) ---")
    
    # 4. Folder Structure: Load from world_data.json via helper
    master_countries = load_countries()
    
    if not master_countries:
         print(f"ERROR: Could not load countries from world_data.json")
         return

    # Load Plan Data (Project Data Root)
    airalo_plans = load_json(os.path.join(DATA_DIR, 'data_plans.json'))
    providers_config = load_json(os.path.join(DATA_DIR, 'providers.json'))
    
    print(f"Loaded {len(master_countries)} countries, {len(airalo_plans)} Airalo plans, {len(providers_config)} providers.")
    
    # Setup Jinja2
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    
    template = env.get_template('country.html')
    
    # Generation Loop
    count = 0
    for country in master_countries:
        try:
            slug = country['slug']
            code = country['code']
            
            # Prepare Data
            grouped_plans = get_grouped_plans(code, slug, airalo_plans, providers_config)
            
            # SEO Variables
            current_year = datetime.datetime.now().year
            
            # Render
            output_html = template.render(
                country=country,
                grouped_plans=grouped_plans,
                current_year=current_year
            )
            
            # Save
            filename = f"{slug}.html"
            filepath = os.path.join(DOCS_DIR, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(output_html)
                
            count += 1
            if count % 10 == 0:
                print(f"Generated {count} pages...")
                
        except Exception as e:
            print(f"ERROR generating {country.get('name')}: {e}")
            
    print(f"--- GENERATION COMPLETE. {count} FILES CREATED. ---")

    # Generate Index Page (SSOT-Driven)
    try:
        index_template = env.get_template('index.html')
        index_str = index_template.render(countries=master_countries)
        index_path = os.path.join(DOCS_DIR, 'index.html')
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_str)
        print("Generated index.html with SSOT data.")
    except Exception as e:
        print(f"ERROR generating index.html: {e}")
    
    # SYSTEM UPGRADE: Sync Backend SSOT -> Frontend JSON
    # The frontend (index.html, search) relies on 'countries.json' in the same directory (docs/)
    # We must update it to include all the new countries we just generated.
    frontend_json_path = os.path.join(DOCS_DIR, 'countries.json')
    with open(frontend_json_path, 'w', encoding='utf-8') as f:
        json.dump(master_countries, f, indent=2)
        
    print(f"SYNC COMPLETE: Updated frontend docs/countries.json with {len(master_countries)} countries.")

if __name__ == '__main__':
    main()
