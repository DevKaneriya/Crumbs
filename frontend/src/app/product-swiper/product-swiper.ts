import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { Wishlistservice } from '../../services/wishlistservice';
import { CatalogService } from '../../services/catalog.service';
import { Cartservice } from '../../services/cartservice';
import { ProductList, ProductVariant } from '../../models/catalog.models';

declare const $: any;

@Component({
  selector: 'app-product-swiper',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './product-swiper.html',
  styleUrls: ['./product-swiper.css']
})
export class ProductSwiper implements OnInit {

  products: ProductList[] = [];
  isLoading = true;
  isDragging = false;
  mobileBreakpoint = 1025;

  // Track which product IDs were just added (for the "✓ Added" flash)
  addedProductIds = new Set<number>();

  constructor(
    private router: Router,
    public wishlistService: Wishlistservice,
    private catalogService: CatalogService,
    private cartService: Cartservice,
  ) { }

  ngOnInit() {
    this.catalogService.getProducts().subscribe({
      next: (products) => {
        this.products = products;
        this.isLoading = false;
        setTimeout(() => this.initializeCarousel(), 100);
      },
      error: (err) => { console.error('Error loading products:', err); this.isLoading = false; }
    });
  }

  navigate(slug: string) {
    if (this.isDragging) { this.isDragging = false; return; }
    this.router.navigate(['/products', slug]).then(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /** First in-stock variant (API already orders by price asc). */
  firstInStockVariant(product: ProductList): ProductVariant | null {
    return product.variants.find(v => v.in_stock) ?? null;
  }

  /** True when every variant is out of stock. */
  isProductOutOfStock(product: ProductList): boolean {
    return product.variants.length > 0 && product.variants.every(v => !v.in_stock);
  }

  addToCart(product: ProductList, event: Event): void {
    event.stopPropagation(); // prevent card click / carousel drag-navigate
    const variant = this.firstInStockVariant(product);
    if (!variant) return;
    this.cartService.addToCart(product.id, variant.weight, 1);
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

  private initializeCarousel() {
    $(".product-carousel").slick({
      dots: false,
      arrows: false,
      infinite: true,
      slidesToScroll: 1,
      slidesToShow: 3,
      accessibility: true,
      variableWidth: true,
      focusOnSelect: false,
      centerMode: false,
      autoplay: true,
      autoplaySpeed: 3000,
      responsive: [
        { breakpoint: 1200, settings: { slidesToShow: 2, slidesToScroll: 2, arrows: false } },
        { breakpoint: 767,  settings: { slidesToShow: 1, slidesToScroll: 1, arrows: false } },
        { breakpoint: 576,  settings: { slidesToShow: 1, slidesToScroll: 1, arrows: false } },
      ],
    });

    if (window.innerWidth > this.mobileBreakpoint) {
      $(".product-carousel").on("mousedown touchstart", () => this.isDragging = false);
      $(".product-carousel").on("mousemove touchmove",  () => this.isDragging = true);
    }

    $("#SliderArrowL").on("click", () => $(".product-carousel").slick("slickPrev"));
    $("#SliderArrowR").on("click", () => $(".product-carousel").slick("slickNext"));
  }

  ngAfterViewInit() { /* carousel init moved to ngOnInit after data loads */ }
}
