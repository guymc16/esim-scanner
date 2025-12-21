import os
import re
import datetime

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DOCS_DIR = os.path.join(PROJECT_ROOT, 'docs')

# Core files to exclude from SEO updates
IGNORED_FILES = {
    'index.html',
    'about.html',
    'partners.html',
    'toolkit.html',
    'sitemap.xml',
    '404.html',
    'google',  # any google verification files
    'robots.txt'
}

# 1. The Data Dictionary (VIP Data)
COUNTRIES_DATA = {
    "Israel": {
        "slug": "israel",
        "capital": "Jerusalem",
        "landmark": "the Western Wall",
        "network": "Pelephone",
        "plug": "Type H"
    },
    "Japan": {
        "slug": "japan",
        "capital": "Tokyo",
        "landmark": "Shibuya Crossing",
        "network": "Docomo",
        "plug": "Type A"
    },
    "USA": {
        "slug": "usa",
        "capital": "Washington D.C.",
        "landmark": "Times Square",
        "network": "T-Mobile",
        "plug": "Type A/B"
    },
    "France": {
        "slug": "france",
        "capital": "Paris",
        "landmark": "the Eiffel Tower",
        "network": "Orange",
        "plug": "Type E"
    },
    "United Kingdom": {
        "slug": "united-kingdom",
        "capital": "London",
        "landmark": "Big Ben",
        "network": "EE",
        "plug": "Type G"
    },
    "Italy": {
        "slug": "italy",
        "capital": "Rome",
        "landmark": "the Colosseum",
        "network": "TIM",
        "plug": "Type L"
    },
    "Spain": {
        "slug": "spain",
        "capital": "Madrid",
        "landmark": "Sagrada Família",
        "network": "Movistar",
        "plug": "Type F"
    },
    "Germany": {
        "slug": "germany",
        "capital": "Berlin",
        "landmark": "Brandenburg Gate",
        "network": "Telekom",
        "plug": "Type F"
    },
    "Portugal": {
        "slug": "portugal",
        "capital": "Lisbon",
        "landmark": "Belem Tower",
        "network": "MEO",
        "plug": "Type F"
    },
    "Greece": {
        "slug": "greece",
        "capital": "Athens",
        "landmark": "the Acropolis",
        "network": "Cosmote",
        "plug": "Type F"
    },
    "Switzerland": {
        "slug": "switzerland",
        "capital": "Bern",
        "landmark": "The Matterhorn",
        "network": "Swisscom",
        "plug": "Type J"
    },
    "Turkey": {
        "slug": "turkey",
        "capital": "Ankara",
        "landmark": "Hagia Sophia",
        "network": "Turkcell",
        "plug": "Type F"
    },
    "Thailand": {
        "slug": "thailand",
        "capital": "Bangkok",
        "landmark": "the Grand Palace",
        "network": "AIS",
        "plug": "Type A/B"
    },
    "South Korea": {
        "slug": "south-korea",
        "capital": "Seoul",
        "landmark": "Gyeongbokgung Palace",
        "network": "SK Telecom",
        "plug": "Type F"
    },
    "Indonesia": {
        "slug": "indonesia",
        "capital": "Jakarta",
        "landmark": "Bali Beaches",
        "network": "Telkomsel",
        "plug": "Type C"
    },
    "Singapore": {
        "slug": "singapore",
        "capital": "Singapore",
        "landmark": "Marina Bay Sands",
        "network": "Singtel",
        "plug": "Type G"
    },
    "Australia": {
        "slug": "australia",
        "capital": "Canberra",
        "landmark": "Sydney Opera House",
        "network": "Telstra",
        "plug": "Type I"
    },
    "Canada": {
        "slug": "canada",
        "capital": "Ottawa",
        "landmark": "Niagara Falls",
        "network": "Rogers",
        "plug": "Type A"
    },
    "Mexico": {
        "slug": "mexico",
        "capital": "Mexico City",
        "landmark": "Chichen Itza",
        "network": "Telcel",
        "plug": "Type A"
    },
    "United Arab Emirates": {
        "slug": "united-arab-emirates",
        "capital": "Abu Dhabi",
        "landmark": "Burj Khalifa",
        "network": "Etisalat",
        "plug": "Type G"
    },
    "Netherlands": {
        "slug": "netherlands",
        "capital": "Amsterdam",
        "landmark": "the Canals",
        "network": "KPN/Vodafone",
        "plug": "Type C/F"
    }
}

