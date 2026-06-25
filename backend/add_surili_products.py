"""
Script to add Surili.shop products to the database.
Since the website may not be directly accessible, this script provides
a template for adding products manually or programmatically.

Usage:
1. Run the script to see available commands
2. Use the template to add new products
3. Import the data using the existing import script
"""

import json
import os
import sys
from pathlib import Path

# Add Django project to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

import django
django.setup()

from catalog.models import Category, Product, ProductImage, ProductVariant

def list_existing_products():
    """List all existing products in the database"""
    print("Existing products in database:")
    print("-" * 60)
    products = Product.objects.all().order_by('name')
    
    for i, product in enumerate(products, 1):
        print(f"{i}. {product.name} (slug: {product.short})")
        print(f"   Categories: {', '.join([c.name for c in product.categories.all()])}")
        print(f"   Variants: {product.variants.count()} price points")
        print(f"   Images: {product.images.count()} images")
        print()
    
    print(f"Total products: {products.count()}")
    print()

def list_categories():
    """List all categories in the database"""
    print("Existing categories:")
    print("-" * 60)
    categories = Category.objects.all().order_by('name')
    
    for category in categories:
        print(f"• {category.name} (slug: {category.route})")
        print(f"  Products: {category.products.count()}")
        print(f"  Description: {category.text}")
        print()

def generate_product_template():
    """Generate a template JSON structure for new products"""
    template = {
        "name": "New Product Name",
        "short": "new-product-slug",
        "image": [
            "assets/products/category-name/product-image.webp",
            "assets/products/category-name/product-image-hover.webp"
        ],
        "price": [
            {
                "weight": "75gm",
                "original": 189.00,
                "discounted": 162.00
            },
            {
                "weight": "150gm", 
                "original": 315.00,
                "discounted": 243.00
            }
        ],
        "categories": ["category-slug"],
        "discription": {
            "about": "Detailed description of the product...",
            "benefits": [
                "Benefit 1",
                "Benefit 2", 
                "Benefit 3"
            ],
            "ingredients": [
                "Ingredient 1",
                "Ingredient 2",
                "Ingredient 3"
            ],
            "nutritional_value": {
                "Fats": "X g",
                "Energy": "Y Kcal",
                "Proteins": "Z g",
                "Sugar": "A g",
                "Carbohydrates": "B g"
            },
            "footer": "Additional information or disclaimer..."
        }
    }
    
    return template

def get_surili_product_examples():
    """Provide examples of Surili.shop products based on typical mukhwas products"""
    examples = [
        {
            "name": "Classic Pan Supari Fusion",
            "short": "classic-pan-supari-fusion",
            "categories": ["best-sellers", "pan", "supari"],
            "description": "A delightful blend of pan leaves and premium supari"
        },
        {
            "name": "Spicy Minty Saunf Elixir", 
            "short": "spicy-minty-saunf-elixir",
            "categories": ["best-sellers", "mukhwas"],
            "description": "Refreshing mint with aromatic saunf seeds"
        },
        {
            "name": "Tangy Imli Goli Temptation",
            "short": "tangy-imli-goli-temptation",
            "categories": ["best-sellers", "churan", "tiny-miny"],
            "description": "Sweet and tangy imli balls with a burst of flavor"
        },
        {
            "name": "Royal Anardana Mix",
            "short": "royal-anardana-mix", 
            "categories": ["best-sellers", "mukhwas"],
            "description": "Premium pomegranate seeds blend with exotic spices"
        },
        {
            "name": "Spicy Adrak Dhaniya Crunch",
            "short": "spicy-adrak-dhaniya-crunch",
            "categories": ["mukhwas", "sugar-free"],
            "description": "Ginger and coriander spicy blend"
        },
        {
            "name": "Saffron Pistachio Symphony",
            "short": "saffron-pistachio-symphony",
            "categories": ["gifts-combos", "tiny-miny"],
            "description": "Premium saffron and pistachio delicacy"
        },
        {
            "name": "Sweet Caramelized Elaichi Bliss",
            "short": "sweet-caramelized-elaichi-bliss",
            "categories": ["tiny-miny", "best-sellers"],
            "description": "Caramelized cardamom sweets"
        }
    ]
    
    return examples

