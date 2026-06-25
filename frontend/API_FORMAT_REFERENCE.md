# API Format Quick Reference

Quick guide to the new API data format used throughout the application.

## Product List Format

Used in: Product listings, carousels, category pages, search results

```typescript
interface ProductList {
  id: number;
  name: string;
  short: string;  // URL slug
  categories: string[];  // Array of category routes
  images: ProductImage[];
  variants: ProductVariant[];
}

interface ProductImage {
  id: number;
  image_path: string;
  display_order: number;
}

interface ProductVariant {
  id: number;
  weight: string;
  original_price: string;  // e.g., "189.00"
  discounted_price: string;  // e.g., "162.00"
}
```

### Example Usage in Templates:
```html
<!-- Display first image -->
<img [src]="product.images[0]?.image_path" />

<!-- Display second image (hover) -->
<img [src]="product.images[1]?.image_path" />

<!-- Display price -->
<span>₹{{product.variants[0]?.discounted_price}}</span>
<span>₹{{product.variants[0]?.original_price}}</span>

<!-- Loop through variants -->
<div *ngFor="let variant of product.variants">
  {{variant.weight}} - ₹{{variant.discounted_price}}
</div>
```

## Product Detail Format

Used in: Product detail page

```typescript
interface Product {
  id: number;
  name: string;
  short: string;
  categories: Category[];  // Full category objects
  about?: string;
  footer?: string;
  benefits?: string[];
  ingredients?: string[];
  nutritional_value?: { [key: string]: string };
  images: ProductImage[];
  variants: ProductVariant[];
}
```

### Example Usage in Templates:
```html
<!-- Product info -->
<h1>{{product.name}}</h1>
<p>{{product.about}}</p>

<!-- Benefits list -->
<ul>
  <li *ngFor="let benefit of product.benefits">{{benefit}}</li>
</ul>

<!-- Ingredients -->
<ul>
  <li *ngFor="let ingredient of product.ingredients">{{ingredient}}</li>
</ul>

<!-- Nutritional values -->
<dl>
  <ng-container *ngFor="let item of product.nutritional_value | keyvalue">
    <dt>{{item.key}}</dt>
    <dd>{{item.value}}</dd>
  </ng-container>
</dl>

<!-- Image gallery -->
<div *ngFor="let img of product.images">
  <img [src]="img.image_path" />
</div>
```

## Category Format

Used in: Category listings, navigation

```typescript
interface Category {
  id: number;
  route: string;  // URL slug
  name: string;
  text: string;
  icon: string;
  image: string;
  content: string;
}
```

### Example Usage in Templates:
```html
<!-- Category card -->
<div class="category">
  <img [src]="category.image" />
  <h3>{{category.name}}</h3>
  <p>{{category.text}}</p>
  <a [routerLink]="['/collections', category.route]">View Products</a>
</div>

<!-- Category header -->
<h1>{{category.name.toUpperCase()}}</h1>
<p>{{category.content}}</p>
```

## Migration from Old Format

### Images
```typescript
// OLD
product.image[0]

// NEW
product.images[0].image_path
```

### Prices
```typescript
// OLD
product.price[0].discounted
product.price[0].original

// NEW
product.variants[0].discounted_price
product.variants[0].original_price
```

### Product Description
```typescript
// OLD
product.discription.about
product.discription.benefits

// NEW
product.about
product.benefits
```

## Converting Prices to Numbers

Prices are returned as strings from the API. Convert when doing calculations:

```typescript
// In TypeScript
const price = parseFloat(variant.discounted_price);
const subtotal = price * quantity;

// In Templates (formatting)
{{variant.discounted_price | number:'1.2-2'}}
```

## API Service Usage

### Get all products
```typescript
this.catalogService.getProducts().subscribe({
  next: (products: ProductList[]) => {
    this.products = products;
  },
  error: (err) => console.error(err)
});
```

### Get filtered products
```typescript
this.catalogService.getProducts({ category: 'sugar-free' }).subscribe({
  next: (products: ProductList[]) => {
    this.filteredProducts = products;
  }
});
```

### Get single product
```typescript
this.catalogService.getProduct('digestive-mukhwas').subscribe({
  next: (product: Product) => {
    this.selectedProduct = product;
  }
});
```

### Get categories
```typescript
this.catalogService.getCategories().subscribe({
  next: (categories: Category[]) => {
    this.categories = categories;
  }
});
```

## Common Patterns

### Display product card
```html
<div class="product-card" (click)="navigate(product.short)">
  <img [src]="product.images[0]?.image_path" />
  <h4>{{product.name}}</h4>
  <div class="price">
    <span class="discount">₹{{product.variants[0]?.discounted_price}}</span>
    <del>₹{{product.variants[0]?.original_price}}</del>
  </div>
</div>
```

### Display product variants
```html
<div class="variants">
  <button *ngFor="let variant of product.variants"
          [class.selected]="selectedVariant?.id === variant.id"
          (click)="selectVariant(variant)">
    {{variant.weight}} - ₹{{variant.discounted_price}}
  </button>
</div>
```

### Handle cart items
```typescript
loadCart() {
  const cart = this.cartService.cart();
  
  this.catalogService.getProducts().subscribe({
    next: (products) => {
      this.cartItems = cart.map(item => {
        const product = products.find(p => p.id === item.productId);
        const variant = product.variants.find(v => v.weight === item.variant);
        
        return {
          name: product.name,
          image: product.images[0]?.image_path,
          price: parseFloat(variant.discounted_price),
          quantity: item.quantity,
          subtotal: parseFloat(variant.discounted_price) * item.quantity
        };
      });
    }
  });
}
```

## Safe Navigation

Always use safe navigation operator (`?.`) for nested properties:

```html
<!-- Good -->
<img [src]="product.images[0]?.image_path" />
<span>{{product.variants[0]?.discounted_price}}</span>

<!-- Bad (will error if undefined) -->
<img [src]="product.images[0].image_path" />
<span>{{product.variants[0].discounted_price}}</span>
```

## TypeScript Type Imports

Import types from models:

```typescript
import { Product, ProductList, Category } from '../../models/catalog.models';

// Use in component
products: ProductList[] = [];
selectedProduct: Product | null = null;
categories: Category[] = [];
```

## Error Handling

Always handle errors in API calls:

```typescript
this.catalogService.getProducts().subscribe({
  next: (products) => {
    this.products = products;
  },
  error: (err) => {
    console.error('Error loading products:', err);
    // Show user-friendly message
    this.errorMessage = 'Failed to load products. Please try again.';
  }
});
```

---

**Quick Tip:** Use your IDE's autocomplete with the TypeScript interfaces to see all available properties!
