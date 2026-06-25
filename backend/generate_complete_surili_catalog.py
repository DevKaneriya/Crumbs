"""
Generate a complete Surili.shop product catalog with variants and images.
Based on typical Indian mukhwas, churan, supari, and digestive products.
"""

import json
import os
from pathlib import Path

def generate_complete_catalog():
    """Generate a complete catalog of Surili.shop products"""
    
    # Base on existing categories
    categories = {
        "sugar-free": "Sugar Free",
        "best-sellers": "Much Loved Treats", 
        "mukhwas": "Mukhwas",
        "churan": "Churan",
        "supari": "Supari",
        "pan": "Pan",
        "tiny-miny": "Tiny Miny",
        "gifts-combos": "Gifts & Combos"
    }
    
    # Complete product catalog for Surili.shop
    products = [
        # Sugar-Free Category (Core Products)
        {
            "name": "Sugar-Free Digestive Mukhwas",
            "slug": "sugar-free-digestive-mukhwas",
            "categories": ["sugar-free", "mukhwas"],
            "description": "Traditional digestive mukhwas made without added sugar. Perfect for diabetics and health-conscious individuals.",
            "variants": [
                {"weight": "75gm", "original": 189, "discounted": 162},
                {"weight": "150gm", "original": 345, "discounted": 295},
                {"weight": "300gm", "original": 659, "discounted": 569}
            ]
        },
        {
            "name": "Zero Sugar Saunf Mix",
            "slug": "zero-sugar-saunf-mix",
            "categories": ["sugar-free", "mukhwas"],
            "description": "Pure fennel seeds with digestive herbs, completely sugar-free.",
            "variants": [
                {"weight": "100gm", "original": 199, "discounted": 169},
                {"weight": "200gm", "original": 379, "discounted": 329}
            ]
        },
        {
            "name": "Diabetic Friendly Ajwain Crunch",
            "slug": "diabetic-friendly-ajwain-crunch",
            "categories": ["sugar-free", "mukhwas"],
            "description": "Carom seeds blend for digestion, suitable for diabetics.",
            "variants": [
                {"weight": "80gm", "original": 179, "discounted": 149},
                {"weight": "160gm", "original": 339, "discounted": 289}
            ]
        },
        
        # Best Sellers / Much Loved Treats
        {
            "name": "Royal Pan Masala",
            "slug": "royal-pan-masala",
            "categories": ["best-sellers", "pan"],
            "description": "Premium pan masala with silver leaf, a customer favorite.",
            "variants": [
                {"weight": "50gm", "original": 299, "discounted": 249},
                {"weight": "100gm", "original": 559, "discounted": 479},
                {"weight": "200gm", "original": 1099, "discounted": 949}
            ]
        },
        {
            "name": "Magic Mint Mukhwas",
            "slug": "magic-mint-mukhwas",
            "categories": ["best-sellers", "mukhwas"],
            "description": "Mint-infused mukhwas that leaves breath fresh for hours.",
            "variants": [
                {"weight": "90gm", "original": 219, "discounted": 189},
                {"weight": "180gm", "original": 419, "discounted": 369}
            ]
        },
        {
            "name": "Golden Elaichi Delight",
            "slug": "golden-elaichi-delight",
            "categories": ["best-sellers", "tiny-miny"],
            "description": "Cardamom sweets coated with edible gold dust.",
            "variants": [
                {"weight": "70gm", "original": 249, "discounted": 219},
                {"weight": "140gm", "original": 479, "discounted": 419}
            ]
        },
        
        # Mukhwas Category
        {
            "name": "Traditional Mixed Seeds Mukhwas",
            "slug": "traditional-mixed-seeds-mukhwas",
            "categories": ["mukhwas"],
            "description": "Classic blend of fennel, sesame, coconut, and coriander seeds.",
            "variants": [
                {"weight": "100gm", "original": 189, "discounted": 159},
                {"weight": "200gm", "original": 359, "discounted": 309},
                {"weight": "500gm", "original": 859, "discounted": 759}
            ]
        },
        {
            "name": "Rose Petal Special",
            "slug": "rose-petal-special",
            "categories": ["mukhwas"],
            "description": "Mukhwas with dried rose petals for aromatic freshness.",
            "variants": [
                {"weight": "85gm", "original": 219, "discounted": 189},
                {"weight": "170gm", "original": 419, "discounted": 369}
            ]
        },
        {
            "name": "Saffron Infused Mukhwas",
            "slug": "saffron-infused-mukhwas",
            "categories": ["mukhwas", "gifts-combos"],
            "description": "Premium mukhwas infused with real saffron strands.",
            "variants": [
                {"weight": "60gm", "original": 399, "discounted": 349},
                {"weight": "120gm", "original": 759, "discounted": 679}
            ]
        },
        
        # Churan Category
        {
            "name": "Amchur Imli Churan",
            "slug": "amchur-imli-churan",
            "categories": ["churan"],
            "description": "Tamarind and dry mango powder digestive churan.",
            "variants": [
                {"weight": "100gm", "original": 149, "discounted": 129},
                {"weight": "200gm", "original": 279, "discounted": 239},
                {"weight": "500gm", "original": 659, "discounted": 579}
            ]
        },
        {
            "name": "Jeera Goli Digestive",
            "slug": "jeera-goli-digestive",
            "categories": ["churan", "tiny-miny"],
            "description": "Cumin seed digestive balls for instant relief.",
            "variants": [
                {"weight": "120gm", "original": 179, "discounted": 149},
                {"weight": "240gm", "original": 339, "discounted": 289}
            ]
        },
        {
            "name": "Panchratna Churan",
            "slug": "panchratna-churan",
            "categories": ["churan"],
            "description": "Five-herb digestive powder for complete digestive health.",
            "variants": [
                {"weight": "150gm", "original": 199, "discounted": 169},
                {"weight": "300gm", "original": 379, "discounted": 329}
            ]
        },
        
        # Supari Category
        {
            "name": "Premium Meetha Supari",
            "slug": "premium-meetha-supari",
            "categories": ["supari"],
            "description": "Sweetened betel nut with natural flavors.",
            "variants": [
                {"weight": "50gm", "original": 159, "discounted": 139},
                {"weight": "100gm", "original": 299, "discounted": 259},
                {"weight": "200gm", "original": 579, "discounted": 499}
            ]
        },
        {
            "name": "Scented Chocolate Supari",
            "slug": "scented-chocolate-supari",
            "categories": ["supari", "tiny-miny"],
            "description": "Chocolate-flavored scented supari for modern tastes.",
            "variants": [
                {"weight": "60gm", "original": 199, "discounted": 169},
                {"weight": "120gm", "original": 379, "discounted": 329}
            ]
        },
        {
            "name": "Traditional Katha Supari",
            "slug": "traditional-katha-supari",
            "categories": ["supari", "pan"],
            "description": "Classic supari with katha for authentic taste.",
            "variants": [
                {"weight": "75gm", "original": 179, "discounted": 149},
                {"weight": "150gm", "original": 339, "discounted": 289}
            ]
        },
        
        # Pan Category
        {
            "name": "Special Meetha Pan",
            "slug": "special-meetha-pan",
            "categories": ["pan"],
            "description": "Sweet pan preparation with natural sweeteners.",
            "variants": [
                {"weight": "100gm", "original": 249, "discounted": 219},
                {"weight": "200gm", "original": 479, "discounted": 419}
            ]
        },
        {
            "name": "Sada Pan Mix",
            "slug": "sada-pan-mix",
            "categories": ["pan"],
            "description": "Plain pan mixture without sweeteners.",
            "variants": [
                {"weight": "90gm", "original": 199, "discounted": 169},
                {"weight": "180gm", "original": 379, "discounted": 329}
            ]
        },
        {
            "name": "Chocolate Pan Fusion",
            "slug": "chocolate-pan-fusion",
            "categories": ["pan", "tiny-miny"],
            "description": "Innovative chocolate and pan fusion.",
            "variants": [
                {"weight": "80gm", "original": 229, "discounted": 199},
                {"weight": "160gm", "original": 439, "discounted": 389}
            ]
        },
        
        # Tiny Miny Category
        {
            "name": "Colorful Sugar Balls",
            "slug": "colorful-sugar-balls",
            "categories": ["tiny-miny"],
            "description": "Vibrant colored sugar balls for festive occasions.",
            "variants": [
                {"weight": "100gm", "original": 129, "discounted": 109},
                {"weight": "200gm", "original": 249, "discounted": 219},
                {"weight": "500gm", "original": 599, "discounted": 529}
            ]
        },
        {
            "name": "Mini Chocolate Coated Nuts",
            "slug": "mini-chocolate-coated-nuts",
            "categories": ["tiny-miny", "gifts-combos"],
            "description": "Chocolate-coated almonds and cashews in bite-sized pieces.",
            "variants": [
                {"weight": "120gm", "original": 299, "discounted": 259},
                {"weight": "240gm", "original": 579, "discounted": 499}
            ]
        },
        {
            "name": "Rainbow Confectionery Mix",
            "slug": "rainbow-confectionery-mix",
            "categories": ["tiny-miny"],
            "description": "Assorted colorful candies and sweets mix.",
            "variants": [
                {"weight": "150gm", "original": 179, "discounted": 149},
                {"weight": "300gm", "original": 339, "discounted": 289}
            ]
        },
        
        # Gifts & Combos Category
        {
            "name": "Premium Gift Hamper",
            "slug": "premium-gift-hamper",
            "categories": ["gifts-combos"],
            "description": "Luxury gift hamper with assorted mukhwas and sweets.",
            "variants": [
                {"weight": "500gm", "original": 1299, "discounted": 1149},
                {"weight": "1kg", "original": 2499, "discounted": 2199}
            ]
        },
        {
            "name": "Diwali Special Combo",
            "slug": "diwali-special-combo",
            "categories": ["gifts-combos"],
            "description": "Festive combo pack for Diwali celebrations.",
            "variants": [
                {"weight": "750gm", "original": 899, "discounted": 799},
                {"weight": "1.5kg", "original": 1699, "discounted": 1499}
            ]
        },
        {
            "name": "Wedding Return Gift Pack",
            "slug": "wedding-return-gift-pack",
            "categories": ["gifts-combos"],
            "description": "Elegant packaging for wedding return gifts.",
            "variants": [
                {"weight": "250gm", "original": 499, "discounted": 449},
                {"weight": "500gm", "original": 949, "discounted": 849}
            ]
        },
        
        # Additional popular products
        {
            "name": "Honey Coated Mukhwas",
            "slug": "honey-coated-mukhwas",
            "categories": ["best-sellers", "mukhwas"],
            "description": "Natural honey-coated seeds for sweetness without sugar.",
            "variants": [
                {"weight": "95gm", "original": 229, "discounted": 199},
                {"weight": "190gm", "original": 439, "discounted": 389}
            ]
        },
        {
            "name": "Cinnamon Spice Mix",
            "slug": "cinnamon-spice-mix",
            "categories": ["mukhwas", "sugar-free"],
            "description": "Cinnamon and spice blend for warming digestion.",
            "variants": [
                {"weight": "85gm", "original": 199, "discounted": 169},
                {"weight": "170gm", "original": 379, "discounted": 329}
            ]
        },
        {
            "name": "Lemon Mint Refresher",
            "slug": "lemon-mint-refresher",
            "categories": ["best-sellers", "mukhwas"],
            "description": "Lemon and mint combination for ultimate freshness.",
            "variants": [
                {"weight": "100gm", "original": 209, "discounted": 179},
                {"weight": "200gm", "original": 399, "discounted": 349}
            ]
        },
        {
            "name": "Dry Fruit Delight",
            "slug": "dry-fruit-delight",
            "categories": ["gifts-combos", "tiny-miny"],
            "description": "Premium dry fruits coated with edible silver.",
            "variants": [
                {"weight": "125gm", "original": 349, "discounted": 299},
                {"weight": "250gm", "original": 679, "discounted": 599}
            ]
        },
        {
            "name": "Ayurvedic Digestive Mix",
            "slug": "ayurvedic-digestive-mix",
            "categories": ["churan", "sugar-free"],
            "description": "Ancient Ayurvedic formula for digestive health.",
            "variants": [
                {"weight": "110gm", "original": 239, "discounted": 209},
                {"weight": "220gm", "original": 459, "discounted": 399}
            ]
        }
    ]
    
    return products

