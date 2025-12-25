import xml.etree.ElementTree as ET
import json
import re
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
XML_FILE = DATA_DIR / "airalo_feed.xml"
MAYA_FEED = DATA_DIR / "maya_feed.json"
COUNTRIES_FILE = DATA_DIR / "world_data.json"

# Phase 1: Region Mapping & Popularity Configuration
POPULAR_CODES = ['US', 'JP', 'FR', 'GB', 'IT', 'TH', 'ES', 'DE', 'TR', 'CN', 'CH', 'PT', 'GR']

def load_country_map():
    with open(COUNTRIES_FILE, "r", encoding="utf-8") as f:
        countries = json.load(f)
    # Map lowercase country name to ISO code
    # world_data.json is Key=ISO, Val={name: "Name"}
    # We need Name -> ISO
    return {v["name"].lower(): k for k, v in countries.items()}



def get_region(country_code):
    """
    Returns the region for a given country ISO code.
    Fallback: 'Other'
    """
    code = country_code.upper()
    
    europe = ['FR', 'DE', 'IT', 'ES', 'GB', 'NL', 'CH', 'TR', 'AT', 'GR', 'PT', 'BE', 'SE', 'NO', 'DK', 'FI', 'IE', 'PL', 'CZ', 'HU', 'RO', 'BG', 'HR', 'RS', 'SI', 'SK', 'EE', 'LV', 'LT', 'IS', 'MT', 'CY', 'AL', 'ME', 'MK', 'BA', 'MD', 'UA', 'BY', 'RU', 'MC', 'LI', 'LU', 'AD', 'SM', 'VA', 'XK']
    asia = ['JP', 'TH', 'CN', 'IN', 'ID', 'KR', 'VN', 'MY', 'SG', 'AE', 'IL', 'SA', 'QA', 'OM', 'KW', 'BH', 'LB', 'JO', 'TW', 'HK', 'MO', 'PH', 'KH', 'LA', 'MM', 'BD', 'NP', 'LK', 'PK', 'MV', 'MN', 'UZ', 'KZ', 'KG', 'TJ', 'TM', 'AF', 'IQ', 'SY', 'YE', 'PS']
    americas = ['US', 'CA', 'MX', 'BR', 'AR', 'CO', 'PE', 'CL', 'VE', 'EC', 'GT', 'CU', 'HT', 'DO', 'HN', 'PY', 'SV', 'NI', 'CR', 'PA', 'UY', 'BO', 'JM', 'TT', 'BS', 'BB', 'LC', 'VC', 'GD', 'AG', 'KN', 'DM', 'BZ', 'GY', 'SR']
    oceania = ['AU', 'NZ', 'FJ', 'PG', 'SB', 'VU', 'NC', 'PF', 'WS', 'TO', 'KI', 'FM', 'MH', 'PW', 'NR', 'TV']
    africa = ['ZA', 'EG', 'MA', 'NG', 'KE', 'ET', 'TZ', 'GH', 'UG', 'DZ', 'SD', 'CD', 'AO', 'MZ', 'CM', 'CI', 'MG', 'ZW', 'SN', 'TN', 'RW', 'SO', 'ZM', 'SS', 'GN', 'BJ', 'BI', 'TG', 'SL', 'LY', 'CG', 'LR', 'CF', 'MR', 'ER', 'NA', 'GM', 'BW', 'GA', 'LS', 'GW', 'GQ', 'DJ', 'KM', 'CV', 'ST', 'SZ', 'SC', 'MU']

    if code in europe: return 'Europe'
    if code in asia: return 'Asia'
    if code in americas: return 'Americas'
    if code in oceania: return 'Oceania'
    if code in africa: return 'Africa'
    
    return 'Other'

def parse_price(price_str):
    if not price_str:
        return 0.0
    # expected format "62.00 USD"
    clean_price = price_str.replace(" USD", "").strip()
    try:
        return float(clean_price)
    except ValueError:
        return 0.0

def parse_data_amount(data_str):
    data_str = data_str.lower().strip()
    if "unlimited" in data_str:
        return -1.0
    
    # Try getting GB
    gb_match = re.search(r"(\d+(\.\d+)?)\s*gb", data_str)
    if gb_match:
        return float(gb_match.group(1))
        
    # Try getting MB
    mb_match = re.search(r"(\d+(\.\d+)?)\s*mb", data_str)
    if mb_match:
        return float(mb_match.group(1)) / 1024.0
        
    return 0.0

def parse_days(days_str):
    days_str = days_str.lower().strip()
    # "30 days" or "7 days"
    match = re.search(r"(\d+)", days_str)
    if match:
        return int(match.group(1))
    return 0

