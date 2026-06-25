import { Injectable, signal, computed, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environment';

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
  private http = inject(HttpClient);

  constructor() {
    if (this.isBrowser()) {
      const saved = localStorage.getItem(this.storageKey);
      if (saved) {
        this.cart.set(JSON.parse(saved));
      }
    }
  }

  isLoggedIn() {
    return this.isBrowser() && !!localStorage.getItem('auth_user');
  }

  syncCart() {
    const localItems = this.cart();
    this.http.post<CartItem[]>(`${environment.apiUrl}/accounts/cart/sync/`, { items: localItems }, { withCredentials: true })
      .subscribe(mergedCart => {
        this.cart.set(mergedCart);
        this.saveToLocal(mergedCart);
      });
  }

  // Called on page refresh/session restore — DB is source of truth, don't re-merge local
  loadFromDB() {
    this.http.get<CartItem[]>(`${environment.apiUrl}/accounts/cart/sync/`, { withCredentials: true })
      .subscribe(dbCart => {
        this.cart.set(dbCart);
        this.saveToLocal(dbCart);
      });
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
    
    if (this.isLoggedIn()) {
      this.http.post(`${environment.apiUrl}/accounts/cart/add/`, { productId, variant, quantity }, { withCredentials: true }).subscribe();
    }
    
    this.isCartOpen.set(true);
  }

  removeFromCart(productId: number | string, variant: string) {
    this.cart.update(cart => {
      const updated = cart.filter(item => !(item.productId === productId && item.variant === variant));
      this.saveToLocal(updated);
      return updated;
    });

    if (this.isLoggedIn()) {
      this.http.post(`${environment.apiUrl}/accounts/cart/remove/`, { productId, variant }, { withCredentials: true }).subscribe();
    }
  }

  clearCart(localOnly = false) {
    this.cart.set([]);
    if (this.isBrowser()) localStorage.removeItem(this.storageKey);
    
    if (!localOnly && this.isLoggedIn()) {
      this.http.post(`${environment.apiUrl}/accounts/cart/clear/`, {}, { withCredentials: true }).subscribe();
    }
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
