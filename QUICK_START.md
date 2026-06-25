# Quick Start Guide

Get your migrated frontend running with the Django API in 5 minutes!

## Step 1: Start Django Backend (Terminal 1)

```bash
cd backend
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

## Step 2: Verify API Works

Open browser and visit:
- http://localhost:8000/api/catalog/categories/
- http://localhost:8000/api/catalog/products/

You should see JSON responses with your data.

## Step 3: Start Angular Frontend (Terminal 2)

```bash
cd frontend
ng serve
```

You should see:
```
Local:   http://localhost:4200/
```

## Step 4: Test the Application

Visit: http://localhost:4200

### Quick Checks:
1. ✅ Homepage loads with categories and products
2. ✅ Click a category → products filtered correctly
3. ✅ Click a product → detail page loads
4. ✅ Search works
5. ✅ Add to cart works
6. ✅ Wishlist works

## Common Issues & Quick Fixes

### Issue: "Failed to fetch" errors
```bash
# Check if Django is running
curl http://localhost:8000/api/catalog/products/

# If not running, start it:
cd backend
python manage.py runserver
```

### Issue: Empty product lists
```bash
# Import the data
cd backend
python manage.py import_catalog_data --categories "../frontend/src/Jsonfile/categories.json" --products "../frontend/src/Jsonfile/product.json"
```

### Issue: CORS errors in browser
Edit `backend/main/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',
    'http://127.0.0.1:4200'
]
```
Then restart Django server.

### Issue: Angular compilation errors
```bash
cd frontend
npm install
ng serve
```

## Verify Data in Database

```bash
cd backend
python manage.py shell
```

```python
from catalog.models import Category, Product
print(f"Categories: {Category.objects.count()}")
print(f"Products: {Product.objects.count()}")
```

Expected: 9 categories, 8+ products

## Success! 🎉

If everything loads correctly, your migration is complete!

## What's Different?

### Before
- Products/Categories loaded from `frontend/src/Jsonfile/*.json`
- Data bundled with frontend code
- Had to rebuild frontend to update products

### After
- Products/Categories loaded from Django API
- Data in database, managed via Django admin
- Update products without touching frontend code

## Django Admin Access

Manage your products and categories:

1. Create superuser (if not done):
```bash
cd backend
python manage.py createsuperuser
```

2. Visit: http://localhost:8000/admin/

3. Navigate to:
   - **Catalog → Categories** - Manage categories
   - **Catalog → Products** - Manage products

## Next Steps

1. **Test thoroughly** - Click around, verify all features
2. **Remove JSON files** - After confirming everything works
3. **Update for production** - Set API URL in environment files
4. **Deploy** - Backend first, then frontend

## Useful Commands

### Backend
```bash
# Run server
python manage.py runserver

# Check data
python manage.py shell -c "from catalog.models import Product; print(Product.objects.count())"

# Import data
python manage.py import_catalog_data

# Create admin user
python manage.py createsuperuser
```

### Frontend
```bash
# Run dev server
ng serve

# Build for production
ng build --configuration production

# Check for errors
ng lint
```

## API Quick Reference

All endpoints: http://localhost:8000/api/catalog/

- `/categories/` - All categories
- `/categories/sugar-free/` - Single category
- `/products/` - All products
- `/products/?categories__route=sugar-free` - Filtered products
- `/products/?search=mukhwas` - Search products
- `/products/digestive-mukhwas/` - Single product

## Need Help?

1. Check `FRONTEND_MIGRATION_COMPLETE.md` for full details
2. See `TEST_API.md` for comprehensive testing guide
3. Review `frontend/MIGRATION_GUIDE.md` for migration info
4. Check browser console for errors
5. Check Django terminal for backend errors

---

**Happy coding!** 🚀
