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
    data_path = project_root / "data" / "esim_data.json"
    templates_path = project_root / "templates"
    output_path = project_root / "docs"
    
    # Create output directory if it doesn't exist
    output_path.mkdir(exist_ok=True)
    
    # Load JSON data
    print(f"Loading data from {data_path}...")
    with open(data_path, 'r', encoding='utf-8') as f:
        countries_data = json.load(f)
    
    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader(str(templates_path)))
    index_template = env.get_template('index.html')
    country_template = env.get_template('country.html')
    
    # Generate index.html homepage
    countries_list = [country_data['country'] for country_data in countries_data]
    index_html = index_template.render(countries=countries_list)
    index_file = output_path / "index.html"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_html)
    generated_count = 1
    print(f"Generated: index.html")
    
    # Define standard data amounts and providers
    standard_data_amounts = ["1GB", "3GB", "5GB", "10GB", "Unlimited"]
    all_providers = ["Airalo", "Maya Mobile", "Nomad", "Holafly", "Klook"]
    
    # Provider-specific benefits mapping
    provider_benefits = {
        'Airalo': ['⚡ 5G Speed', '📅 30 Days'],
        'Maya Mobile': ['⚡ 5G Speed', '📅 30 Days'],
        'Nomad': ['⚡ 5G Speed', '📅 30 Days'],
        'Holafly': ['⚡ 5G Speed', '📅 30 Days'],
        'Klook': ['⚡ 5G Speed', '📅 30 Days']
    }
    
    # Provider logo URLs (Clearbit API)
    provider_logos = {
        'Airalo': 'https://logo.clearbit.com/airalo.com',
        'Maya Mobile': 'https://logo.clearbit.com/maya.net',
        'Nomad': 'https://logo.clearbit.com/getnomad.app',
        'Holafly': 'https://logo.clearbit.com/holafly.com',
        'Klook': 'https://logo.clearbit.com/klook.com'
    }
    
    # Base price structure (varies by provider and data amount)
    # Format: {provider: {data_amount: base_price}}
    base_prices = {
        'Airalo': {'1GB': 4.50, '3GB': 9.00, '5GB': 12.00, '10GB': 18.00, 'Unlimited': 35.00},
        'Maya Mobile': {'1GB': 5.00, '3GB': 10.00, '5GB': 13.50, '10GB': 20.00, 'Unlimited': 38.00},
        'Nomad': {'1GB': 5.50, '3GB': 11.00, '5GB': 14.00, '10GB': 22.00, 'Unlimited': 40.00},
        'Holafly': {'1GB': 6.00, '3GB': 12.00, '5GB': 15.00, '10GB': 24.00, 'Unlimited': 45.00},
        'Klook': {'1GB': 4.75, '3GB': 9.50, '5GB': 12.50, '10GB': 19.00, 'Unlimited': 36.00}
    }
    
    # Country price multipliers (to vary prices by country)
    country_multipliers = {
        'USA': 1.0,
        'Japan': 1.15,
        'France': 1.05
    }
    
    # Generate HTML for each country
    for country_data in countries_data:
        country = country_data['country']
        multiplier = country_multipliers.get(country, 1.0)
        
        # Generate plans for ALL providers and ALL data amounts
        all_plans = []
        for provider in all_providers:
            for data_amount in standard_data_amounts:
                base_price = base_prices[provider][data_amount]
                final_price = round(base_price * multiplier, 2)
                
                # Generate random rating between 4.5 and 5.0
                rating = round(random.uniform(4.5, 5.0), 1)
                
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
                
                plan = {
                    'name': provider,
                    'price': final_price,
                    'data_amount': data_amount,
                    'link': f"https://example.com/{provider.lower().replace(' ', '-')}-{country.lower()}",
                    'benefits': provider_benefits[provider],
                    'logo_url': provider_logos[provider],
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
        
        # Generate filename (lowercase with .html extension)
        filename = f"{country.lower()}.html"
        output_file = output_path / filename
        
        # Get flag emoji for country
        flag_map = {
            'USA': '🇺🇸',
            'Japan': '🇯🇵',
            'France': '🇫🇷'
        }
        country_flag = flag_map.get(country, '🌍')
        
        # Render template
        html_content = country_template.render(
            country=country,
            country_flag=country_flag,
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
