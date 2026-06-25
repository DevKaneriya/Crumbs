# Frontend Migration Guide: JSON to API

This guide documents the migration from local JSON files to Django REST API endpoints.

## What Changed

### 1. **Environment Configuration**
- Created `src/environments/environment.ts` for development
- Created `src/environments/environment.prod.ts` for production
- API URL is now configurable: `http://localhost:8000/api` (dev)

### 2. **Type Safety**
- Created `src/models/catalog.models.ts` with TypeScript interfaces:
  - `Category` - Category data structure
  - `Product` - Full product details
  - `ProductList` - Lightweight product listing
  - `LegacyProduct` - Backward compatible format
  - `ProductImage` - Product image structure
  - `ProductVariant` - Price/variant structure

### 3. **New Catalog Service**
- Created `src/services/catalog.service.ts` to handle all API calls
- Provides methods for:
  - Getting categories
  - Getting products (with filtering)
  - Getting single product/category
  - Legacy format conversion for backward compatibility

### 4. **Updated Components**

All components now use the `CatalogService` instead of importing JSON files:

#### ✅ Updated Files:
1. `src/services/searchservice.ts` - Now uses CatalogService
2. `src/app/category/category.ts` - Loads categories from API
3. `src/app/collection-page/collection-page.ts` - Loads categories from API
4. `src/app/collection-category/collection-category.ts` - Loads products by category from API
5. `src/app/product-page/product-page.ts` - Loads single product from API
6. `src/app/product-swiper/product-swiper.ts` - Loads all products from API
7. `src/app/product-template/product-template.ts` - Loads categories from API
8. `src/app/wishlist-page/wishlist-page.ts` - Loads products from API
9. `src/app/cart/cart.ts` - Loads products from API

#### 📦 Old JSON Files (can be removed after testing):
- `src/Jsonfile/categories.json`
- `src/Jsonfile/product.json`

## API Endpoints Used

### Categories
- `GET /api/catalog/categories/` - List all categories
- `GET /api/catalog/categories/{route}/` - Get single category
- `GET /api/catalog/categories/{route}/products/` - Get category with products

### Products
- `GET /api/catalog/products/` - List all products
- `GET /api/catalog/products/?categories__route={route}` - Filter by category
- `GET /api/catalog/products/?search={query}` - Search products
- `GET /api/catalog/products/{short}/` - Get single product

## Testing the Migration

### 1. Start the Backend
```bash
cd backend
python manage.py runserver
```

### 2. Start the Frontend
```bash
cd frontend
ng serve
```

### 3. Test These Features:
- [ ] Homepage displays categories
- [ ] Homepage product carousel shows products
- [ ] Collections page shows all categories
- [ ] Category pages show filtered products
- [ ] Individual product pages load correctly
- [ ] Search functionality works
- [ ] Wishlist displays products
- [ ] Cart displays products with correct prices
- [ ] All images load correctly
- [ ] All product variants/prices display

### 4. Check Browser Console
- No 404 errors for API endpoints
- No JSON import errors
- Products and categories load successfully

## Data Format Conversion

The `CatalogService` automatically converts API responses to match the old JSON format:

### API Format:
```json
{
  "id": 1,
  "images": [{"image_path": "assets/..."}],
  "variants": [{"weight": "75gm", "original_price": "189.00"}]
}
```

### Legacy Format (what components use):
```json
{
  "id": 1,
  "image": ["assets/..."],
  "price": [{"weight": "75gm", "original": 189}]
}
```

This conversion happens automatically in the service, so components didn't need major refactoring.

## Environment Variables

Update `src/environments/environment.prod.ts` before production deployment:

```typescript
export const environment = {
  production: true,
  apiUrl: 'https://your-domain.com/api'
};
```

## CORS Configuration

The backend is already configured with CORS. Verify in `backend/main/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',
    'http://127.0.0.1:4200'
]
```

Add your production frontend URL before deploying.

## Troubleshooting

### Issue: Products not loading
**Solution**: Check that Django server is running and accessible at `http://localhost:8000`

### Issue: CORS errors in browser console
**Solution**: Verify frontend URL is in `CORS_ALLOWED_ORIGINS` in Django settings

### Issue: Images not displaying
**Solution**: Image paths should work as-is since they're relative. If issues persist, check that `assets/` folder structure matches image paths in database

### Issue: Price formatting issues
**Solution**: The service converts string prices from API to numbers automatically

## Rollback Plan

If issues arise, you can temporarily rollback by:

1. Reverting the component changes
2. Re-importing the JSON files in components
3. Keep the new services for future use

However, the migration is designed to be seamless with minimal risk.

## Performance Improvements

Benefits of API-based approach:

✅ **Data always up-to-date** - No need to rebuild frontend when products change  
✅ **Admin interface** - Easy product management via Django admin  
✅ **Scalability** - Can add pagination, caching, etc.  
✅ **Search improvements** - Server-side search is more powerful  
✅ **Reduced bundle size** - JSON data no longer bundled with app  

## Next Steps

After successful testing:

1. ✅ Remove old JSON files
2. ✅ Remove JSON imports from components
3. ✅ Update production environment config
4. ✅ Deploy backend first, then frontend
5. ✅ Monitor for any issues

## Support

If you encounter issues:
1. Check browser console for errors
2. Check Django server logs
3. Verify API endpoints return data: `http://localhost:8000/api/catalog/products/`
4. Check network tab in browser dev tools
