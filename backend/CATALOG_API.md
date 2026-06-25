# Catalog API Documentation

The catalog app provides REST API endpoints for managing categories and products.

## Database Models

### Category
- `route` (SlugField): URL-friendly identifier (e.g., 'sugar-free')
- `name` (CharField): Display name
- `text` (CharField): Short text description
- `icon` (CharField): Path to icon asset
- `image` (CharField): Path to category image
- `content` (TextField): Full description

### Product
- `name` (CharField): Product name
- `short` (SlugField): URL-friendly identifier (e.g., 'digestive-mukhwas')
- `categories` (ManyToMany): Related categories
- `about` (TextField): Product description
- `footer` (TextField): Additional information/disclaimer
- `benefits` (JSONField): Array of benefit strings
- `ingredients` (JSONField): Array of ingredient strings
- `nutritional_value` (JSONField): Object with nutritional information

### ProductImage
- `product` (ForeignKey): Related product
- `image_path` (CharField): Path to image asset
- `display_order` (PositiveInteger): Order for displaying images

### ProductVariant
- `product` (ForeignKey): Related product
- `weight` (CharField): Weight/size (e.g., '75gm', '150gm')
- `original_price` (Decimal): Original price
- `discounted_price` (Decimal): Discounted price

## API Endpoints

Base URL: `http://localhost:8000/api/catalog/`

### Categories

#### List all categories
```
GET /api/catalog/categories/
```
Returns all categories with basic information.

#### Get category details
```
GET /api/catalog/categories/{route}/
```
Get a single category by its route (slug).

Example: `GET /api/catalog/categories/sugar-free/`

#### Get category with products
```
GET /api/catalog/categories/{route}/products/
```
Get a category with all its products.

Example: `GET /api/catalog/categories/sugar-free/products/`

### Products

#### List all products
```
GET /api/catalog/products/
```
Returns all products with images and variants.

**Query Parameters:**
- `search`: Search in product name, about, and ingredients
- `categories__route`: Filter by category route
- `ordering`: Order by fields (e.g., `name`, `-name`, `id`)

Examples:
- `GET /api/catalog/products/?categories__route=sugar-free`
- `GET /api/catalog/products/?search=digestive`
- `GET /api/catalog/products/?ordering=-id`

#### Get product details
```
GET /api/catalog/products/{short}/
```
Get detailed information about a single product including all categories, images, variants, benefits, ingredients, and nutritional value.

Example: `GET /api/catalog/products/digestive-mukhwas/`

## Data Import

To import data from JSON files:

```bash
python manage.py import_catalog_data --categories "../frontend/src/Jsonfile/categories.json" --products "../frontend/src/Jsonfile/product.json"
```

This command will:
1. Import all categories from the categories JSON file
2. Import all products with their images and variants
3. Create relationships between products and categories

## Admin Interface

All models are registered in the Django admin interface at:
```
http://localhost:8000/admin/
```

Admin features:
- Category management with prepopulated slug field
- Product management with inline image and variant editors
- Search and filtering capabilities
- Horizontal filter for categories (many-to-many)

## Response Format Examples

### Category List Response
```json
[
  {
    "id": 1,
    "route": "sugar-free",
    "name": "Sugar Free",
    "text": "Sugar Free",
    "icon": "assets/icon3.png",
    "image": "assets/products/sugar-free/digestive-mukhwas.webp",
    "content": "Our Sugar-Free Healthy Mukhwas is a refreshing blend..."
  }
]
```

### Product List Response
```json
[
  {
    "id": 1,
    "name": "Digestive Mukhwas",
    "short": "digestive-mukhwas",
    "categories": ["Sugar Free"],
    "images": [
      {
        "id": 1,
        "image_path": "assets/products/sugar-free/digestive-mukhwas.webp",
        "display_order": 0
      }
    ],
    "variants": [
      {
        "id": 1,
        "weight": "75gm",
        "original_price": "189.00",
        "discounted_price": "162.00"
      }
    ]
  }
]
```

### Product Detail Response
```json
{
  "id": 1,
  "name": "Digestive Mukhwas",
  "short": "digestive-mukhwas",
  "categories": [
    {
      "id": 3,
      "route": "sugar-free",
      "name": "Sugar Free",
      "text": "Sugar Free",
      "icon": "assets/icon3.png",
      "image": "assets/products/sugar-free/digestive-mukhwas.webp",
      "content": "Our Sugar-Free Healthy Mukhwas..."
    }
  ],
  "about": "Digestive Mukhwas is a type of mouth freshener...",
  "footer": "Disclaimer For 9kg, 18kg, 27kg...",
  "benefits": [
    "Aids digestion by stimulating digestive enzymes...",
    "Freshens breath and masks odors..."
  ],
  "ingredients": [
    "Fennel Seeds",
    "Coriander Seeds",
    "Sesame Seeds"
  ],
  "nutritional_value": {
    "Fats": "7.62 g",
    "Energy": "334 Kcal",
    "Proteins": "9.24 g"
  },
  "images": [...],
  "variants": [...]
}
```

## Next Steps

1. Update your frontend Angular application to consume these API endpoints
2. Remove the local JSON files once confirmed the API works correctly
3. Consider adding:
   - Pagination for large product lists
   - Product search with more advanced filters
   - Image upload functionality
   - Shopping cart integration
   - Product reviews and ratings
