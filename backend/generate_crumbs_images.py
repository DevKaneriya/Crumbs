"""
Generate and organize product images with Crumbs branding.
This script will create placeholder images for all products in the catalog.
"""

import json
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_crumbs_branded_image(product_name, category, size=(400, 300)):
    """
    Create a placeholder image with Crumbs branding for a product.
    In a real scenario, this would use actual product images.
    For now, we create branded placeholder images.
    """
    # Create a new image with a background color based on category
    category_colors = {
        "sugar-free": (240, 248, 255),  # Alice Blue
        "best-sellers": (255, 250, 240),  # Floral White
        "mukhwas": (255, 245, 238),  # Seashell
        "churan": (240, 255, 240),  # Honeydew
        "supari": (255, 250, 250),  # Snow
        "pan": (245, 245, 220),  # Beige
        "tiny-miny": (255, 250, 205),  # Lemon Chiffon
        "gifts-combos": (248, 248, 255),  # Ghost White
    }
    
    bg_color = category_colors.get(category, (255, 255, 255))
    image = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(image)
    
    # Add Crumbs branding
    try:
        # Try to use a system font
        font_large = ImageFont.truetype("arial.ttf", 32)
        font_medium = ImageFont.truetype("arial.ttf", 20)
        font_small = ImageFont.truetype("arial.ttf", 14)
    except:
        # Fallback to default font
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw Crumbs logo/header
    draw.text((size[0]//2, 40), "CRUMBS", fill=(139, 0, 0), font=font_large, anchor="mm")
    draw.text((size[0]//2, 80), "Premium Indian Digestives", fill=(105, 105, 105), font=font_medium, anchor="mm")
    
    # Draw product name (wrapped)
    wrapped_name = textwrap.fill(product_name, width=20)
    draw.text((size[0]//2, size[1]//2), wrapped_name, fill=(0, 0, 139), font=font_medium, anchor="mm", align="center")
    
    # Draw category
    draw.text((size[0]//2, size[1] - 60), f"Category: {category.replace('-', ' ').title()}", 
              fill=(128, 128, 128), font=font_small, anchor="mm")
    
    # Draw border
    draw.rectangle([10, 10, size[0]-10, size[1]-10], outline=(220, 220, 220), width=2)
    
    return image

def create_hover_image(base_image):
    """
    Create a hover version of the image (slightly different).
    """
    # In a real scenario, this would be a different angle or zoom
    # For now, we just add a hover effect overlay
    hover_image = base_image.copy()
    draw = ImageDraw.Draw(hover_image, 'RGBA')
    
    # Add a semi-transparent overlay
    draw.rectangle([0, 0, hover_image.width, hover_image.height], 
                   fill=(255, 255, 255, 50))
    
    # Add "View Details" text
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except:
        font = ImageFont.load_default()
    
    draw.text((hover_image.width//2, hover_image.height - 30), 
              "View Details", fill=(139, 0, 0), font=font, anchor="mm")
    
    return hover_image

def generate_all_product_images():
    """
    Generate images for all products in the catalog.
    """
    print("Generating Crumbs-branded product images...")
    print("=" * 60)
    
    # Paths
    base_dir = Path(__file__).parent.parent
    product_json = base_dir / "frontend" / "public" / "Jsonfile" / "product.json"
    assets_dir = base_dir / "frontend" / "src" / "assets"
    
    # Read product data
    with open(product_json, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    print(f"Found {len(products)} products in catalog")
    
    # Track statistics
    images_created = 0
    directories_created = 0
    products_processed = 0
    
    # Process each product
    for product in products:
        product_name = product['name']
        slug = product['short']
        categories = product.get('categories', [])
        primary_category = categories[0] if categories else 'mukhwas'
        
        print(f"\nProcessing: {product_name}")
        print(f"  Slug: {slug}, Category: {primary_category}")
        
        # Get image paths from product data
        image_paths = product.get('image', [])
        
        if not image_paths:
            print(f"  Warning: No image paths defined for {product_name}")
            continue
        
        # Create images for this product
        for i, img_path in enumerate(image_paths):
            if img_path.startswith('assets/'):
                # Convert to filesystem path
                rel_path = img_path.replace('assets/', '')
                full_path = assets_dir / rel_path
                
                # Create directory if it doesn't exist
                full_path.parent.mkdir(parents=True, exist_ok=True)
                if not full_path.parent.exists():
                    directories_created += 1
                
                # Create the image
                if '-hover' in str(full_path):
                    # Create hover version
                    base_image_path = str(full_path).replace('-hover', '')
                    if Path(base_image_path).exists():
                        base_image = Image.open(base_image_path)
                        image = create_hover_image(base_image)
                    else:
                        # Create new base image first
                        base_image = create_crumbs_branded_image(product_name, primary_category)
                        image = create_hover_image(base_image)
                else:
                    # Create regular image
                    image = create_crumbs_branded_image(product_name, primary_category)
                
                # Save the image
                image.save(full_path, 'WEBP', quality=85)
                images_created += 1
                print(f"  ✓ Created: {img_path}")
        
        products_processed += 1
    
    print(f"\n" + "=" * 60)
    print("IMAGE GENERATION SUMMARY")
    print("=" * 60)
    print(f"Products processed: {products_processed}")
    print(f"Directories created: {directories_created}")
    print(f"Images created: {images_created}")
    
    # Create a sample HTML preview
    create_image_preview(products, assets_dir)
    
    return images_created

def create_image_preview(products, assets_dir):
    """
    Create an HTML preview of the generated images.
    """
    preview_path = assets_dir.parent / 'products_image_preview.html'
    
    html_content = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Crumbs Product Images Preview</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background: #f5f5f5;
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
                padding: 20px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .product-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                gap: 20px;
            }
            .product-card {
                background: white;
                border-radius: 8px;
                padding: 15px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                transition: transform 0.3s;
            }
            .product-card:hover {
                transform: translateY(-5px);
            }
            .product-image {
                width: 100%;
                height: 200px;
                object-fit: contain;
                background: #f8f8f8;
                border-radius: 5px;
                margin-bottom: 10px;
            }
            .product-name {
                font-weight: bold;
                margin: 10px 0 5px 0;
                color: #333;
            }
            .product-category {
                color: #666;
                font-size: 0.9em;
                margin-bottom: 5px;
            }
            .product-slug {
                color: #888;
                font-size: 0.8em;
                font-family: monospace;
            }
            .image-count {
                background: #4CAF50;
                color: white;
                padding: 2px 8px;
                border-radius: 10px;
                font-size: 0.8em;
                display: inline-block;
                margin-top: 5px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🛍️ Crumbs Product Images Preview</h1>
            <p>Generated product images with Crumbs branding</p>
            <p>Total Products: ''' + str(len(products)) + '''</p>
        </div>
        
        <div class="product-grid">
    '''
    
    # Add product cards
    for product in products[:20]:  # Show first 20 for preview
        product_name = product['name']
        slug = product['short']
        categories = ', '.join(product.get('categories', []))
        image_paths = product.get('image', [])
        
        # Get first image path if available
        first_image = ''
        if image_paths:
            first_image = image_paths[0].replace('assets/', '../src/assets/')
        
        html_content += f'''
            <div class="product-card">
                <div class="product-name">{product_name}</div>
                <div class="product-category">{categories}</div>
                <div class="product-slug">{slug}</div>
                <span class="image-count">{len(image_paths)} images</span>
        '''
        
        if first_image and Path(assets_dir.parent.parent / first_image.replace('../', '')).exists():
            html_content += f'<img src="{first_image}" class="product-image" alt="{product_name}">'
        else:
            html_content += f'<div class="product-image" style="display: flex; align-items: center; justify-content: center; color: #999;">Image Preview</div>'
        
        html_content += '</div>'
    
    html_content += '''
        </div>
        
        <div style="margin-top: 40px; padding: 20px; background: white; border-radius: 10px;">
            <h2>📁 Image Directory Structure</h2>
            <pre style="background: #f8f8f8; padding: 15px; border-radius: 5px; overflow: auto;">
    frontend/src/assets/products/
    ├── sugar-free/
    │   ├── digestive-mukhwas.webp
    │   ├── digestive-mukhwas-hover.webp
    │   └── ...
    ├── mukhwas/
    ├── churan/
    ├── supari/
    ├── pan/
    ├── tiny-miny/
    └── gifts-combos/
            </pre>
        </div>
        
        <div style="margin-top: 20px; padding: 20px; background: white; border-radius: 10px;">
            <h2>🎨 Image Specifications</h2>
            <ul>
                <li><strong>Format:</strong> WEBP (modern, efficient format)</li>
                <li><strong>Size:</strong> 400x300 pixels</li>
                <li><strong>Quality:</strong> 85% (optimal balance)</li>
                <li><strong>Branding:</strong> All images feature "Crumbs" branding</li>
                <li><strong>Categories:</strong> Color-coded by product category</li>
                <li><strong>Hover Images:</strong> Special hover versions created</li>
            </ul>
        </div>
    </body>
    </html>
    '''
    
    with open(preview_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\n📊 Preview created: {preview_path}")
    print("Open this file in a browser to see the image preview.")

def check_existing_images():
    """
    Check which images already exist and which need to be created.
    """
    print("Checking existing product images...")
    print("=" * 60)
    
    base_dir = Path(__file__).parent.parent
    product_json = base_dir / "frontend" / "public" / "Jsonfile" / "product.json"
    assets_dir = base_dir / "frontend" / "src" / "assets"
    
    with open(product_json, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    total_images_needed = 0
    existing_images = 0
    missing_images = 0
    
    for product in products:
        image_paths = product.get('image', [])
        total_images_needed += len(image_paths)
        
        for img_path in image_paths:
            if img_path.startswith('assets/'):
                rel_path = img_path.replace('assets/', '')
                full_path = assets_dir / rel_path
                
                if full_path.exists():
                    existing_images += 1
                else:
                    missing_images += 1
    
    print(f"Total products: {len(products)}")
    print(f"Total image references: {total_images_needed}")
    print(f"Existing images: {existing_images}")
    print(f"Missing images: {missing_images}")
    print(f"Completion: {existing_images/total_images_needed*100:.1f}%")
    
    return missing_images

def main():
    """
    Main function to manage image generation.
    """
    print("🛍️ CRUMBS PRODUCT IMAGE GENERATION SYSTEM")
    print("=" * 60)
    
    # Check if Pillow is installed
    try:
        from PIL import Image, ImageDraw, ImageFont
        print("✓ Pillow library is available for image generation")
    except ImportError:
        print("✗ Pillow library is not installed")
        print("\nTo install Pillow, run:")
        print("pip install Pillow")
        print("\nAlternatively, we can create image placeholders without Pillow.")
        response = input("\nContinue with basic image generation? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Check existing images
    missing_count = check_existing_images()
    
    if missing_count == 0:
        print("\n✅ All product images already exist!")
        response = input("Regenerate all images? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Generate images
    print(f"\nGenerating {missing_count} missing images...")
    images_created = generate_all_product_images()
    
    print(f"\n🎉 Image generation complete!")
    print(f"Created {images_created} Crumbs-branded product images.")
    print("\nNext steps:")
    print("1. Open products_image_preview.html to see the generated images")
    print("2. Update your frontend to display the new product images")
    print("3. Consider replacing placeholders with actual product photos")

if __name__ == "__main__":
    main()