def get_country_data(filename):
    """
    Determines country data based on filename.
    Returns (country_name, data_dict)
    """
    slug = filename.replace('.html', '')
    
    # Capitalize Slug for Name (e.g. costa-rica -> Costa Rica)
    country_name = slug.replace('-', ' ').title()
    
    # Special Case Fixes (e.g. Uae -> UAE, Usa -> USA if not handled)
    if country_name.lower() == 'usa': country_name = "USA"
    if country_name.lower() == 'uae': country_name = "UAE"
    if country_name.lower() == 'uk': country_name = "UK"
    if country_name.lower() == 'united kingdom': country_name = "United Kingdom"

    # LOOKUP IN VIP DATA
    # Try to find by name match
    # 1. Exact Name Match
    if country_name in COUNTRIES_DATA:
        return country_name, COUNTRIES_DATA[country_name]
    
    # 2. Slug Match
    for name, data in COUNTRIES_DATA.items():
        if data['slug'] == slug:
            return name, data

    # FALLBACK LOGIC
    # print(f"   (Using fallback data for {country_name})")
    fallback_data = {
        "slug": slug,
        "capital": "the capital city",
        "landmark": "popular tourist attractions",
        "network": "top-tier local networks",
        "plug": "local"  # Will result in "local power outlets"
    }
    return country_name, fallback_data


def generate_premium_accordion(country_name, data):
    """
    Generates the Premium Tailwind Accordion HTML.
    """
    current_year = datetime.datetime.now().year
    
    # formatting "plug" correctly for fallback
    plug_text = f"<strong>{data['plug']}</strong>" if data['plug'] != "local" else "the local"
    
    html = f"""<!-- Premium FAQ Accordion -->
<div id="faq-section" class="max-w-4xl mx-auto my-16 px-4">
    <details class="group bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <summary class="flex items-center justify-between p-5 cursor-pointer bg-white hover:bg-gray-50 transition-colors list-none select-none">
            <span class="flex items-center gap-3 text-lg font-semibold text-gray-800">
                <span>🌍</span> Traveler's Guide: Connectivity in {country_name} ({current_year})
            </span>
            <svg class="w-5 h-5 text-gray-400 transform group-open:rotate-180 transition-transform duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
        </summary>
        <div class="p-6 text-gray-600 bg-gray-50/50 border-t border-gray-100 space-y-4 text-sm leading-relaxed">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <h4 class="font-bold text-gray-800 mb-2">Why buy an eSIM?</h4>
                    <p>Traveling to <strong>{country_name}</strong>? Whether you're visiting <strong>{data['landmark']}</strong> or staying in <strong>{data['capital']}</strong>, public WiFi is unreliable. An eSIM gives you instant, secure data the moment you land.</p>
                </div>
                <div>
                    <h4 class="font-bold text-gray-800 mb-2">Best Local Network</h4>
                    <p>Connecting to networks like <strong>{data['network']}</strong> ensures you have fast 4G/5G coverage, even in remote areas.</p>
                </div>
                <div>
                    <h4 class="font-bold text-gray-800 mb-2">Installation</h4>
                    <p>You will receive a QR code via email instantly. Scan it to activate data in under 2 minutes.</p>
                </div>
                <div>
                    <h4 class="font-bold text-gray-800 mb-2">Local Tech Specs</h4>
                    <p>{country_name} uses {plug_text} power outlets. Don't forget your travel adapter!</p>
                </div>
            </div>
        </div>
    </details>
</div>
<!-- End Accordion -->"""
    return html

