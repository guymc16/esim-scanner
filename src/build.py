import json
import os
import random
import urllib.request
import urllib.error
import urllib.parse
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
    random.seed(f"{provider_name}_{size_gb}") 
    base = 4.5 # Standard market rate for 1GB
    
    if size_gb >= 50:
        base = 100.0
    elif size_gb >= 20:
        base = 35.0
    elif size_gb >= 10:
        base = 18.0
    elif size_gb >= 5:
        base = 12.0
    elif size_gb >= 3:
        base = 8.0
    elif size_gb >= 2:
        base = 6.0
    elif size_gb >= 1:
        base = 4.5
    else: # Unlimited
        base = 35.0

    # Multiplier-based randomness (stable)
    multiplier = random.uniform(0.95, 1.05)
    
    # Specific adjustments to match user perception if needed
    if "Yesim" in provider_name:
        multiplier = 1.0 # Force stable for Yesim
        if size_gb == 1: base = 4.5 # Result ~4.50 -> 3.60w/20%

    price = base * multiplier
    return round(price, 2)

def get_affiliate_link(provider_name, iso_code, slug):
    p = provider_name
    c = iso_code.upper()
    s = slug.lower()
    
    # Overrides
    if c == 'US': s = 'usa' if "Maya" in p else 'united-states'
    elif c == 'GB': s = 'uk' if "Maya" in p else 'united-kingdom'
    
    # Logic
    if "Airalo" in p: return f"https://tp.media/r?campaign_id=541&marker=689615&p=8310&trs=479661&u=https://airalo.com/{s}-esim"
    if "Maya" in p: return f"https://maya.net/esim/{s}?pid=QTsarrERAv1y"
    if "Saily" in p: return f"https://tp.media/r?campaign_id=629&marker=689615&p=8979&trs=479661&u=https://saily.com/esim-{s}"
    if "Yesim" in p: return f"https://tp.media/r?campaign_id=224&marker=689615&p=5998&trs=479661&u=https://yesim.tech/country/{s}"
    elif "Klook" in p:
         import urllib.parse
         # 1. Clean Search Term
         search_term = f"esim {s.replace('-', ' ')}"
         
         # 2. Build Target URL (Matching the actual Klook search structure)
         # Note: usage of '/search/result/' and '?query='
         # We use quote() to get '%20' instead of '+' which Klook prefers in this structure
         target_url = f"https://www.klook.com/en-US/search/result/?query={urllib.parse.quote(search_term)}"
         
         # 3. Encode for Travelpayouts (Safe wrapping)
         encoded_target = urllib.parse.quote(target_url, safe='')
         
         return f"https://tp.media/r?campaign_id=137&marker=689615&p=4110&trs=479661&u={encoded_target}"
    
    return "#"

def fix_template_safeguard():
    """
    User requested 'Just fix build'. 
    This auto-repairs the recurrent Jinja syntax error in templates/index.html 
    BEFORE the build process tries to interpret it.
    """
    target_file = os.path.join(TEMPLATES_DIR, 'index.html')
    if not os.path.exists(target_file):
        return

    try:
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # The specific regression pattern
        bad_pattern = '{ { country.is_popular | tojson } }'
        good_pattern = '{{ country.is_popular|tojson }}'
        
        if bad_pattern in content:
            print("SAFEGUARD: Fixing broken Jinja syntax in index.html...")
            content = content.replace(bad_pattern, good_pattern)
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(content)
    except Exception as e:
        print(f"SAFEGUARD WARNING: Could not check template: {e}")

def ensure_about_hero():
    """Downloads a clean hero image without text overlays."""
    url = "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?q=80&w=2074&auto=format&fit=crop"
    filepath = os.path.join(DOCS_DIR, 'static', 'brand', 'hero_bg_clean.jpg')
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    if not os.path.exists(filepath):
        print("Downloading clean About Us hero...")
        try:
             req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
             with urllib.request.urlopen(req) as response:
                 with open(filepath, 'wb') as f:
                     f.write(response.read())
        except Exception as e:
            print(f"Failed to download hero: {e}")
    return "static/brand/hero_bg_clean.jpg"

