import json

with open('data/maya_feed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

products = data.get('products', [])
print(f"Total Products: {len(products)}")

for p in products:
    iso = p.get('country_iso2', '').upper()
    if iso == 'IL':
        print(f"\n--- Israel Plan ---")
        print(f"Data: {p.get('data_gb')}")
        print(f"Duration: {p.get('duration_days')}")
        print(f"URL: {p.get('url_direct')}")
        print(f"Type: {p.get('plan_type')}")
        
    # Also valid check if 180 is string
    if iso == 'IL' and str(p.get('duration_days')) == '180':
        print("*** FOUND 180 DAY PLAN ***")