def create_product_json(products, start_id=17):
    """Convert product data to JSON format matching your schema"""
    product_json = []
    
    for i, product in enumerate(products, start_id):
        # Generate image paths based on first category
        primary_category = product["categories"][0]
        slug = product["slug"]
        
        # Create image array (2-3 images per product)
        images = [
            f"assets/products/{primary_category}/{slug}.webp",
            f"assets/products/{primary_category}/{slug}-hover.webp"
        ]
        
        # Add third image for some products
        if i % 3 == 0:
            images.append(f"assets/products/{primary_category}/{slug}-3.webp")
        
        # Create product JSON
        product_data = {
            "id": i,
            "name": product["name"],
            "short": slug,
            "image": images,
            "price": product["variants"],
            "categories": product["categories"]
        }
        
        # Add description for all products
        product_data["discription"] = {
            "about": product["description"],
            "benefits": [
                "Aids digestion and promotes gut health",
                "Freshens breath naturally",
                "Contains natural antioxidants",
                "Helps regulate appetite",
                "Supports overall digestive wellness"
            ],
            "ingredients": [
                "Natural Herbs and Seeds",
                "Traditional Spices",
                "Premium Quality Ingredients",
                "No Artificial Colors",
                "No Preservatives"
            ],
            "nutritional_value": {
                "Fats": "5-8 g",
                "Energy": "280-320 Kcal",
                "Proteins": "7-10 g",
                "Sugar": "2-10 g",
                "Carbohydrates": "55-65 g"
            },
            "footer": "Store in an airtight container in a cool, dry place. Best consumed within 6 months of opening. Contains natural ingredients."
        }
        
        product_json.append(product_data)
    
    return product_json