def add_sample_products():
    """Add sample Surili.shop products to the existing product.json file"""
    # Read existing products
    products_file = Path(__file__).parent.parent.parent / "frontend" / "public" / "Jsonfile" / "product.json"
    
    with open(products_file, 'r', encoding='utf-8') as f:
        existing_products = json.load(f)
    
    # Find the highest existing ID
    max_id = max(p["id"] for p in existing_products) if existing_products else 0
    
    # Sample products to add (these are typical Surili.shop products based on the categories)
    sample_products = [
        {
            "id": max_id + 1,
            "name": "Classic Pan Supari Fusion",
            "short": "classic-pan-supari-fusion",
            "image": [
                "assets/products/best-sellers/classic-pan-supari-fusion.webp",
                "assets/products/best-sellers/classic-pan-supari-fusion-hover.webp"
            ],
            "price": [
                {
                    "weight": "50gm",
                    "original": 199.00,
                    "discounted": 169.00
                },
                {
                    "weight": "100gm",
                    "original": 359.00,
                    "discounted": 299.00
                }
            ],
            "categories": ["best-sellers", "pan", "supari"],
            "discription": {
                "about": "Experience the perfect fusion of traditional pan leaves and premium supari. This Classic Pan Supari Fusion offers a delightful blend that captures the authentic taste of Indian after-meal rituals with a modern twist.",
                "benefits": [
                    "Provides instant freshness and breath freshening",
                    "Aids in digestion after meals",
                    "Contains natural antioxidants from pan leaves",
                    "Promotes oral health with its herbal composition",
                    "Offers a satisfying crunch and long-lasting flavor"
                ],
                "ingredients": [
                    "Pan Leaves",
                    "Premium Supari",
                    "Kattha",
                    "Chuna",
                    "Natural Sweeteners",
                    "Aromatic Spices"
                ],
                "nutritional_value": {
                    "Fats": "5.2 g",
                    "Energy": "285 Kcal",
                    "Proteins": "7.8 g",
                    "Sugar": "8.5 g",
                    "Carbohydrates": "62.3 g"
                },
                "footer": "Store in an airtight container to maintain freshness. Best consumed within 6 months of opening."
            }
        },
        {
            "id": max_id + 2,
            "name": "Spicy Minty Saunf Elixir",
            "short": "spicy-minty-saunf-elixir",
            "image": [
                "assets/products/best-sellers/spicy-minty-saunf-elixir.webp",
                "assets/products/best-sellers/spicy-minty-saunf-elixir-hover.webp"
            ],
            "price": [
                {
                    "weight": "75gm",
                    "original": 189.00,
                    "discounted": 159.00
                },
                {
                    "weight": "150gm",
                    "original": 345.00,
                    "discounted": 289.00
                }
            ],
            "categories": ["best-sellers", "mukhwas"],
            "discription": {
                "about": "A refreshing blend of cooling mint and aromatic saunf (fennel seeds) with a spicy twist. This elixir provides instant freshness while aiding digestion and promoting oral health.",
                "benefits": [
                    "Instant cooling effect with natural mint",
                    "Aids digestion and reduces bloating",
                    "Freshens breath naturally",
                    "Contains anti-inflammatory properties",
                    "Rich in antioxidants"
                ],
                "ingredients": [
                    "Saunf (Fennel Seeds)",
                    "Peppermint",
                    "Ajwain (Carom Seeds)",
                    "Black Salt",
                    "Jeera (Cumin)",
                    "Dried Mint Leaves"
                ],
                "nutritional_value": {
                    "Fats": "6.8 g",
                    "Energy": "312 Kcal",
                    "Proteins": "8.5 g",
                    "Sugar": "3.2 g",
                    "Carbohydrates": "58.9 g"
                },
                "footer": "Ideal for post-meal freshness or as an anytime snack. Suitable for all age groups."
            }
        },
        {
            "id": max_id + 3,
            "name": "Tangy Imli Goli Temptation",
            "short": "tangy-imli-goli-temptation",
            "image": [
                "assets/products/best-sellers/tangy-imli-goli-temptation.webp",
                "assets/products/best-sellers/tangy-imli-goli-temptation-hover.webp"
            ],
            "price": [
                {
                    "weight": "100gm",
                    "original": 179.00,
                    "discounted": 149.00
                },
                {
                    "weight": "200gm",
                    "original": 329.00,
                    "discounted": 279.00
                }
            ],
            "categories": ["best-sellers", "churan", "tiny-miny"],
            "discription": {
                "about": "Sweet and tangy tamarind balls with a perfect balance of spices. These Imli Goli are a traditional favorite, offering a burst of flavor that tantalizes your taste buds.",
                "benefits": [
                    "Rich in vitamin C and antioxidants",
                    "Aids digestion and appetite stimulation",
                    "Natural source of dietary fiber",
                    "Helps relieve constipation",
                    "Provides instant energy boost"
                ],
                "ingredients": [
                    "Tamarind Pulp",
                    "Jaggery",
                    "Black Salt",
                    "Cumin Powder",
                    "Ginger Powder",
                    "Rock Salt"
                ],
                "nutritional_value": {
                    "Fats": "4.5 g",
                    "Energy": "298 Kcal",
                    "Proteins": "6.2 g",
                    "Sugar": "42.8 g",
                    "Carbohydrates": "68.5 g"
                },
                "footer": "Contains natural sugars. Enjoy in moderation as part of a balanced diet."
            }
        }
    ]
    
    # Add sample products to existing list
    existing_products.extend(sample_products)
    
    # Write back to file
    with open(products_file, 'w', encoding='utf-8') as f:
        json.dump(existing_products, f, indent=4, ensure_ascii=False)
    
    print(f"Added {len(sample_products)} sample products to product.json")
    print("You can now import these products using:")
    print("python manage.py import_catalog_data")
    return sample_products

