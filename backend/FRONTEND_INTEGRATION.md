# Frontend Integration Guide

This guide shows how to integrate the Django catalog API with your Angular frontend.

## Angular Service Example

Create a service to handle catalog API calls:

```typescript
// catalog.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Category {
  id: number;
  route: string;
  name: string;
  text: string;
  icon: string;
  image: string;
  content: string;
}

export interface ProductImage {
  id: number;
  image_path: string;
  display_order: number;
}

export interface ProductVariant {
  id: number;
  weight: string;
  original_price: string;
  discounted_price: string;
}

export interface Product {
  id: number;
  name: string;
  short: string;
  categories: string[] | Category[];
  images: ProductImage[];
  variants: ProductVariant[];
  about?: string;
  footer?: string;
  benefits?: string[];
  ingredients?: string[];
  nutritional_value?: { [key: string]: string };
}

@Injectable({
  providedIn: 'root'
})
export class CatalogService {
  private apiUrl = 'http://localhost:8000/api/catalog';

  constructor(private http: HttpClient) { }

  // Categories
  getCategories(): Observable<Category[]> {
    return this.http.get<Category[]>(`${this.apiUrl}/categories/`);
  }

  getCategory(route: string): Observable<Category> {
    return this.http.get<Category>(`${this.apiUrl}/categories/${route}/`);
  }

  getCategoryWithProducts(route: string): Observable<Category & { products: Product[] }> {
    return this.http.get<Category & { products: Product[] }>(
      `${this.apiUrl}/categories/${route}/products/`
    );
  }

  // Products
  getProducts(filters?: {
    search?: string;
    category?: string;
    ordering?: string;
  }): Observable<Product[]> {
    let params = new HttpParams();
    
    if (filters?.search) {
      params = params.set('search', filters.search);
    }
    if (filters?.category) {
      params = params.set('categories__route', filters.category);
    }
    if (filters?.ordering) {
      params = params.set('ordering', filters.ordering);
    }

    return this.http.get<Product[]>(`${this.apiUrl}/products/`, { params });
  }

  getProduct(short: string): Observable<Product> {
    return this.http.get<Product>(`${this.apiUrl}/products/${short}/`);
  }
}
```

## Component Usage Examples

### 1. Display Categories

```typescript
// categories.component.ts
import { Component, OnInit } from '@angular/core';
import { CatalogService, Category } from './catalog.service';

@Component({
  selector: 'app-categories',
  template: `
    <div class="categories">
      <div *ngFor="let category of categories" class="category-card">
        <img [src]="category.image" [alt]="category.name">
        <h3>{{ category.name }}</h3>
        <p>{{ category.text }}</p>
        <a [routerLink]="['/category', category.route]">View Products</a>
      </div>
    </div>
  `
})
export class CategoriesComponent implements OnInit {
  categories: Category[] = [];

  constructor(private catalogService: CatalogService) {}

  ngOnInit() {
    this.catalogService.getCategories().subscribe(
      categories => this.categories = categories
    );
  }
}
```

### 2. Display Products in a Category

```typescript
// category-products.component.ts
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CatalogService, Product } from './catalog.service';

@Component({
  selector: 'app-category-products',
  template: `
    <div class="products-grid">
      <div *ngFor="let product of products" class="product-card">
        <img [src]="product.images[0]?.image_path" [alt]="product.name">
        <h4>{{ product.name }}</h4>
        <div class="variants">
          <div *ngFor="let variant of product.variants" class="variant">
            <span>{{ variant.weight }}</span>
            <span class="price">
              <del>₹{{ variant.original_price }}</del>
              ₹{{ variant.discounted_price }}
            </span>
          </div>
        </div>
        <a [routerLink]="['/product', product.short]">View Details</a>
      </div>
    </div>
  `
})
export class CategoryProductsComponent implements OnInit {
  products: Product[] = [];
  categoryRoute: string = '';

  constructor(
    private catalogService: CatalogService,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.categoryRoute = params['route'];
      this.loadProducts();
    });
  }

  loadProducts() {
    this.catalogService.getProducts({ category: this.categoryRoute }).subscribe(
      products => this.products = products
    );
  }
}
```

### 3. Display Product Details