def process_maya_feed():
    if not MAYA_FEED.exists():
        print("Maya feed not found.")
        return []
    
    with open(MAYA_FEED, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    products = data.get('products', [])
    plans = []
    
    print(f"Processing {len(products)} Maya products...")
    
    for p in products:
        # Filter: Prepaid only
        if p.get('plan_type') != 'prepaid':
            continue
            
        iso2 = p.get('country_iso2', '').upper()
        if not iso2:
             continue
             
        # Link Validation
        link = p.get('url_direct', '')
        if 'pid=QTsarrERAv1y' not in link:
             sep = '&' if '?' in link else '?'
             link += f"{sep}pid=QTsarrERAv1y"
        
        # Extract fields
        try:
            price_usd = float(p.get('price_usd', 0))
            
            # Smart Unlimited Handling
            # If API flag is true OR URL contains 'unlimited', treat as -1.0
            is_unlimited = bool(p.get('unlimited_data')) or 'unlimited' in link.lower()
            
            if is_unlimited:
                 data_gb = -1.0
            else:
                 data_gb = float(p.get('data_gb', 0))

            days = int(p.get('duration_days', 0))
        except (ValueError, TypeError):
            continue

        plan = {
            "provider": "Maya Mobile",
            "country_iso": iso2,
            "data_gb": data_gb,
            "days": days,
            "price": price_usd,
            "link": link,
            "region": get_region(iso2),
            "is_popular": iso2 in POPULAR_CODES
        }
        plans.append(plan)
        
    return plans

def analyze_feed():
    country_map = load_country_map()
    
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    
    # Namespace map for find
    ns = {'g': 'http://base.google.com/ns/1.0'}
    
    # Items are usually in channel/item. But root is rss.
    # Structure: rss -> channel -> item
    channel = root.find('channel')
    if channel is None: # Sometimes items are direct children or other structure, but usually rss > channel
         vals = root.findall('item')
    else:
         vals = channel.findall('item')

    parsed_plans = []
    
    print(f"Found {len(vals)} items in XML.")

    manual_map = {
        "united states": "US",
        "united kingdom": "GB",
        "south korea": "KR",
        "czech republic": "CZ",
        "moldova": "MD",
        # NEW MAPPINGS
        "côte d'ivoire": "CI",
        "curaçao": "CW",
        "réunion": "RE",
        "saint barthélemy": "BL",
        "democratic republic of the congo": "CD",
        "republic of the congo": "CG",
        "timor - leste": "TL",
        "virgin islands (u.s.)": "VI",
        "palestine, state of": "PS",
        "macao": "MO", 
        "saint martin (french part)": "MF",
        "sint eustatius": "BQ",
        "bonaire": "BQ",
        "saba": "BQ",
        "turks and caicos islands": "TC",
        "trinidad and tobago": "TT",
        "saint vincent and the grenadines": "VC",
        "saint kitts and nevis": "KN",
        "antigua and barbuda": "AG",
        "bosnia and herzegovina": "BA",
        "cape verde": "CV",
        "eswatini": "SZ",
        "kosovo": "XK",
        "north macedonia": "MK",
        "guinea-bissau": "GW",
        "central african republic": "CF",
        "vatican city": "VA",
        "brunei": "BN",
        "burkina faso": "BF",
        "sierra leone": "SL",
        "fiji": "FJ",
        "gambia": "GM",
        "papua new guinea": "PG",
        # UNMAPPED REGIONS (Explicitly ignored or mapped to placeholders if needed)
        # "asia": "XA", 
        # "europe": "XE", 
    }
    for item in vals:
        price_elem = item.find('g:price', ns)
        product_type_elem = item.find('g:product_type', ns)
        link_elem = item.find('g:link', ns)
        
        if price_elem is None or product_type_elem is None or link_elem is None:
            continue
            
        price_val = parse_price(price_elem.text)
        link_val = link_elem.text
        
        # Parse product_type: esim > region > country > type > data > duration
        # Example: esim > europe & cis > italy > data > 1 gb > 7 days
        # Parts can be varying, but usually:
        # 0: esim
        # 1: region (europe & cis, asia pacific, etc)
        # 2: country (italy, south korea)
        # 3: type ("data"?)
        # 4: data amount ("1 gb", "unlimited")
        # 5: duration ("7 days")
        
        raw_type = product_type_elem.text
        parts = [p.strip() for p in raw_type.split('>')]
        
        if len(parts) < 6:
            # Maybe a regional plan or different structure, skip for now to match user reqs for simple parsing
            continue
            
        country_name = parts[2].lower()
        
        # Manual overrides for XML country names to ISO codes

        # Check manual_map first, then country_map
        if country_name in manual_map:
            country_iso = manual_map[country_name]
        elif country_name in country_map:
            country_iso = country_map[country_name]
        else:
            # Could be a regional plan not in our countries list, or name mismatch
            continue
            
        data_part = parts[4] # "1 gb" or "unlimited"
        duration_part = parts[5] # "7 days"
        
        data_gb = parse_data_amount(data_part)
        days = parse_days(duration_part)
        
        # New Logic: Region & Popularity
        region = get_region(country_iso)
        is_popular = country_iso in POPULAR_CODES
        
        plan = {
            "provider": "Airalo",
            "country_iso": country_iso,
            "data_gb": data_gb,
            "days": days,
            "price": price_val,
            "link": link_val,
            "region": region,
            "is_popular": is_popular
        }
        
        parsed_plans.append(plan)
        
    print(f"Successfully parsed {len(parsed_plans)} plans.")
    
    # --- MERGE MAYA PLANS ---
    maya_plans = process_maya_feed()
    print(f"Successfully parsed {len(maya_plans)} Maya plans.")
    
    all_plans = parsed_plans + maya_plans
    print(f"Total plans merged: {len(all_plans)}")
    

    # Save to data/data_plans.json
    output_file = DATA_DIR / "data_plans.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_plans, f, indent=2)
        
    print(f"Saved parsed plans to {output_file}")
    
    # Verification for US plans
    us_plans = [p for p in all_plans if p["country_iso"] == "US"]
    print(f"Found {len(us_plans)} plans for US.")


if __name__ == "__main__":
    analyze_feed()
