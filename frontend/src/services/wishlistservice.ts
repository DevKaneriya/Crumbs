import { Injectable, signal, computed } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class Wishlistservice {

  private storageKey = 'wishlist';
  public wishlist = signal<number[]>([]);
  wishlistCount = computed(() => this.wishlist().length);

  constructor() {
    if (this.isBrowser()) {
      const saved = localStorage.getItem(this.storageKey);
      if (saved) {
        this.wishlist.set(JSON.parse(saved));
      }
    }
  }

  loadFromDB(dbWishlist: number[]) {
    this.wishlist.set(dbWishlist || []);
  }

  saveToLocalFromDB(dbWishlist: number[]) {
    this.wishlist.set(dbWishlist || []);
    if (this.isBrowser()) {
      localStorage.setItem(this.storageKey, JSON.stringify(dbWishlist || []));
    }
  }

  getWishlist() {
    return this.wishlist();
  }

  isInWishlist(productId: number): boolean {
    return this.wishlist().includes(productId);
  }

  addToWishlist(productId: number) {
    if (!this.isInWishlist(productId)) {
      this.wishlist.update(list => {
        const updated = [...list, productId];
        if (this.isBrowser()) {
          localStorage.setItem(this.storageKey, JSON.stringify(updated));
        }
        return updated;
      });
    }
  }

  removeFromWishlist(productId: number) {
    this.wishlist.update(list => {
      const updated = list.filter(id => id !== productId);
      if (this.isBrowser()) {
        localStorage.setItem(this.storageKey, JSON.stringify(updated));
      }
      return updated;
    });
  }

  toggleWishlist(productId: number) {
    this.isInWishlist(productId)
      ? this.removeFromWishlist(productId)
      : this.addToWishlist(productId);
  }

  public isLoggedIn() {
    return this.isBrowser() && !!localStorage.getItem('auth_token');
  }

  private isBrowser() {
    return typeof window !== 'undefined' && typeof localStorage !== 'undefined';
  }
}