def update_country_page(filename, country_name, data):
    """
    Surgically updates the HTML file for a country.
    """
    filepath = os.path.join(DOCS_DIR, filename)
    
    if not os.path.exists(filepath):
        print(f"File not found: {filename} (Skipping)")
        return
        
    # print(f"   - Updating {filename}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    current_year = datetime.datetime.now().year
    
    # --- Step A: SEO Updates (Regex) ---
    
    # 1. Title
    # New Format: "Best eSIM for {Country} (2025) | Cheapest & Student Plans"
    new_title = f"Best eSIM for {country_name} ({current_year}) | Cheapest & Student Plans"
    
    # Check if Title actually needs update to avoid regex work if possible? 
    # Valid regex replace is fast enough.
    content = re.sub(r'<title>.*?</title>', f'<title>{new_title}</title>', content, count=1, flags=re.IGNORECASE)
    
    # 2. Meta Description
    # New Format: "Looking for the cheapest eSIM for {Country}? Compare top-tier data plans for travelers and students. Instant activation, no roaming fees. Plans start from $4.50."
    new_desc = f"Looking for the cheapest eSIM for {country_name}? Compare top-tier data plans for travelers and students. Instant activation, no roaming fees. Plans start from $4.50."
    
    desc_pattern = r'<meta\s+name=["\']description["\']\s+content=["\'].*?["\']\s*/?>'
    if re.search(desc_pattern, content, re.IGNORECASE):
        content = re.sub(desc_pattern, f'<meta name="description" content="{new_desc}">', content, count=1, flags=re.IGNORECASE)
    else:
        # Insert after title if missing
        # print("     (Injecting missing Meta Description)")
        content = re.sub(r'(</title>)', f'\\1\n    <meta name="description" content="{new_desc}">', content, count=1, flags=re.IGNORECASE)
                     
    # --- Step B: Accordion Injection ---
    
    accordion_html = generate_premium_accordion(country_name, data)
    
    # Check if we already have an FAQ section (to update it instead of duplicate)
    if 'id="faq-section"' in content:
        # print("     (Updating existing Accordion)")
        # Regex to remove existing block using our comments
        if '<!-- Premium FAQ Accordion -->' in content:
             content = re.sub(r'<!-- Premium FAQ Accordion -->.*?<!-- End Accordion -->', accordion_html, content, flags=re.DOTALL)
        else:
            # Fallback for the very first overwrite if structure exists but not comments? 
            # We assume "Surgical Update" Phase 1 put them there, OR they don't exist in fallback files yet.
            print(f"   WARNING: {filename} has id='faq-section' but no comment markers. Skipping accordion to avoid duplication/damage.")
            pass 
    else:
        # print("     (Injecting new Accordion)")
        # Insert before <footer>
        match = re.search(r'(<footer)', content, re.IGNORECASE)
        if match:
            idx = match.start()
            content = content[:idx] + accordion_html + "\n\n" + content[idx:]
        else:
             content = content.replace('</body>', f'{accordion_html}\n</body>')

    # --- Step C: Save ---
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    print("--- STARTING UNIVERSAL SURGICAL UPDATE (PHASE 4) ---")
    print(f"Target Directory: {DOCS_DIR}")
    
    # 1. Discover all HTML files
    all_files = os.listdir(DOCS_DIR)
    html_files = [f for f in all_files if f.endswith('.html')]
    
    valid_files = [f for f in html_files if f not in IGNORED_FILES]
    print(f"Found {len(valid_files)} country pages to update.")
    
    count = 0
    for filename in valid_files:
        # 2. Determine Data
        name, data = get_country_data(filename)
        
        # 3. Update
        try:
            update_country_page(filename, name, data)
            count += 1
            if count % 10 == 0:
                print(f"   Processed {count} files...")
        except Exception as e:
            print(f"   ERROR updating {filename}: {e}")
        
    print(f"\n--- COMPLETED {count} FILES ---")

if __name__ == '__main__':
    main()
