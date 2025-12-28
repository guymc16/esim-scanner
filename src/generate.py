import json
import os
import random
import datetime
from jinja2 import Environment, FileSystemLoader

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, 'templates')
DOCS_DIR = os.path.join(PROJECT_ROOT, 'docs')

KLOOK_WHITELIST = [
    'japan', 'south-korea', 'thailand', 'singapore', 'taiwan', 'hong-kong',
    'vietnam', 'malaysia', 'indonesia', 'philippines', 'china', 'india',
    'usa', 'united-kingdom', 'france', 'italy', 'spain', 'germany',
    'australia', 'new-zealand', 'turkey', 'united-arab-emirates'
]

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

def get_grouped_plans(country_code, country_slug, all_real_plans, providers):
    """
    Groups plans by data size for the template.
    Returns: list of group objects
    """
    # 1. Get Real Plans for this country (Airalo + Maya + Yesim + Saily)
    country_plans = [p for p in all_real_plans if p['country_iso'].upper() == country_code.upper()]
    
    # 3. Group by Data Size
    sizes = sorted(list(set(p['data_gb'] for p in country_plans)))
    
    # Custom Sort for Sizes: Unlimited (9999) last
    def size_sorter(s):
        if s > 1000: return 999999 # Unlimited at end
        return s
    sizes.sort(key=size_sorter)
    
    grouped_sections = []
    
    for size in sizes:
        if size == 0: continue
        
        # Title
        if size > 1000:
            title = "Unlimited Data Plans"
            filter_val = 9999
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
        


        # 2. Inject Klook Card (Static) if Country is Whitelisted
        # We add it to EVERY group so it shows up regardless of filter
        if country_slug in KLOOK_WHITELIST:
             # print(f"DEBUG: Process Klook for {country_slug}")
             # Find Klook config
             klook_conf = next((p for p in providers if 'Klook' in p['name']), None)
             if klook_conf:
                 # Construct Static Card
                 klook_link = klook_conf['affiliate_link'].replace('{country_slug}', country_slug)
                 klook_card = {
                    "name": "Klook",
                    "json_data": "[]", # No dynamic plans
                    "data_amount": "Various Plans",
                    "duration": "1-30 Days",
                    "price": "Check Price", # String display
                    "discounted_price": None,
                    "logo_url": "static/logos/klook.png",
                    "rating": klook_conf.get('base_rating', 4.6),
                    "benefits": klook_conf.get('benefits', []),
                    "coupons": None,
                    "link": klook_link,
                    "sort_price": 9999, # Force to bottom
                    "is_static": True
                 }
                 section_plans.append(klook_card)

        # 3. Sort again to ensure Klook is last
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
    all_plans = load_json(os.path.join(DATA_DIR, 'data_plans.json'))
    providers_config = load_json(os.path.join(DATA_DIR, 'providers.json'))
    
    # NORMALIZE UNLIMITED (-1 -> 9999)
    # This ensures consistent grouping if input data is mixed
    normalized_count = 0
    for p in all_plans:
        if p['data_gb'] == -1 or p['data_gb'] == -1.0:
            p['data_gb'] = 9999.0
            normalized_count += 1
            
    print(f"Loaded {len(master_countries)} countries, {len(all_plans)} Total plans (Normalized {normalized_count} Unlimiteds).")
    
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
            grouped_plans = get_grouped_plans(code, slug, all_plans, providers_config)
            
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
    
    # Generate Static Pages (About, Partners, Toolkit)
    # Load Tools Data
    tools_data = load_json(os.path.join(DATA_DIR, 'tools.json'))
    
    # Prepare Partners Data (Enrich providers with UI fields for Partner Page)
    partners_data = []
    for p in providers_config:
        # Defaults for UI
        badge = "Trusted Partner"
        badge_color = "blue"
        desc = f"Global connectivity provider with excellent coverage in {p.get('review_count', '10k')}+ reviews."
        
        # Custom Overrides based on name
        if "Airalo" in p['name']:
            badge = "Global Leader"
            badge_color = "blue"
            desc = "The world’s first and largest eSIM store. best for coverage and app experience."
        elif "Maya" in p['name']:
            badge = "Top Rated"
            badge_color = "green"
            desc = "Excellent 5G/4G speeds and unlimited data options. Great for power users."
        elif "Saily" in p['name']:
            badge = "Secure Choice"
            badge_color = "purple"
            desc = "Built by Nord Security. Focuses on privacy and secure global connections."
        elif "Yesim" in p['name']:
            badge = "Pay As You Go"
            badge_color = "yellow"
            desc = "Unique pay-as-you-go options and non-expiring data coins."
        elif "Drimsim" in p['name']:
            badge = "Global Roaming"
            badge_color = "orange"
            desc = "One SIM for the whole world. Real pay-per-mb business model."
        elif "Klook" in p['name']:
            badge = "Travel Bundles"
            badge_color = "red"
            desc = "Perfect for Asia travel. Combine eSIM with train tickets and tours."

        # Logo Logic (Reuse from above or simplified)
        logo_filename = f"static/logos/{p['name'].lower().replace(' ', '_').replace('.', '')}.png"
        if 'maya' in p['name'].lower(): logo_filename = "static/logos/maya_mobile.png"
        if 'airalo' in p['name'].lower(): logo_filename = "static/logos/airalo.png"
        if 'yesim' in p['name'].lower(): logo_filename = "static/logos/yesim.png"
        if 'saily' in p['name'].lower(): logo_filename = "static/logos/saily.png"
        if 'klook' in p['name'].lower(): logo_filename = "static/logos/klook.png"
        if 'drimsim' in p['name'].lower(): logo_filename = "static/logos/drimsim.png"

        partners_data.append({
            "name": p['name'],
            "local_logo": logo_filename,
            "badge": badge,
            "badge_color": badge_color,
            "description": desc,
            "link": p['affiliate_link'].replace('{country_slug}', 'global') # Fallback link
        })

    static_context = {
        "partners": partners_data,
        "tools": tools_data,
        "ecosystem": tools_data # Reuse tools for the ecosystem marquee
    }

    static_pages = ['about.html', 'partners.html', 'toolkit.html']
    for page in static_pages:
        try:
            tmpl = env.get_template(page)
            # Pass the full context
            output = tmpl.render(
                countries=master_countries, 
                current_year=datetime.datetime.now().year,
                **static_context
            )
            path = os.path.join(DOCS_DIR, page)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Generated {page} from template.")
        except Exception as e:
            print(f"WARNING: Could not generate {page}: {e}")
    
    # SYSTEM UPGRADE: Sync Backend SSOT -> Frontend JSON
    # The frontend (index.html, search) relies on 'countries.json' in the same directory (docs/)
    # We must update it to include all the new countries we just generated.
    frontend_json_path = os.path.join(DOCS_DIR, 'countries.json')
    with open(frontend_json_path, 'w', encoding='utf-8') as f:
        json.dump(master_countries, f, indent=2)
        
    print(f"SYNC COMPLETE: Updated frontend docs/countries.json with {len(master_countries)} countries.")

if __name__ == '__main__':
    main()
