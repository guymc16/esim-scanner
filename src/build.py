#!/usr/bin/env python3
"""
Static Site Generator for eSIM Comparison Website
Generates HTML pages for each country from JSON data.
"""

import json
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def main():
    # Get the project root directory (parent of src/)
    project_root = Path(__file__).parent.parent
    
    # Define paths
    data_path = project_root / "data" / "esim_data.json"
    templates_path = project_root / "templates"
    output_path = project_root / "public"
    
    # Create output directory if it doesn't exist
    output_path.mkdir(exist_ok=True)
    
    # Load JSON data
    print(f"Loading data from {data_path}...")
    with open(data_path, 'r', encoding='utf-8') as f:
        countries_data = json.load(f)
    
    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader(str(templates_path)))
    base_template = env.get_template('base.html')
    index_template = env.get_template('index.html')
    
    # Generate index.html homepage
    countries_list = [country_data['country'] for country_data in countries_data]
    index_html = index_template.render(countries=countries_list)
    index_file = output_path / "index.html"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_html)
    generated_count = 1
    print(f"Generated: index.html")
    
    # Generate HTML for each country
    for country_data in countries_data:
        country = country_data['country']
        providers = country_data['providers']
        
        # Generate filename (lowercase with .html extension)
        filename = f"{country.lower()}.html"
        output_file = output_path / filename
        
        # Render template
        html_content = base_template.render(
            country=country,
            providers=providers
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

