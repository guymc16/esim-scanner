import json
import os
import random
import urllib.request
import urllib.error
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
            else:
                size_label = f"{size}GB"
                pricing_size = size
            
            plans_for_size = []
            
            for p in fixed_providers:
                # Price
                price = generate_dummy_price(p['name'], pricing_size)
                
                # Affiliate Link
                link = p['affiliate_link']
                if '{country_slug}' in link:
                    link = link.replace('{country_slug}', country['slug'])
                
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
                    'link': link,
                    'features': p['benefits'], 
                    'benefits': p['benefits'],
                    'rating': p['base_rating'],
                    'review_count': p['review_count'],
                    'coupons': coupons,
                    'is_cheapest': False 
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
