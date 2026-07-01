import { Component, OnInit } from '@angular/core';
import { Header } from '../header/header';
import { Footer } from '../footer/footer';
import { WhyChooseUs } from '../why-choose-us/why-choose-us';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { Cartservice } from '../../services/cartservice';
import { CatalogService } from '../../services/catalog.service';
import { Wishlistservice } from '../../services/wishlistservice';
import { Product, ProductVariant } from '../../models/catalog.models';

type ProductTab = 'description' | 'shipping' | 'reviews';

@Component({
  selector: 'app-product-page',
  standalone: true,
  imports: [Header, Footer, WhyChooseUs, CommonModule, FormsModule],
  templateUrl: './product-page.html',
  styleUrl: './product-page.css'
})
export class ProductPage implements OnInit {

  productsId: string | null = null;
  selectedProduct: Product | null = null;
  selectedWeight: ProductVariant | null = null;
  quantity = 1;
  imageList: string[] = [];
  selectedImage = '';
  currentIndex = 0;
  hovering = false;
  activeTab: ProductTab = 'description';
  showAskQuestion = false;
  shareCopied = false;

  askForm = {
    name: '',
    email: '',
    message: ''
  };

  constructor(
    private route: ActivatedRoute,
    private cartService: Cartservice,
    private catalogService: CatalogService,
    public wishlistService: Wishlistservice
  ) { }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.productsId = params.get('short');

      if (this.productsId) {
        this.catalogService.getProduct(this.productsId).subscribe({
          next: (product) => {
            this.selectedProduct = product;
            this.imageList = product.images.filter(img => img !== undefined).map(img => img.image_path);
            this.selectedImage = this.imageList[0] ?? '';
            // Default to first in-stock variant, fallback to first variant
            this.selectedWeight = product.variants.find(v => v.in_stock) ?? product.variants[0] ?? null;
            this.currentIndex = 0;
            this.quantity = 1;
            this.activeTab = 'description';
          },
          error: (err) => console.error('Error loading product:', err)
        });
      }
    });
  }

  get hasDiscount(): boolean {
    if (!this.selectedWeight) return false;
    const original = parseFloat(this.selectedWeight.original_price);
    const discounted = parseFloat(this.selectedWeight.discounted_price);
    return original > discounted;
  }

  get savePercent(): number {
    if (!this.selectedWeight || !this.hasDiscount) return 0;
    const original = parseFloat(this.selectedWeight.original_price);
    const discounted = parseFloat(this.selectedWeight.discounted_price);
    return Math.round(((original - discounted) / original) * 100);
  }

  get isInWishlist(): boolean {
    return this.selectedProduct
      ? this.wishlistService.isInWishlist(this.selectedProduct.id)
      : false;
  }

  get nutritionalEntries(): { key: string; value: string }[] {
    if (!this.selectedProduct?.nutritional_value) return [];
    return Object.entries(this.selectedProduct.nutritional_value).map(([key, value]) => ({
      key,
      value
    }));
  }

  increaseQty(): void {
    this.quantity++;
  }

  decreaseQty(): void {
    if (this.quantity > 1) {
      this.quantity--;
    }
  }

  selectWeight(variant: ProductVariant): void {
    this.selectedWeight = variant;
  }

  addToCart(): void {
    if (!this.selectedWeight || !this.selectedProduct) return;
    if (!this.selectedWeight.in_stock) return; // guard — should never reach here via UI
    this.cartService.addToCart(
      this.selectedProduct.id,
      this.selectedWeight.weight,
      this.quantity
    );
    alert('Product added to cart!');
  }

  toggleWishlist(): void {
    if (!this.selectedProduct) return;
    this.wishlistService.toggleWishlist(this.selectedProduct.id);
  }

  selectImage(index: number): void {
    this.currentIndex = index;
    this.selectedImage = this.imageList[this.currentIndex];
  }

  nextImage(): void {
    if (!this.imageList.length) return;
    this.currentIndex = (this.currentIndex + 1) % this.imageList.length;
    this.selectedImage = this.imageList[this.currentIndex];
  }

  prevImage(): void {
    if (!this.imageList.length) return;
    this.currentIndex = (this.currentIndex - 1 + this.imageList.length) % this.imageList.length;
    this.selectedImage = this.imageList[this.currentIndex];
  }

  setActiveTab(tab: ProductTab): void {
    this.activeTab = tab;
  }

  toggleAskQuestion(): void {
    this.showAskQuestion = !this.showAskQuestion;
  }

  submitQuestion(): void {
    if (!this.askForm.name || !this.askForm.email || !this.askForm.message) {
      alert('Please fill in all required fields.');
      return;
    }
    alert('Thank you! We will get back to you shortly.');
    this.askForm = { name: '', email: '', message: '' };
    this.showAskQuestion = false;
  }

  shareProduct(): void {
    const url = window.location.href;
    navigator.clipboard.writeText(url).then(() => {
      this.shareCopied = true;
      setTimeout(() => (this.shareCopied = false), 2000);
    });
  }

}
