import { Injectable, signal, computed } from '@angular/core';

export interface CartItem {
  productId: number | string;
  variant: string;
  quantity: number;
}

@Injectable({
  providedIn: 'root'
})
export class Cartservice {

  private storageKey = 'cart';
  public cart = signal<CartItem[]>([]);
  cartCount = computed(() => this.cart().reduce((sum, item) => sum + item.quantity, 0));
  public isCartOpen = signal(false);

  constructor() {
    if (this.isBrowser()) {
      const saved = localStorage.getItem(this.storageKey);
      if (saved) {
        this.cart.set(JSON.parse(saved));
      }
    }
  }

  addToCart(productId: number | string, variant: string, quantity: number) {
    this.cart.update(cart => {
      const existing = cart.find(item => item.productId === productId && item.variant === variant);
      if (existing) {
        existing.quantity += quantity;
      } else {
        cart.push({ productId, variant, quantity });
      }
      this.saveToLocal(cart);
      return [...cart];
    });
    this.isCartOpen.set(true);
  }

  removeFromCart(productId: number | string, variant: string) {
    this.cart.update(cart => {
      const updated = cart.filter(item => !(item.productId === productId && item.variant === variant));
      this.saveToLocal(updated);
      return updated;
    });
  }

  clearCart() {
    this.cart.set([]);
    if (this.isBrowser()) localStorage.removeItem(this.storageKey);
  }

  private saveToLocal(cart: CartItem[]) {
    if (this.isBrowser()) {
      localStorage.setItem(this.storageKey, JSON.stringify(cart));
    }
  }

  private isBrowser() {
    return typeof window !== 'undefined' && typeof localStorage !== 'undefined';
  }

  openCart() {
    this.isCartOpen.set(true);
  }

  closeCart() {
    this.isCartOpen.set(false);
  }

  toggleCart() {
    this.isCartOpen.update(state => !state);
  }
}
