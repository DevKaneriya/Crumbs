"""
Web scraping utility for Surili.shop products.
This script provides functions to scrape product data from the Surili.shop website.

Note: Use responsibly and respect the website's terms of service.
"""

import json
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse
import re

class SuriliScraper:
    def __init__(self, base_url="https://surili.shop"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
        })
    
    def get_all_product_links(self):
        """Extract all product links from the products page"""
        print(f"Fetching products page: {self.base_url}/collections/all-products")
        
        try:
            response = self.session.get(f"{self.base_url}/collections/all-products", timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for product links - these patterns are common for e-commerce sites
            product_links = []
            
            # Try different selectors for product links
            selectors = [
                'a[href*="/products/"]',
                'a.product-card',
                '.product-item a',
                'a[href*="/collections/all-products/products/"]',
                'div.product a',
            ]
            
            for selector in selectors:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href', '')
                    if href and '/products/' in href:
                        full_url = urljoin(self.base_url, href)
                        if full_url not in product_links:
                            product_links.append(full_url)
            
            # Also check for JSON data in script tags (common in Shopify stores)
            script_tags = soup.find_all('script', type='application/json')
            for script in script_tags:
                try:
                    data = json.loads(script.string)
                    # Look for product data in the JSON
                    if isinstance(data, dict):
                        self._extract_products_from_json(data, product_links)
                except:
                    continue
            
            # Remove duplicates
            product_links = list(set(product_links))
            
            print(f"Found {len(product_links)} product links")
            return product_links
            
        except Exception as e:
            print(f"Error fetching product links: {e}")
            return []
    
    def _extract_products_from_json(self, data, product_links):
        """Extract product links from JSON data"""
        # This is a simplified approach - Shopify stores often have product data in JSON
        if 'products' in data:
            for product in data['products']:
                if 'handle' in product:
                    product_url = f"{self.base_url}/products/{product['handle']}"
                    product_links.append(product_url)
    
    def scrape_product_details(self, product_url):
        """Scrape detailed product information from a product page"""
        print(f"Scraping product: {product_url}")
        
        try:
            response = self.session.get(product_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            product_data = {
                'url': product_url,
                'name': '',
                'price': [],
                'description': '',
                'images': [],
                'categories': [],
                'metadata': {}
            }
            
            # Extract product name
            name_selectors = [
                'h1.product-title',
                'h1.product__title',
                'h1[itemprop="name"]',
                'h1.product-single__title',
                'div.product-title h1',
            ]
            
            for selector in name_selectors:
                element = soup.select_one(selector)
                if element:
                    product_data['name'] = element.get_text(strip=True)
                    break
            
            # Extract price
            price_selectors = [
                'span.price',
                'span.product-price',
                'span.money',
                'meta[itemprop="price"]',
                'div.price__regular',
                'span.price-item--regular',
            ]
            
            for selector in price_selectors:
                elements = soup.select(selector)
                for element in elements:
                    price_text = element.get_text(strip=True)
                    # Extract numeric price
                    price_match = re.search(r'[\d,.]+', price_text)
                    if price_match:
                        try:
                            price = float(price_match.group().replace(',', ''))
                            product_data['price'].append({
                                'weight': 'default',
                                'original': price,
                                'discounted': price
                            })
                        except:
                            pass
            
            # Extract description
            desc_selectors = [
                'div.product-description',
                'div.product__description',
                'div.description',
                'div[itemprop="description"]',
                'div.product-single__description',
            ]
            
            for selector in desc_selectors:
                element = soup.select(selector)
                if element:
                    product_data['description'] = element[0].get_text(strip=True, separator='\n')
                    break
            
            # Extract images
            img_selectors = [
                'img[src*="products"]',
                'img.product-featured-image',
                'div.product-gallery img',
                'img.product__image',
            ]
            
            for selector in img_selectors:
                elements = soup.select(selector)
                for img in elements:
                    src = img.get('src', '') or img.get('data-src', '')
                    if src and ('products' in src or 'product' in src):
                        if src.startswith('//'):
                            src = 'https:' + src
                        elif src.startswith('/'):
                            src = urljoin(self.base_url, src)
                        if src not in product_data['images']:
                            product_data['images'].append(src)
            
            # Extract categories from breadcrumbs or tags
            breadcrumb_selectors = [
                'nav.breadcrumb a',
                'div.breadcrumb a',
                'span.breadcrumb a',
                'a.breadcrumb__item',
            ]
            
            for selector in breadcrumb_selectors:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text(strip=True)
                    if text and text.lower() not in ['home', 'products', 'collections', 'all']:
                        product_data['categories'].append(text.lower().replace(' ', '-'))
            
            # Look for JSON-LD data (structured data)
            json_ld = soup.find('script', type='application/ld+json')
            if json_ld:
                try:
                    ld_data = json.loads(json_ld.string)
                    if '@type' in ld_data and ld_data['@type'] == 'Product':
                        self._extract_from_json_ld(ld_data, product_data)
                except:
                    pass
            
            # Generate slug from URL or name
            if product_data['name']:
                slug = product_data['name'].lower().replace(' ', '-').replace('--', '-')
                slug = re.sub(r'[^a-z0-9-]', '', slug)
                product_data['slug'] = slug
            
            return product_data
            
        except Exception as e:
            print(f"Error scraping product {product_url}: {e}")
            return None
    
    def _extract_from_json_ld(self, ld_data, product_data):
        """Extract product data from JSON-LD structured data"""
        if 'name' in ld_data and not product_data['name']:
            product_data['name'] = ld_data['name']
        
        if 'description' in ld_data and not product_data['description']:
            product_data['description'] = ld_data['description']
        
        if 'image' in ld_data:
            if isinstance(ld_data['image'], str):
                product_data['images'].append(ld_data['image'])
            elif isinstance(ld_data['image'], list):
                product_data['images'].extend(ld_data['image'])
        
        if 'offers' in ld_data:
            if isinstance(ld_data['offers'], dict) and 'price' in ld_data['offers']:
                try:
                    price = float(ld_data['offers']['price'])
                    product_data['price'].append({
                        'weight': 'default',
                        'original': price,
                        'discounted': price
                    })
                except:
                    pass
    
    def convert_to_catalog_format(self, scraped_products):
        """Convert scraped product data to your catalog format"""
        catalog_products = []
        
        # Read existing products to get next ID
        try:
            with open('../frontend/public/Jsonfile/product.json', 'r', encoding='utf-8') as f:
                existing_products = json.load(f)
            next_id = max(p['id'] for p in existing_products) + 1 if existing_products else 1
        except:
            next_id = 1
        
        for scraped in scraped_products:
            if not scraped['name']:
                continue
            
            # Map to your catalog format
            catalog_product = {
                'id': next_id,
                'name': scraped['name'],
                'short': scraped.get('slug', scraped['name'].lower().replace(' ', '-')),
                'image': [],
                'price': [],
                'categories': scraped.get('categories', ['all-products']),
                'discription': {
                    'about': scraped.get('description', ''),
                    'benefits': [],
                    'ingredients': [],
                    'nutritional_value': {},
                    'footer': ''
                }
            }
            
            # Add images (simplify paths)
            for i, img_url in enumerate(scraped.get('images', [])[:2]):  # Take max 2 images
                filename = f"{catalog_product['short']}{'-hover' if i==1 else ''}.webp"
                catalog_product['image'].append(f"assets/products/category/{filename}")
            
            # Add prices
            for price_data in scraped.get('price', []):
                catalog_product['price'].append({
                    'weight': price_data.get('weight', '100gm'),
                    'original': float(price_data.get('original', 0)),
                    'discounted': float(price_data.get('discounted', price_data.get('original', 0)))
                })
            
            # If no price found, add a default
            if not catalog_product['price']:
                catalog_product['price'].append({
                    'weight': '100gm',
                    'original': 199.00,
                    'discounted': 169.00
                })
            
            catalog_products.append(catalog_product)
            next_id += 1
        
        return catalog_products
    
    def scrape_all_products(self):
        """Scrape all products from the website"""
        print("Starting Surili.shop product scraping...")
        print("=" * 60)
        
        # Get all product links
        product_links = self.get_all_product_links()
        
        if not product_links:
            print("No product links found. Trying alternative approach...")
            # Try to scrape from collections
            collections = self._get_collections()
            if collections:
                product_links = []
                for collection in collections:
                    time.sleep(1)  # Be polite
                    collection_links = self._get_products_from_collection(collection)
                    product_links.extend(collection_links)
        
        # Scrape each product
        scraped_products = []
        for i, link in enumerate(product_links[:10], 1):  # Limit to 10 for demo
            print(f"\nProcessing product {i}/{len(product_links[:10])}")
            product_data = self.scrape_product_details(link)
            if product_data:
                scraped_products.append(product_data)
            time.sleep(1)  # Be polite to the server
        
        print(f"\nScraped {len(scraped_products)} products")
        
        # Convert to catalog format
        catalog_products = self.convert_to_catalog_format(scraped_products)
        
        # Save to file
        output_file = 'scraped_products.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(catalog_products, f, indent=4, ensure_ascii=False)
        
        print(f"\nSaved {len(catalog_products)} products to {output_file}")
        
        # Also append to existing product.json
        try:
            with open('../frontend/public/Jsonfile/product.json', 'r', encoding='utf-8') as f:
                existing = json.load(f)
        except:
            existing = []
        
        existing.extend(catalog_products)
        
        with open('../frontend/public/Jsonfile/product.json', 'w', encoding='utf-8') as f:
            json.dump(existing, f, indent=4, ensure_ascii=False)
        
        print(f"Added {len(catalog_products)} products to product.json")
        print("\nYou can now import these products using:")
        print("python manage.py import_catalog_data")
        
        return catalog_products
    
    def _get_collections(self):
        """Get collection links from the website"""
        try:
            response = self.session.get(self.base_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            collections = []
            collection_selectors = [
                'a[href*="/collections/"]',
                'nav a[href*="/collections/"]',
                'ul.menu a[href*="/collections/"]',
            ]
            
            for selector in collection_selectors:
                elements = soup.select(selector)
                for element in elements:
                    href = element.get('href', '')
                    if href and '/collections/' in href and not href.endswith('/all-products'):
                        full_url = urljoin(self.base_url, href)
                        if full_url not in collections:
                            collections.append(full_url)
            
            return collections
        except:
            return []
    
    def _get_products_from_collection(self, collection_url):
        """Get product links from a collection page"""
        try:
            response = self.session.get(collection_url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            product_links = []
            selectors = [
                'a[href*="/products/"]',
                'a.product-card',
                '.product-item a',
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                for element in elements:
                    href = element.get('href', '')
                    if href and '/products/' in href:
                        full_url = urljoin(self.base_url, href)
                        if full_url not in product_links:
                            product_links.append(full_url)
            
            return product_links
        except:
            return []

def main():
    """Main function to run the scraper"""
    print("Surili.shop Product Scraper")
    print("=" * 60)
    print("This script will attempt to scrape products from Surili.shop")
    print()
    
    scraper = SuriliScraper()
    
    print("Choose an option:")
    print("1. Scrape all products and add to database")
    print("2. Test scraping (get product links only)")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        print("\nStarting full scrape...")
        scraper.scrape_all_products()
    elif choice == "2":
        print("\nTesting product link extraction...")
        links = scraper.get_all_product_links()
        if links:
            print(f"\nFound {len(links)} product links:")
            for link in links[:5]:  # Show first 5
                print(f"  • {link}")
            if len(links) > 5:
                print(f"  ... and {len(links) - 5} more")
        else:
            print("No product links found.")
    elif choice == "3":
        print("Exiting...")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()