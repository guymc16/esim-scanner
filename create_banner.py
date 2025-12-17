from PIL import Image
import os

# Paths
bg_path = r"C:/Users/Michaeli/.gemini/antigravity/brain/9099ba0c-fad2-4e76-a596-244e2713413f/social_background_1765974257437.png"
logo_path = r"docs/static/brand/site-logo.png"
output_path = r"docs/static/brand/social-preview.png"

def create_banner():
    print(f"Opening background: {bg_path}")
    bg = Image.open(bg_path).convert("RGBA")
    
    # Resize background to strictly 1200x630 just in case
    bg = bg.resize((1200, 630), Image.Resampling.LANCZOS)
    
    print(f"Opening logo: {logo_path}")
    if not os.path.exists(logo_path):
        print("Error: Logo file not found!")
        return

    logo = Image.open(logo_path).convert("RGBA")
    
    # Resize logo to be suitable for the banner (e.g., 400px height)
    logo_height = 400
    aspect_ratio = logo.width / logo.height
    logo_width = int(logo_height * aspect_ratio)
    logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
    
    # Calculate center position
    x = (bg.width - logo.width) // 2
    y = (bg.height - logo.height) // 2
    
    # Paste logo onto background (using logo as mask for transparency)
    bg.paste(logo, (x, y), logo)
    
    # Save output
    print(f"Saving to: {output_path}")
    bg.save(output_path, "PNG")
    print("Done!")

if __name__ == "__main__":
    create_banner()
