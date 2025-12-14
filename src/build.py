import json
import os
import random
import urllib.request
import urllib.error
# urllib.parse is imported locally where needed as per user request
from jinja2 import Environment, FileSystemLoader

# Configuration
DATA_DIR = 'data'
DOCS_DIR = 'docs'
TEMPLATES_DIR = 'templates'
STATIC_LOGOS_DIR = os.path.join(DOCS_DIR, 'static', 'logos')
STATIC_COUNTRIES_DIR = os.path.join(DOCS_DIR, 'static', 'countries')

# Ensure directories exist
os.makedirs(STATIC_LOGOS_DIR, exist_ok=True)
os.makedirs(STATIC_COUNTRIES_DIR, exist_ok=True)

def download_logo(url, name):
    if not url:
        return ''
    
    # Sanitize filename
    safe_name = "".join([c for c in name.lower() if c.isalnum() or c in (' ', '-', '_')]).strip().replace(' ', '_')
    filename = f"{safe_name}.png"
    filepath = os.path.join(STATIC_LOGOS_DIR, filename)
    relative_path = f"static/logos/{filename}"
    
    if os.path.exists(filepath):
        return relative_path
        
    print(f"Downloading logo for {name}: {url}")
    try:
        req = urllib.request.Request(
            url, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Referer': 'https://www.google.com/'
            }
        )
        with urllib.request.urlopen(req) as response:
            with open(filepath, 'wb') as out_file:
                out_file.write(response.read())
        return relative_path
    except Exception as e:
        print(f"Failed to download logo for {name}: {e}")
        return url # Fallback to remote URL

def download_country_image(country):
    # If explicitly defined image URL (e.g. Wikimedia), keep it (User said they are fast)
    if country.get('image_url'):
        return country.get('image_url')

    # If missing, use LoremFlickr dynamic image but DOWNLOAD it to cache
    slug = country['slug']
    filename = f"{slug}.jpg"
    filepath = os.path.join(STATIC_COUNTRIES_DIR, filename)
    relative_path = f"static/countries/{filename}"

    if os.path.exists(filepath):
        return relative_path

    # Construct LoremFlickr URL
    url = f"https://loremflickr.com/1600/900/{slug},travel/all"
    print(f"Downloading background for {country['name']}: {url}")
    
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(filepath, 'wb') as out_file:
                out_file.write(response.read())
        return relative_path
    except Exception as e:
        print(f"Failed to download background for {country['name']}: {e}")
        return url # Fallback to remote if download fails

def comma_filter(value):
    try:
        if isinstance(value, (int, float)):
             return "{:,}".format(value)
        return value
    except:
        return value

def generate_dummy_price(provider_name, size_gb):
    # Dummy logic with some consistency
    random.seed(f"{provider_name}_{size_gb}") # Consistent per run/provider
    base = 3.0
    if size_gb >= 20:
        base = 25.0
    elif size_gb >= 10:
        base = 15.0
    elif size_gb >= 5:
        base = 10.0
    elif size_gb >= 3:
        base = 6.0
    elif size_gb >= 1:
        base = 3.0
    
    # Add randomness
    price = base + random.uniform(0, 5)
    return round(price, 2)