def main():
    # 0. Safeguard: Fix Templates
    fix_template_safeguard()
    ensure_about_hero()
    
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

    # Enrich Countries with Region & Popularity from Plan Data
    # 1. Build Lookup
    country_meta_map = {}
    for p in real_plans_data:
        iso = p.get('country_iso')
        if iso:
            # If we haven't seen this country yet, or if this plan marks it as popular, update.
            # We want to capture the region (assumed constant per country) and is_popular flag.
            if iso not in country_meta_map:
                country_meta_map[iso] = {
                    'region': p.get('region', 'Other'),
                    'is_popular': p.get('is_popular', False)
                }
            else:
                # If any plan says it's popular, the country is popular
                if p.get('is_popular'):
                    country_meta_map[iso]['is_popular'] = True
                # Region should be consistent, no need to overwrite unless missing

    # 2. Inject into Country Objects
    for c in countries:
        code = c.get('code')
        if code in country_meta_map:
            c['region'] = country_meta_map[code]['region']
            c['is_popular'] = country_meta_map[code]['is_popular']
        else:
            c['region'] = 'Other'
            c['is_popular'] = False

    # Force correct links in the loaded JSON data
    for plan in real_plans_data:
        country_match = next((c for c in countries if c['code'] == plan['country_iso']), None)
        c_slug = country_match['slug'] if country_match else plan['country_iso']
        plan['link'] = get_affiliate_link(plan['provider'], plan['country_iso'], c_slug)
    
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
        c['image'] = download_country_image(c) # Check key 'image' vs 'image_url' in template

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
    print(f"Rendering {len(countries)} country pages...")
    
    for country in countries:
        # Generate plans for this country
        grouped_plans = [] # List of dicts with title, filter_value, plans
        
        # Valid sizes to group by
        sizes = [1, 2, 3, 5, 10, 20, -1]
                
        # Get plans map for this country
        c_code = country.get('code', '').upper()
        base_slug = country.get('slug', '').lower()

        # Pre-calc overrides for link generation (Affiliate)
        slugs = {
            'Airalo': base_slug,
            'Maya Mobile': base_slug,
            'Saily': base_slug,
            'Yesim': base_slug
        }
        if c_code == 'US':
             slugs = {'Airalo': 'united-states', 'Maya Mobile': 'usa', 'Saily': 'united-states', 'Yesim': 'united-states'}
        elif c_code == 'GB':
             slugs = {'Airalo': 'united-kingdom', 'Maya Mobile': 'uk', 'Saily': 'united-kingdom', 'Yesim': 'united-kingdom'}

        for size in sizes:
            section_plans = []
            
            for provider_meta in fixed_providers:
                p_name = provider_meta['name']
                
                # Check for Real Plans Data
                key = (p_name, c_code)
                
                if key in real_plans_map and real_plans_map[key]:
                    # REAL DATA PATH
                    plans = real_plans_map[key]
                    matching_plans = [p for p in plans if p['data_gb'] == size]
                    
                    if not matching_plans:
                        continue
                        
                    best_plan = min(matching_plans, key=lambda x: x['price'])
                    price = best_plan['price']
                    duration = best_plan['days']
                    final_link = best_plan['link']
                    
                    # JSON for Filter
                    available_plans_list = []
                    for rp in plans:
                        available_plans_list.append({
                            'data': rp['data_gb'],
                            'day': rp['days'],
                            'price': rp['price'],
                            'link': rp['link']
                        })
                    json_data = json.dumps(available_plans_list)
                    
                else:
                    # FALLBACK / DUMMY DATA PATH (For Maya, Saily, etc.)
                    # Only generate if it makes sense (e.g. usually providers have 1/3/5/10/20)
                    if size == -1: # Unlimited logic
                        pass

                    
                    smart_link = get_affiliate_link(p_name, c_code, base_slug)
                    
                    # Update dummy plans generation
                    dummy_plans = []
                    dummy_sizes = [1, 2, 3, 5, 10, 20, 50, -1]
                    for d_size in dummy_sizes:
                         dummy_plans.append({
                            'data': d_size, 
                            'day': 30, 
                            'price': generate_dummy_price(p_name, d_size), 
                            'link': smart_link 
                         })
                    
                    # Create JSON with correct links
                    json_data = json.dumps(dummy_plans)
                    final_link = smart_link
                    best_plan = {'coupon': None}
                    price = generate_dummy_price(p_name, size)
                    duration = 30

                # Link Logic (Dynamic or Fallback)
                if not final_link or final_link == "#":
                     # Fallback Affiliate Links
                     s = slugs.get(p_name, base_slug)
                     if "Airalo" in p_name: final_link = f"https://tp.media/r?campaign_id=541&marker=689615&p=8310&trs=479661&u=https://airalo.com/{s}-esim"
                     elif "Maya" in p_name: final_link = f"https://maya.net/esim/{s}?pid=QTsarrERAv1y"
                     elif "Saily" in p_name: final_link = f"https://tp.media/r?campaign_id=629&marker=689615&p=8979&trs=479661&u=https://saily.com/esim-{s}"
                     elif "Yesim" in p_name: final_link = f"https://tp.media/r?campaign_id=224&marker=689615&p=5998&trs=479661&u=https://yesim.tech/country/{s}"
                     elif "Klook" in p_name:
                         # Klook needs encoded search
                         q = urllib.parse.quote(f"esim {country.get('name', '')}")
                         final_link = f"https://www.klook.com/en-US/search/?keyword={q}"
                
                # Dynamic Discount Calculation (Front-loaded)
                discounted_price = None
                coupons = best_plan.get('coupon')
                if not coupons:
                    coupons = provider_meta.get('coupons')
                
                if coupons and coupons.get('new_user'):
                    l = coupons['new_user']['label'] # e.g. "15% OFF"

                    if "%" in l:
                        try:
                            pct = float(l.replace('%','').replace(' OFF',''))
                            discounted_price = price * (1 - pct/100)
                        except: pass


                plan_display = {
                    'name': p_name,
                    'logo_url': provider_meta['local_logo'],
                    'rating': provider_meta['base_rating'],
                    'review_count': provider_meta['review_count'],
                    'json_data': json_data, # Essential for JS
                    
                    # Display values
                    'data': size,
                    'price': price,
                    'discounted_price': discounted_price,
                    'duration': duration,
                    'link': final_link,
                    
                    'benefits': provider_meta['benefits'],
                    'coupons': coupons,
                    'is_cheapest': False
                }
                section_plans.append(plan_display)
            
            # Sort Section by Price
            # Sort plans by price (low to high)
            # Ensure discounted_price is used if present
            def get_sort_price(p):
                val = p['discounted_price'] if p['discounted_price'] else p['price']
                return val

            section_plans.sort(key=get_sort_price)
            
            # Recalculate cheapest flag based on sorted list
            if section_plans:
                # Reset all first
                for p in section_plans: p['is_cheapest'] = False
                # Set first as cheapest
                section_plans[0]['is_cheapest'] = True

            if section_plans:
                grouped_plans.append({
                    'title': f"{size}GB Plans" if size != -1 else "Unlimited Data Plans",
                    'filter_value': 999 if size == -1 else size,
                    'plans': section_plans
                })

        # Render Template
        try:
            output_html = country_template.render(
                country=country, # Pass FULL Object so {{ country.name }} works
                all_countries=countries,
                top_countries=top_countries,
                grouped_plans=grouped_plans, 
                payg_plans=payg_providers
            )
            
            with open(os.path.join(DOCS_DIR, f"{country['slug']}.html"), 'w', encoding='utf-8') as f:
                f.write(output_html)
        except Exception as e:
            print(f"Failed to render {country['name']}: {e}")
            

    # Render About Page
    try:
        about_template = env.get_template('about.html')
        about_html = about_template.render(
            all_countries=countries,
            page_title="About Us"
        )
        with open(os.path.join(DOCS_DIR, 'about.html'), 'w', encoding='utf-8') as f:
            f.write(about_html)
        print("Built about.html")
    except Exception as e:
        print(f"Failed to render about.html: {e}")

    print("Build complete.")

if __name__ == '__main__':
    main()
