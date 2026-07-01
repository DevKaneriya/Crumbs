import { Component, OnInit } from '@angular/core';
import { Header } from "../header/header";
import { Footer } from "../footer/footer";
import { ProductTemplate } from "../product-template/product-template";
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { Wishlistservice } from '../../services/wishlistservice';
import { CatalogService } from '../../services/catalog.service';
import { Cartservice } from '../../services/cartservice';
import { ProductList, ProductVariant, Category } from '../../models/catalog.models';

@Component({
  selector: 'app-collection-category',
  standalone: true,
  imports: [Header, Footer, ProductTemplate, CommonModule],
  templateUrl: './collection-category.html',
  styleUrl: './collection-category.css'
})
export class CollectionCategory implements OnInit {

  categoriesId: string | null = null;
  filteredProducts: ProductList[] = [];
  currentCategory: Category | null = null;
  isLoading = true;

  // Track which product IDs were just added (for the "✓ Added" flash)
  addedProductIds = new Set<number>();

  constructor(
    private activeRoute: ActivatedRoute,
    private router: Router,
    public wishlistService: Wishlistservice,
    private catalogService: CatalogService,
    private cartService: Cartservice,
  ) { }

  navigate(slug: string) {
    this.router.navigate(['/products', slug]).then(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  ngOnInit(): void {
    this.activeRoute.paramMap.subscribe(params => {
      this.categoriesId = params.get('route');

      if (this.categoriesId === 'all-products') {
        this.catalogService.getProducts().subscribe({
          next: (products) => { this.filteredProducts = products; this.isLoading = false; },
          error: (err) => { console.error('Error loading products:', err); this.isLoading = false; }
        });
        this.catalogService.getCategory('all-products').subscribe({
          next: (category) => { this.currentCategory = category; },
          error: (err) => console.error('Error loading category:', err)
        });
      } else if (this.categoriesId) {
        this.catalogService.getProducts({ category: this.categoriesId }).subscribe({
          next: (products) => { this.filteredProducts = products; this.isLoading = false; },
          error: (err) => { console.error('Error loading products:', err); this.isLoading = false; }
        });
        this.catalogService.getCategory(this.categoriesId).subscribe({
          next: (category) => { this.currentCategory = category; },
          error: (err) => console.error('Error loading category:', err)
        });
      } else {
        this.filteredProducts = [];
      }
    });
  }

  /** First in-stock variant, sorted by price ascending (API already sorts by price). */
  firstInStockVariant(product: ProductList): ProductVariant | null {
    return product.variants.find(v => v.in_stock) ?? null;
  }

  /** True only when ALL variants are out of stock. */
  isProductOutOfStock(product: ProductList): boolean {
    return product.variants.length > 0 && product.variants.every(v => !v.in_stock);
  }

  addToCart(product: ProductList, event: Event): void {
    event.stopPropagation(); // don't navigate to product page
    const variant = this.firstInStockVariant(product);
    if (!variant) return; // button is disabled anyway, but guard here too
    this.cartService.addToCart(product.id, variant.weight, 1);
    // Flash "Added" state for 1.5s
    this.addedProductIds.add(product.id);
    setTimeout(() => this.addedProductIds.delete(product.id), 1500);
  }

  wasJustAdded(product: ProductList): boolean {
    return this.addedProductIds.has(product.id);
  }

  toggleWishlist(product: ProductList, event: Event) {
    event.stopPropagation();
    this.wishlistService.toggleWishlist(product.id);
  }

  isInWishlist(product: ProductList) {
    return this.wishlistService.isInWishlist(product.id);
  }
}