def main():
    # Load Data
    with open(os.path.join(DATA_DIR, 'providers.json'), 'r', encoding='utf-8') as f:
        providers = json.load(f)
        
    with open(os.path.join(DATA_DIR, 'countries.json'), 'r', encoding='utf-8') as f:
        countries = json.load(f)

    # Load Real Plans
    real_plans_path = os.path.join(DATA_DIR, 'data_plans.json')
    real_plans_data = []
    if os.path.exists(real_plans_path):
        with open(real_plans_path, 'r', encoding='utf-8') as f:
            real_plans_data = json.load(f)
    
    # Index Real Plans for O(1) Lookup: (provider_name, country_iso) -> [plans]
    real_plans_map = {}
    for p in real_plans_data:
        key = (p['provider'], p['country_iso'])
        if key not in real_plans_map:
            real_plans_map[key] = []
        real_plans_map[key].append(p)

    # Download Logos & Split Providers
    fixed_providers = []
    payg_providers = []
    
    print("Processing providers and downloading logos...")
    for p in providers:
        # Download Logo
        p['local_logo'] = download_logo(p.get('logo_url'), p.get('name'))
        
        # Split type
        if p.get('service_type') == 'pay_as_you_go':
            payg_providers.append(p)
        elif p.get('service_type') == 'hybrid':
            payg_providers.append(p)
            fixed_providers.append(p)
        else:
            fixed_providers.append(p)

    # Process Country Images FIRST (so they are ready for template)
    print("Processing country images...")
    for c in countries:
        c['image_url'] = download_country_image(c)

    # Prepare Jinja2 Environment
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    env.filters['comma'] = comma_filter
    
    try:
        index_template = env.get_template('index.html')
        country_template = env.get_template('country.html')
    except Exception as e:
        print(f"Error loading templates: {e}")
        return

    top_countries = countries[:8]
    
    # Render Index
    print("Rendering index.html...")
    try:
        output_html = index_template.render(
            all_countries=countries,
            top_countries=top_countries,
            plans_by_size={}, 
            payg_plans=payg_providers
        )
        
        with open(os.path.join(DOCS_DIR, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(output_html)
        print("Built index.html")
    except Exception as e:
        print(f"Failed to render index.html: {e}")

    # Render Country Pages
    sizes = [1, 3, 5, 10, "Unlimited"] # GB or String
    print(f"Rendering {len(countries)} country pages...")
    
    for country in countries:
        # Generate plans for this country
        plans_by_size = {} # Dict for User Request
        grouped_plans = [] # List for Existing Template
        
        for size in sizes:
            if size == "Unlimited":
                size_label = "Unlimited"
                pricing_size = 100 # Arbitrary high number for pricing logic
                target_gb = -1.0
            else:
                size_label = f"{size}GB"
                pricing_size = size
                target_gb = float(size)
            
            plans_for_size = []
            
            for p in fixed_providers:
                # Default Logic (Dummy)
                price = generate_dummy_price(p['name'], pricing_size)
                provider_name = p['name']
                final_link = "#" # Default fallback
                
                # --- REAL DATA INJECTION START ---
                c_code = country.get('code', '').upper()
                
                # Check for Real Plans
                found_real_plan = None
                available_plans = []
                
                # Lookup key: (Provider Name, Country ISO)
                # Note: build.py uses "Airalo", data_plans uses "Airalo"
                lookup_key = (provider_name, c_code)
                
                if lookup_key in real_plans_map:
                    raw_plans = real_plans_map[lookup_key]
                    
                    # Create clean available_plans list for JSON injection
                    for rp in raw_plans:
                        clean_obj = {
                            'data': rp['data_gb'],
                            'day': rp['days'],
                            'price': rp['price'],
                            'link': rp['link']
                        }
                        available_plans.append(clean_obj)
                        
                        # Check if this matches our current size filter
                        # Allow slight tolerance? No, strict for now based on user specs.
                        # Handle Unlimited (-1.0)
                        if rp['data_gb'] == target_gb:
                             # If multiple matches, find cheapest?
                             if found_real_plan is None or rp['price'] < found_real_plan['price']:
                                 found_real_plan = rp

                json_plans_str = json.dumps(available_plans) if available_plans else "{}"

                # --- FINAL ROBUST MAPPING LOGIC START ---
        
                # 1. Get Country Code and Base Slug
                base_slug = country.get('slug', '').lower()
                
                # 2. Define Default Slugs
                airalo_slug = base_slug
                maya_slug = base_slug
                saily_slug = base_slug
                yesim_slug = base_slug

                # 3. MANUAL OVERRIDES (The Fix)
                
                if c_code == 'US':
                    # USA Specifics
                    airalo_slug = 'united-states'
                    maya_slug = 'usa'            # <--- FIX: Maya uses 'usa', not 'united-states'
                    saily_slug = 'united-states'
                    yesim_slug = 'united-states'
                    
                elif c_code == 'GB':
                    # UK Specifics
                    airalo_slug = 'united-kingdom'
                    maya_slug = 'uk'             # <--- FIX: Maya uses 'uk', not 'united-kingdom'
                    saily_slug = 'united-kingdom'
                    yesim_slug = 'united-kingdom'

                # (South Korea and others use the base_slug 'south-korea', so they work automatically)
                
                # 4. GENERATE LINKS (Fallback if real link not found)
                
                if "Airalo" in provider_name:
                    if found_real_plan:
                         final_link = found_real_plan['link']
                         price = found_real_plan['price']
                    else:
                        # Fallback Link Logic
                        target = f"https://airalo.com/{airalo_slug}-esim"
                        final_link = f"https://tp.media/r?campaign_id=541&marker=689615&p=8310&trs=479661&u={target}"

                elif "Maya" in provider_name:
                    # DIRECT LINK (No Travelpayouts Wrapper)
                    # Format: https://maya.net/esim/usa?pid=QTsarrERAv1y
                    target = f"https://maya.net/esim/{maya_slug}?pid=QTsarrERAv1y"
                    final_link = target

                elif "Saily" in provider_name:
                    target = f"https://saily.com/esim-{saily_slug}" 
                    final_link = f"https://tp.media/r?campaign_id=629&marker=689615&p=8979&trs=479661&u={target}"

                elif "Yesim" in provider_name:
                    target = f"https://yesim.tech/country/{yesim_slug}"
                    final_link = f"https://tp.media/r?campaign_id=224&marker=689615&p=5998&trs=479661&u={target}"

                elif "Klook" in provider_name:
                    import urllib.parse
                    encoded_query = urllib.parse.quote(f"esim {country.get('name', '')}")
                    target = f"https://www.klook.com/en-US/search/?keyword={encoded_query}"
                    final_link = f"https://tp.media/r?campaign_id=137&marker=689615&p=4110&trs=479661&u={target}"

                elif "Drimsim" in provider_name:
                     final_link = "https://tp.media/r?campaign_id=102&marker=689615&p=2762&trs=479661&u=https://drimsim.com"

                else:
                    final_link = "#"
                # --- FINAL ROBUST MAPPING LOGIC END ---
                
                # Calculate Discounted Price
                discounted_price = None
                discount_label = None
                best_coupon_code = None
                
                coupons = p.get('coupons')
                if coupons and coupons.get('new_user'):
                    try:
                        label = coupons['new_user']['label']
                        if "%" in label:
                            percent = float(label.replace('%', '').replace(' OFF', ''))
                            discounted_price = price * (1 - (percent / 100))
                            discounted_price = round(discounted_price, 2)
                            discount_label = label
                            best_coupon_code = coupons['new_user']['code']
                    except:
                        pass
                
                plan_obj = {
                    'name': p['name'],
                    'logo_url': p['local_logo'], 
                    'price': price, # Original Price
                    'discounted_price': discounted_price,
                    'discount_label': discount_label,
                    'best_coupon_code': best_coupon_code,
                    'data_amount': size_label,
                    'link': final_link, # Use the computed link variable
                    'features': p['benefits'], 
                    'benefits': p['benefits'],
                    'rating': p['base_rating'],
                    'review_count': p['review_count'],
                    'coupons': coupons,
                    'is_cheapest': False,
                    'json_data': json_plans_str # Added for data-plans attribute
                }
                plans_for_size.append(plan_obj)
            
            # Sort Top 5 by Price (Effective Price)
            plans_for_size.sort(key=lambda x: x['discounted_price'] if x['discounted_price'] else x['price'])
            top_5 = plans_for_size[:5]
            
            if top_5:
                top_5[0]['is_cheapest'] = True
            
            plans_by_size[size_label] = top_5
            grouped_plans.append({
                'data_amount': size_label,
                'plans': top_5
            })
            
        # Render
        try:
            country_html = country_template.render(
                country=country['name'], 
                country_slug=country['slug'],
                country_code=country.get('code'),
                image_url=country.get('image_url'),
                intro_text=country.get('intro_text'),
                
                # Requested vars
                all_countries=countries,
                top_countries=top_countries,
                plans_by_size=plans_by_size,
                payg_plans=payg_providers,
                
                # Template compat var
                grouped_plans=grouped_plans 
            )
            
            out_path = os.path.join(DOCS_DIR, f"{country['slug']}.html")
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(country_html)
        except Exception as e:
            print(f"Failed to render {country['name']}: {e}")
            
    print("Build complete.")

if __name__ == '__main__':
    main()
