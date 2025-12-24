
import xml.etree.ElementTree as ET
import json
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
XML_FILE = DATA_DIR / "airalo_feed.xml"
COUNTRIES_FILE = DATA_DIR / "world_data.json"

# Manual Map from src/process_data.py
manual_map = {
    "united states": "US",
    "united kingdom": "GB",
    "south korea": "KR",
    "czech republic": "CZ",
    "moldova": "MD"
}

def load_country_map():
    with open(COUNTRIES_FILE, "r", encoding="utf-8") as f:
        countries = json.load(f)
    # Map lowercase country name to ISO code
    return {v["name"].lower(): k for k, v in countries.items()}

def audit_feed():
    print(f"Reading {XML_FILE}...")
    try:
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
        items = root.findall("./channel/item")
    except Exception as e:
        print(f"Error reading XML: {e}")
        return

    country_map = load_country_map()
    
    unique_countries_in_xml = set()
    skipped_countries = set()
    mapped_countries = set()
    
    print(f"Processing {len(items)} items...")
    
    for item in items:
        product_type = item.find("g:product_type", namespaces={'g': 'http://base.google.com/ns/1.0'})
        if product_type is None: continue
        
        # Format: esim > latin america > côte d'ivoire > data > 2 gb > 15 days
        raw_type = product_type.text
        parts = [p.strip() for p in raw_type.split('>')]
        
        if len(parts) < 3: continue
        
        country_name = parts[2].lower()
        unique_countries_in_xml.add(country_name)
        
        # Verify Mapping Logic
        country_iso = None
        if country_name in manual_map:
            country_iso = manual_map[country_name]
        elif country_name in country_map:
            country_iso = country_map[country_name]
            
        if country_iso:
            mapped_countries.add(f"{country_name} -> {country_iso}")
        else:
            skipped_countries.add(country_name)

    print("\n--- AUDIT RESULTS ---")
    print(f"Total Unique Countries in Feed: {len(unique_countries_in_xml)}")
    print(f"Successfully Mapped: {len(mapped_countries)}")
    print(f"SKIPPED / MISSING MAPPINGS: {len(skipped_countries)}")
    
    if skipped_countries:
        print("\n[!] The following countries are in the Airalo feed but NOT in your database:")
        for c in sorted(list(skipped_countries)):
            print(f"  - {c}")
            
    # Propose Fixes
    print("\n--- PROPOSED FIXES for src/process_data.py ---")
    print("Add these to manual_map:")
    for c in sorted(list(skipped_countries)):
        print(f'    "{c}": "XX", # TODO: Fill Code')

if __name__ == "__main__":
    audit_feed()
