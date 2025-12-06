#!/usr/bin/env python3
"""
Static Site Generator for eSIM Comparison Website
Generates HTML pages for each country from JSON data.
"""

import json
import re
import random
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def main():
    # Get the project root directory (parent of src/)
    project_root = Path(__file__).parent.parent
    
    # Define paths
    providers_path = project_root / "data" / "providers.json"
    countries_path = project_root / "data" / "countries.json"
    templates_path = project_root / "templates"
    output_path = project_root / "docs"
    
    # Create output directory if it doesn't exist
    output_path.mkdir(exist_ok=True)
    
    # Load JSON data
    print(f"Loading providers from {providers_path}...")
    with open(providers_path, 'r', encoding='utf-8') as f:
        providers_data = json.load(f)
    
    print(f"Loading countries from {countries_path}...")
    with open(countries_path, 'r', encoding='utf-8') as f:
        countries_data = json.load(f)
    
    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader(str(templates_path)))
    index_template = env.get_template('index.html')
    country_template = env.get_template('country.html')
    
    # Standard data amounts
    standard_data_amounts = ["1GB", "3GB", "5GB", "10GB", "Unlimited"]
    
    # Country price multipliers (to vary prices by country)
    # Base multiplier is 1.0, adjust for specific countries
    country_multipliers = {
        'USA': 1.0,
        'Japan': 1.15,
        'France': 1.05,
        'Switzerland': 1.20,
        'United Arab Emirates': 1.10
    }
    
    # Generate index.html homepage
    # Template will show top 9 from all_countries
    all_countries = countries_data
    index_html = index_template.render(
        all_countries=all_countries
    )
    index_file = output_path / "index.html"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_html)
    generated_count = 1
    print(f"Generated: index.html")
    
    # Generate HTML for each country
    for country_info in countries_data:
        country_name = country_info['name']
        country_slug = country_info['slug']
        country_code = country_info.get('code', '')
        image_url = country_info.get('image_url', '')
        intro_text = country_info.get('intro_text', '')
        multiplier = country_multipliers.get(country_name, 1.0)
        
        # Generate plans for ALL providers and ALL data amounts
        all_plans = []
        for provider_info in providers_data:
            provider_name = provider_info['name']
            base_prices = provider_info['base_prices']
            base_rating = provider_info['base_rating']
            
            for data_amount in standard_data_amounts:
                base_price = base_prices[data_amount]
                final_price = round(base_price * multiplier, 2)
                
                # Generate random rating around base rating (between base_rating and 5.0)
                rating = round(random.uniform(base_rating, 5.0), 1)
                
                # Generate random review count (formatted)
                review_counts = [
                    random.randint(200, 999),
                    f"{random.randint(1, 9)}.{random.randint(0, 9)}k",
                    f"{random.randint(10, 99)}k"
                ]
                review_count = random.choice(review_counts)
                if isinstance(review_count, int):
                    review_count_str = str(review_count)
                else:
                    review_count_str = review_count
                
                # Generate affiliate link
                affiliate_link = provider_info['affiliate_link_template'].format(
                    country_slug=country_slug
                )
                
                plan = {
                    'name': provider_name,
                    'price': final_price,
                    'data_amount': data_amount,
                    'link': affiliate_link,
                    'benefits': provider_info['benefits'],
                    'logo_url': provider_info['logo_url'],
                    'rating': rating,
                    'review_count': review_count_str
                }
                all_plans.append(plan)
        
        # Group plans by data_amount
        grouped_plans = {}
        for plan in all_plans:
            data_amount = plan['data_amount']
            if data_amount not in grouped_plans:
                grouped_plans[data_amount] = []
            grouped_plans[data_amount].append(plan)
        
        # Sort data amounts logically (smallest to largest, "Unlimited" last)
        def sort_key(data_amount):
            if data_amount.lower() == 'unlimited':
                return float('inf')
            # Extract numeric value (handles "1GB", "3GB", "10GB", etc.)
            match = re.search(r'(\d+\.?\d*)', data_amount)
            if match:
                return float(match.group(1))
            return 0
        
        sorted_data_amounts = sorted(grouped_plans.keys(), key=sort_key)
        
        # Find cheapest plan in each group and mark it
        grouped_plans_sorted = []
        for data_amount in sorted_data_amounts:
            plans = grouped_plans[data_amount]
            # Find the cheapest plan
            cheapest_plan = min(plans, key=lambda p: p['price'])
            # Mark it as cheapest
            cheapest_plan['is_cheapest'] = True
            # Mark others as not cheapest
            for plan in plans:
                if plan != cheapest_plan:
                    plan['is_cheapest'] = False
            
            grouped_plans_sorted.append({
                'data_amount': data_amount,
                'plans': plans
            })
        
        # Generate filename using slug
        filename = f"{country_slug}.html"
        output_file = output_path / filename
        
        # Render template
        html_content = country_template.render(
            country=country_name,
            country_code=country_code,
            country_slug=country_slug,
            image_url=image_url,
            intro_text=intro_text,
            grouped_plans=grouped_plans_sorted
        )
        
        # Write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        generated_count += 1
        print(f"Generated: {filename}")
    
    # Print success message
    print(f"\n✓ Generated {generated_count} pages in {output_path}")


if __name__ == "__main__":
    main()
