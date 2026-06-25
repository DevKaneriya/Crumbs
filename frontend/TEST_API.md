# API Testing Guide

Quick reference for testing the API endpoints before running the frontend.

## Prerequisites

1. Django backend must be running:
```bash
cd backend
python manage.py runserver
```

2. You should have data in the database (already imported via `import_catalog_data` command)

## Test Endpoints Manually

### 1. Test Categories List
```bash
curl http://localhost:8000/api/catalog/categories/
```

**Expected Response:**
```json
[
  {
    "id": 1,
    "route": "all-products",
    "name": "All Products",
    "text": "Shop All",
    "icon": "assets/icon1.png",
    "image": "assets/category/tiny-miny.webp",
    "content": "Discover a wide selection..."
  },
  ...
]
```

### 2. Test Single Category
```bash
curl http://localhost:8000/api/catalog/categories/sugar-free/
```

### 3. Test Category with Products
```bash
curl http://localhost:8000/api/catalog/categories/sugar-free/products/
```

### 4. Test All Products
```bash
curl http://localhost:8000/api/catalog/products/
```

**Expected Response:**
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
  },
  ...
]
```

### 5. Test Products Filtered by Category
```bash
curl "http://localhost:8000/api/catalog/products/?categories__route=sugar-free"
```

### 6. Test Product Search
```bash
curl "http://localhost:8000/api/catalog/products/?search=mukhwas"
```

### 7. Test Single Product
```bash
curl http://localhost:8000/api/catalog/products/digestive-mukhwas/
```

**Expected Response:**
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
      ...
    }
  ],
  "about": "Digestive Mukhwas is a type of mouth freshener...",
  "footer": "Disclaimer For 9kg, 18kg, 27kg...",
  "benefits": [
    "Aids digestion by stimulating digestive enzymes...",
    ...
  ],
  "ingredients": [
    "Fennel Seeds",
    "Coriander Seeds",
    ...
  ],
  "nutritional_value": {
    "Fats": "7.62 g",
    "Energy": "334 Kcal",
    ...
  },
  "images": [...],
  "variants": [...]
}
```

## Browser Testing

Open your browser and visit:

1. **Categories**: http://localhost:8000/api/catalog/categories/
2. **Products**: http://localhost:8000/api/catalog/products/
3. **Single Product**: http://localhost:8000/api/catalog/products/digestive-mukhwas/
4. **Single Category**: http://localhost:8000/api/catalog/categories/sugar-free/

You should see JSON responses for all URLs.

## Frontend Testing Checklist

Once backend APIs are confirmed working, test the frontend:

### Homepage (/)
- [ ] Category section displays 8 categories (skipping first one)
- [ ] Product carousel displays all products
- [ ] Images load correctly
- [ ] Clicking category navigates to `/collections/{route}`
- [ ] Clicking product navigates to `/products/{short}`

### Collections Page (/collections)
- [ ] All categories display
- [ ] Category images load
- [ ] Clicking category navigates to filtered view

### Category Page (/collections/sugar-free)
- [ ] Products filtered by category display
- [ ] Product cards show correct images
- [ ] Price variants display correctly
- [ ] Wishlist toggle works
- [ ] Clicking product opens product detail page

### Product Page (/products/digestive-mukhwas)
- [ ] Product details load
- [ ] All images display in gallery
- [ ] Benefits list displays (if available)
- [ ] Ingredients list displays (if available)
- [ ] Nutritional values display (if available)
- [ ] Price variants display correctly
- [ ] Add to cart works
- [ ] Quantity controls work

### Wishlist Page (/wishlist)
- [ ] Wishlist products display
- [ ] Products load from API
- [ ] Remove from wishlist works
- [ ] Navigate to product works

### Cart
- [ ] Cart items display with correct product info
- [ ] Images load
- [ ] Prices calculate correctly
- [ ] Quantity increase/decrease works
- [ ] Remove item works
- [ ] Total calculates correctly

### Search
- [ ] Search returns products
- [ ] Search returns categories
- [ ] Clicking result navigates correctly

## Common Issues

### Issue: "Failed to fetch"
- Ensure Django server is running on port 8000
- Check `http://localhost:8000/api/catalog/products/` in browser

### Issue: Empty product lists
- Run: `python manage.py import_catalog_data --categories "../frontend/src/Jsonfile/categories.json" --products "../frontend/src/Jsonfile/product.json"`
- Verify data in Django admin: `http://localhost:8000/admin/`

### Issue: CORS errors
- Check Django `settings.py` has `'http://localhost:4200'` in `CORS_ALLOWED_ORIGINS`
- Restart Django server after changes

### Issue: Images not loading
- Image paths should be relative (e.g., `assets/products/...`)
- Ensure `assets/` folder exists in `frontend/src/`
- Check that image paths in database match file locations

## Database Quick Check

Verify data exists:

```bash
cd backend
python manage.py shell
```

```python
from catalog.models import Category, Product
print(f"Categories: {Category.objects.count()}")
print(f"Products: {Product.objects.count()}")

# Show first category
cat = Category.objects.first()
print(f"First category: {cat.name} ({cat.route})")

# Show first product
prod = Product.objects.first()
print(f"First product: {prod.name} ({prod.short})")
print(f"  Images: {prod.images.count()}")
print(f"  Variants: {prod.variants.count()}")
```

Expected output:
```
Categories: 9
Products: 8
First category: All Products (all-products)
First product: Digestive Mukhwas (digestive-mukhwas)
  Images: 5
  Variants: 5
```

## Success Criteria

✅ All API endpoints return valid JSON  
✅ Products have images and variants  
✅ Categories have proper data  
✅ Frontend loads without console errors  
✅ All pages navigate correctly  
✅ Search, wishlist, and cart work  
✅ Images display properly  

If all checks pass, migration is successful! 🎉
