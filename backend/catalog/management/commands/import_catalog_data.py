import json
import os
from django.core.management.base import BaseCommand
from catalog.models import Category, Product, ProductImage, ProductVariant


class Command(BaseCommand):
    help = 'Import categories and products from JSON files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--categories',
            type=str,
            default='../../frontend/src/Jsonfile/categories.json',
            help='Path to categories JSON file'
        )
        parser.add_argument(
            '--products',
            type=str,
            default='../../frontend/src/Jsonfile/product.json',
            help='Path to products JSON file'
        )

    def handle(self, *args, **options):
        # Get the base directory (backend folder)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        
        categories_path = os.path.join(base_dir, options['categories'])
        products_path = os.path.join(base_dir, options['products'])

        self.stdout.write(self.style.WARNING('Starting data import...'))

        # Import categories
        self.import_categories(categories_path)

        # Import products
        self.import_products(products_path)

        self.stdout.write(self.style.SUCCESS('Data import completed successfully!'))

    def import_categories(self, file_path):
        """Import categories from JSON file"""
        self.stdout.write(f'Importing categories from {file_path}...')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                categories_data = data.get('categories', [])

            created_count = 0
            updated_count = 0

            for index, cat_data in enumerate(categories_data):
                category, created = Category.objects.update_or_create(
                    route=cat_data['route'],
                    defaults={
                        'name': cat_data['name'],
                        'text': cat_data.get('text', ''),
                        'icon': cat_data.get('icon', ''),
                        'image': cat_data.get('image', ''),
                        'content': cat_data.get('content', ''),
                        'display_order': cat_data.get('display_order', index),
                    }
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f'Categories: {created_count} created, {updated_count} updated'
                )
            )
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'Categories file not found: {file_path}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error importing categories: {str(e)}')
            )

    def import_products(self, file_path):
        """Import products from JSON file"""
        self.stdout.write(f'Importing products from {file_path}...')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                products_data = json.load(f)

            created_count = 0
            updated_count = 0

            for prod_data in products_data:
                # Get or create product
                description = prod_data.get('discription', {})
                
                product, created = Product.objects.update_or_create(
                    short=prod_data['short'],
                    defaults={
                        'name': prod_data['name'],
                        'about': description.get('about', ''),
                        'footer': description.get('footer', ''),
                        'benefits': description.get('benefits', []),
                        'ingredients': description.get('ingredients', []),
                        'nutritional_value': description.get('nutritional_value', {}),
                    }
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

                # Clear existing related data if updating
                if not created:
                    product.images.all().delete()
                    product.variants.all().delete()
                    product.categories.clear()

                # Add categories
                for category_route in prod_data.get('categories', []):
                    try:
                        category = Category.objects.get(route=category_route)
                        product.categories.add(category)
                    except Category.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Category "{category_route}" not found for product "{product.name}"'
                            )
                        )

                # Add images
                for idx, image_path in enumerate(prod_data.get('image', [])):
                    ProductImage.objects.create(
                        product=product,
                        image_path=image_path,
                        display_order=idx
                    )

                # Add variants (prices)
                for price_data in prod_data.get('price', []):
                    ProductVariant.objects.create(
                        product=product,
                        weight=price_data['weight'],
                        original_price=price_data['original'],
                        discounted_price=price_data['discounted']
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Products: {created_count} created, {updated_count} updated'
                )
            )
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'Products file not found: {file_path}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error importing products: {str(e)}')
            )
