import { Component, effect } from '@angular/core';
import { Cartservice, CartItem } from '../../services/cartservice';
import * as productsData from '../../Jsonfile/product.json';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-cart',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './cart.html',
  styleUrl: './cart.css'
})
export class Cart {

  products: any = (productsData as any).default;
  cartItems: any[] = [];
  totalAmount: number = 0;

  constructor(
    public cartService: Cartservice,
    private router: Router,
  ) {
    effect(() => {
      this.loadCart();
    });
  }

  ngOnInit() {
    this.loadCart();
  }

  loadCart() {
    const cart: CartItem[] = this.cartService.cart();

    this.cartItems = cart.map(item => {
      const product = this.products.find((p: { id: string | number; }) => p.id === item.productId);

      const variant = product.price.find((v: any) => v.weight === item.variant);

      return {
        productId: item.productId,
        variant: item.variant,
        quantity: item.quantity,
        name: product.name,
        route: product.short,
        image: product.image[0],
        price: variant.discounted,
        original: variant.original,
        actualsubtotal: variant.original * item.quantity,
        subtotal: variant.discounted * item.quantity
      };
    });



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