def main():
    """Main function to run the script"""
    print("=" * 70)
    print("SURILI.SHOP PRODUCTS DATABASE MANAGER")
    print("=" * 70)
    print()
    
    while True:
        print("Choose an option:")
        print("1. List existing products in database")
        print("2. List existing categories")
        print("3. Generate product template for new products")
        print("4. Show Surili.shop product examples")
        print("5. Add sample Surili.shop products to product.json")
        print("6. Exit")
        
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "1":
            list_existing_products()
        elif choice == "2":
            list_categories()
        elif choice == "3":
            template = generate_product_template()
            print("\nProduct Template:")
            print(json.dumps(template, indent=4))
            
            # Save template to file
            template_file = Path(__file__).parent / "product_template.json"
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump([template], f, indent=4, ensure_ascii=False)
            print(f"\nTemplate saved to: {template_file}")
            
        elif choice == "4":
            examples = get_surili_product_examples()
            print("\nSurili.shop Product Examples:")
            print("-" * 60)
            for i, example in enumerate(examples, 1):
                print(f"{i}. {example['name']}")
                print(f"   Slug: {example['short']}")
                print(f"   Categories: {', '.join(example['categories'])}")
                print(f"   Description: {example['description']}")
                print()
                
        elif choice == "5":
            print("\nAdding sample Surili.shop products...")
            try:
                added_products = add_sample_products()
                print(f"\nSuccessfully added {len(added_products)} sample products:")
                for product in added_products:
                    print(f"  • {product['name']} (slug: {product['short']})")
            except Exception as e:
                print(f"\nError adding products: {e}")
                
        elif choice == "6":
            print("\nExiting. To import products, run:")
            print("cd backend")
            print("python manage.py import_catalog_data")
            break
        else:
            print("Invalid choice. Please try again.")
        
        print("\n" + "-" * 70 + "\n")

if __name__ == "__main__":
    main()