```typescript
// product-detail.component.ts
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CatalogService, Product } from './catalog.service';

@Component({
  selector: 'app-product-detail',
  template: `
    <div *ngIf="product" class="product-detail">
      <div class="gallery">
        <img *ngFor="let img of product.images" 
             [src]="img.image_path" 
             [alt]="product.name">
      </div>
      
      <div class="info">
        <h1>{{ product.name }}</h1>
        <p>{{ product.about }}</p>
        
        <div *ngIf="product.benefits?.length" class="benefits">
          <h3>Benefits:</h3>
          <ul>
            <li *ngFor="let benefit of product.benefits">{{ benefit }}</li>
          </ul>
        </div>
        
        <div *ngIf="product.ingredients?.length" class="ingredients">
          <h3>Ingredients:</h3>
          <ul>
            <li *ngFor="let ingredient of product.ingredients">{{ ingredient }}</li>
          </ul>
        </div>
        
        <div *ngIf="product.nutritional_value" class="nutrition">
          <h3>Nutritional Value:</h3>
          <dl>
            <ng-container *ngFor="let item of product.nutritional_value | keyvalue">
              <dt>{{ item.key }}:</dt>
              <dd>{{ item.value }}</dd>
            </ng-container>
          </dl>
        </div>
        
        <div class="variants">
          <h3>Select Size:</h3>
          <div *ngFor="let variant of product.variants" class="variant-option">
            <input type="radio" [id]="'variant-' + variant.id" name="variant">
            <label [for]="'variant-' + variant.id">
              {{ variant.weight }} - 
              <del>₹{{ variant.original_price }}</del>
              <strong>₹{{ variant.discounted_price }}</strong>
            </label>
          </div>
        </div>
        
        <p *ngIf="product.footer" class="footer-note">{{ product.footer }}</p>
      </div>
    </div>
  `
})
export class ProductDetailComponent implements OnInit {
  product: Product | null = null;

  constructor(
    private catalogService: CatalogService,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    this.route.params.subscribe(params => {
      const productShort = params['short'];
      this.catalogService.getProduct(productShort).subscribe(
        product => this.product = product
      );
    });
  }
}
```

## Migration Steps

1. **Keep Both Systems Running Initially**
   - Keep the JSON files temporarily
   - Test the API endpoints thoroughly
   - Gradually switch components to use the API

2. **Update Environment Configuration**
   ```typescript
   // environment.ts
   export const environment = {
     production: false,
     apiUrl: 'http://localhost:8000/api'
   };
   
   // environment.prod.ts
   export const environment = {
     production: true,
     apiUrl: 'https://your-domain.com/api'
   };
   ```

3. **Update HttpClient Configuration**
   Make sure HttpClientModule is imported in your app.module.ts:
   ```typescript
   import { HttpClientModule } from '@angular/common/http';
   
   @NgModule({
     imports: [
       HttpClientModule,
       // ... other modules
     ]
   })
   ```

4. **Handle CORS**
   The Django backend is already configured with CORS settings in settings.py.
   Verify that your frontend URL is included in CORS_ALLOWED_ORIGINS.

5. **Test Each Endpoint**
   - Categories list: `/api/catalog/categories/`
   - Category detail: `/api/catalog/categories/sugar-free/`
   - Products list: `/api/catalog/products/`
   - Products by category: `/api/catalog/products/?categories__route=sugar-free`
   - Product detail: `/api/catalog/products/digestive-mukhwas/`

6. **Remove JSON Files**
   Once everything is working and tested:
   - Remove `frontend/src/Jsonfile/categories.json`
   - Remove `frontend/src/Jsonfile/product.json`
   - Remove any JSON file loading code

## Error Handling

Add proper error handling to your service:

```typescript
import { catchError } from 'rxjs/operators';
import { throwError } from 'rxjs';

getProducts(filters?: any): Observable<Product[]> {
  // ... params setup
  return this.http.get<Product[]>(`${this.apiUrl}/products/`, { params })
    .pipe(
      catchError(error => {
        console.error('Error fetching products:', error);
        return throwError(() => error);
      })
    );
}
```

## Notes

- All image paths are stored as strings (e.g., 'assets/products/...'). Your Angular app should already handle these paths correctly.
- Prices are returned as strings from the API to preserve decimal precision.
- The API uses route/short slugs for URLs instead of numeric IDs for better SEO.
- JSONField data (benefits, ingredients, nutritional_value) is automatically parsed to JavaScript arrays/objects.
