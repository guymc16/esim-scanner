from PIL import Image
import os

def create_social_card():
    # Paths
    input_path = "docs/static/brand/site-logo.png"
    output_path = "docs/static/brand/social-card.jpg"

    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    # Open Logo
    logo = Image.open(input_path).convert("RGBA")
    
    # Target Dimensions
    W, H = 1200, 630
    
    # Create background (White)
    # You can change (255, 255, 255) to a brand color if desired
    background = Image.new("RGB", (W, H), (255, 255, 255))
    
    # Calculate Center Position
    # Optionally scale logo if it's too big or too small
    # Current logo is ~560x560. 
    # That fits nicely in 630 height with ~35px padding top/bottom.
    # But let's check if we want to resize it slightly smaller to have breathing room
    
    # Target logo height (Increased for visibility)
    target_logo_h = 580
    ratio = target_logo_h / logo.height
    new_w = int(logo.width * ratio)
    new_h = int(logo.height * ratio)
    
    logo_resized = logo.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    x = (W - new_w) // 2
    y = (H - new_h) // 2
    
    # Paste (using alphamask)
    background.paste(logo_resized, (x, y), logo_resized)
    
    # Save
    background.save(output_path, "JPEG", quality=90)
    print(f"Social card created at {output_path}")

if __name__ == "__main__":
    create_social_card()
