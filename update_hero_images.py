
import re

# Mapping of Country Name (lowercase for matching) -> Unsplash Photo ID (last part of URL)
# Used user's list, skipping missing Guinea-Bissau for now.
# User's URLs e.g. https://unsplash.com/photos/group-of-forest-elephants...-QMAOXqlLn5Q
# We extract ID "QMAOXqlLn5Q" and form "https://images.unsplash.com/photo-QMAOXqlLn5Q?ixlib=rb-4.1.0&q=80&w=1080"

updates = {
    "central african republic": "QMAOXqlLn5Q",
    "cameroon": "f6ruhwz9MFc",
    "ethiopia": "eRFC0_U0hGE",
    "gambia": "GygPFmXGD1o",
    "grenada": "c9yXt2dL1JI",
    "guam": "zNRU6opOyAA",
    "guinea": "5FU10SbjKJM",
    # "guinea-bissau": "SKIPPED_MISSING",
    "guyana": "TsnY150S3Pc",
    "iraq": "8eJTLS3lIiw",
    "haiti": "EICXhtGFDAs",
    "kosovo": "NNMF5B5Zsa8",
    "malawi": "6QjWzfnrN_g",
    "mayotte": "qjyY80RtOEU",
    "namibia": "UwQp0wHLSaE", # corrected spelling "nambia"
    "nauru": "LoREprgqzCI",
    "niger": "nJ-3hV0Xp_g",
    "northern cyprus": "RPk4aFw1K4w",
    "papua new guinea": "n1LrwXzsnuU",
    "reunion": "SKryJkQogrA",
    "rwanda": "z-lNmXoXt-k",
    "saint lucia": "StcchinvvQs",
    "senegal": "zLXKV5UV8F4",
    "timor-leste": "rbmwEl8H-Oc", # "timor leste" -> "timor-leste" likely key
    "vanuatu": "JxL6t8iVri4"
}

target_file = 'src/create_world_db.py'

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to find where the URL is defined. 
# It could be in RICH_DATA (as 'image_source_url': "...") or UNSPLASH_GAP_FILL.
# Strategy: 
# 1. Search for regex `'{code}': \{.*? 'image_source_url': "(.*?)"`? No, too complex multiline.
# 2. Iterate through `updates`. 
#    - Try to find `'{name_capitalized}': '...'` in UNSPLASH_GAP_FILL.
#    - Try to find `'name': "{Name}", ... 'image_source_url': "..."` in RICH_DATA.

new_content = content

for name, photo_id in updates.items():
    direct_url = f"https://images.unsplash.com/photo-{photo_id}?ixlib=rb-4.1.0&q=80&w=1080"
    
    # Capitalize for searching (e.g. "Gambia")
    # Special cases: "central african republic" -> "Central African Republic"
    name_cap = name.title()
    if name == "guinea-bissau": name_cap = "Guinea-Bissau"
    if name == "timor-leste": name_cap = "Timor-Leste" # or "Timor-leste"? Usually proper case.
    if name == "central african republic": name_cap = "Central African Republic"
    if name == "northern cyprus": name_cap = "Northern Cyprus"
    if name == "papua new guinea": name_cap = "Papua New Guinea"
    if name == "saint lucia": name_cap = "Saint Lucia"
    
    # 1. Attempt replace in UNSPLASH_GAP_FILL
    # Pattern: 'Name': 'OLD_URL',
    # Use generic regex to be safe with spaces/quotes
    # We want to replace the value URL.
    
    # gap fill pattern: 'Gambia': '...'
    regex_gap = r"('" + re.escape(name_cap) + r"':\s*')([^']+?)(')"
    
    match_gap = re.search(regex_gap, new_content)
    if match_gap:
        print(f"Updating {name_cap} in UNSPLASH_GAP_FILL")
        # Replace only the URL group (group 2)
        # re.sub is tricky with groups, better to just replace the whole match string carefully
        # or use a function.
        new_content = re.sub(regex_gap, r"\1" + direct_url + r"\3", new_content, count=1)
        continue # Found it, next country

    # 2. Attempt replace in RICH_DATA
    # Pattern: 'name': "Gambia", ... 'image_source_url': "OLD_URL"
    # This is multiline.
    # We can look for the name line, then find the image_source_url line following it narrowly?
    # Or strict replacement if we know the unique current URL (loremflickr).
    # Most of these have "loremflickr.com/800/600/Gambia,landscape/all"
    # Let's try replacing the specific LoremFlickr URL for that country!
    # Expected LoremFlickr: `https://loremflickr.com/800/600/Name,landscape/all` or with commas replacing spaces
    
    lorem_name = name_cap.replace(" ", ",")
    lorem_url = f"https://loremflickr.com/800/600/{lorem_name},landscape/all"
    
    # Try finding this specific URL in the file
    if lorem_url in new_content:
        print(f"Updating {name_cap} via LoremFlickr URL replacement")
        new_content = new_content.replace(lorem_url, direct_url)
    else:
        # Fallback: maybe punctuation diffs (e.g. Cote d'Ivoire)
        # Or maybe it was already Unsplash? (e.g. Malawi might be in gap fill)
        print(f"WARNING: Could not find entry for {name_cap} (Tried Gap Fill and LoremFlickr: {lorem_url})")
        # specific manual checks for tough ones later if needed

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Update complete.")