def main():
    """Main function to generate and save the complete catalog"""
    print("Generating complete Surili.shop product catalog...")
    
    # Generate products
    products = generate_complete_catalog()
    
    # Convert to JSON format
    product_json = create_product_json(products, start_id=17)
    
    # Read existing products
    existing_file = Path(__file__).parent.parent / "frontend" / "public" / "Jsonfile" / "product.json"
    
    try:
        with open(existing_file, 'r', encoding='utf-8') as f:
            existing_products = json.load(f)
        existing_count = len(existing_products)
    except:
        existing_products = []
        existing_count = 0
    
    # Merge products (avoid duplicates)
    existing_slugs = {p['short'] for p in existing_products}
    new_products = []
    
    for product in product_json:
        if product['short'] not in existing_slugs:
            new_products.append(product)
            existing_slugs.add(product['short'])
    
    # Combine all products
    all_products = existing_products + new_products
    
    # Save to file
    with open(existing_file, 'w', encoding='utf-8') as f:
        json.dump(all_products, f, indent=4, ensure_ascii=False)
    
    print(f"\nCatalog generation complete!")
    print(f"Existing products: {existing_count}")
    print(f"New products added: {len(new_products)}")
    print(f"Total products now: {len(all_products)}")
    
    # Save new products to separate file for reference
    new_file = Path(__file__).parent / "complete_surili_catalog.json"
    with open(new_file, 'w', encoding='utf-8') as f:
        json.dump(new_products, f, indent=4, ensure_ascii=False)
    
    print(f"\nNew products saved to: {new_file}")
    
    # Print summary by category
    print("\nProduct distribution by category:")
    category_counts = {}
    for product in all_products:
        for category in product['categories']:
            category_counts[category] = category_counts.get(category, 0) + 1
    
    for category, count in sorted(category_counts.items()):
        print(f"  {category}: {count} products")
    
    print(f"\nTo import these products into your database, run:")
    print("cd backend")
    print("python manage.py import_catalog_data --categories ../frontend/public/Jsonfile/categories.json --products ../frontend/public/Jsonfile/product.json")

if __name__ == "__main__":
    main()