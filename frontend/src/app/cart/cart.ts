import { Component, effect, OnInit } from '@angular/core';
import { Cartservice, CartItem } from '../../services/cartservice';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { CatalogService } from '../../services/catalog.service';
import { ProductList } from '../../models/catalog.models';

@Component({
  selector: 'app-cart',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './cart.html',
  styleUrl: './cart.css'
})
export class Cart implements OnInit {

  products: ProductList[] = [];
  cartItems: any[] = [];
  totalAmount: number = 0;

  constructor(
    public cartService: Cartservice,
    private router: Router,
    private catalogService: CatalogService
  ) {
    effect(() => {
      this.loadCart();
    });
  }

  ngOnInit() {
    // Load products from API
    this.catalogService.getProducts().subscribe({
      next: (products) => {
        this.products = products;
        this.loadCart();
      },
      error: (err) => console.error('Error loading products:', err)
    });
  }

  loadCart() {
    const cart: CartItem[] = this.cartService.cart();
    
    if (this.products.length === 0) return;

    this.cartItems = cart.map(item => {
      const product = this.products.find((p: ProductList) => p.id === item.productId);
      
      if (!product) return null;

      const variant = product.variants.find(v => v.weight === item.variant);
      
      if (!variant) return null;

      const discountedPrice = parseFloat(variant.discounted_price);
      const originalPrice = parseFloat(variant.original_price);

      return {
        productId: item.productId,
        variant: item.variant,
        quantity: item.quantity,
        name: product.name,
        route: product.short,
        image: product.images[0]?.image_path,
        price: discountedPrice,
        original: originalPrice,
        actualsubtotal: originalPrice * item.quantity,
        subtotal: discountedPrice * item.quantity
      };
    }).filter(item => item !== null);

    this.calculateTotal();
  }

  calculateTotal() {
    this.totalAmount = this.cartItems.reduce((sum, item) => sum + item.subtotal, 0);
  }

  increaseQty(item: any) {
    item.quantity++;
    this.cartService.addToCart(item.productId, item.variant, 1);
    item.subtotal = item.quantity * item.price;
    this.calculateTotal();
  }

  decreaseQty(item: any) {
    if (item.quantity > 1) {
      item.quantity--;
      this.cartService.addToCart(item.productId, item.variant, -1);
      item.subtotal = item.quantity * item.price;
      this.calculateTotal();
    }
  }

  removeItem(item: any) {
    this.cartService.removeFromCart(item.productId, item.variant);
    this.loadCart();
  }

  clearCart() {
    this.cartService.clearCart();
    this.loadCart();
  }


  navigate(path: string, slug?: string) {
    if (slug) {
      this.router.navigate([path, slug]);
    } else {
      this.router.navigate([path]);
    }
    this.cartService.closeCart();
  }

}
