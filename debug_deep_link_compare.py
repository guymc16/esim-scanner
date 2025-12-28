import json
import urllib.parse

def main():
    with open('data/data_plans.json', 'r', encoding='utf-8') as f:
        plans = json.load(f)

    il_link = None
    us_link = None
    
    # We want one sample for each
    for p in plans:
        if p['provider'] == 'Airalo':
            if p['country_iso'] == 'IL' and not il_link:
                il_link = p['link']
            if p['country_iso'] == 'US' and not us_link:
                us_link = p['link']
        
        if il_link and us_link:
            break

    print("--- RAW LINKS ---")
    print(f"Israel: {il_link}")
    print(f"USA:    {us_link}")
    
    print("\n--- DECODED 'u' PARAMETER ---")
    
    def extract_u(link):
        if not link: return "N/A"
        try:
            parsed = urllib.parse.urlparse(link)
            qs = urllib.parse.parse_qs(parsed.query)
            return qs.get('u', ['N/A'])[0]
        except:
            return "Error"

    print(f"Israel Target: {extract_u(il_link)}")
    print(f"USA Target:    {extract_u(us_link)}")

if __name__ == "__main__":
    main()
