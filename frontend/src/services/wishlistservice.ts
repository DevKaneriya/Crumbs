import { Injectable, signal, computed, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class Wishlistservice {

  private storageKey = 'wishlist';
  public wishlist = signal<number[]>([]);
  wishlistCount = computed(() => this.wishlist().length);
  private http = inject(HttpClient);

  constructor() {
    if (this.isBrowser()) {
      const saved = localStorage.getItem(this.storageKey);
      if (saved) {
        this.wishlist.set(JSON.parse(saved));
      }
    }
  }

  syncWishlist() {
    const localItems = this.wishlist();
    this.http.post<number[]>(`${environment.apiUrl}/accounts/wishlist/sync/`, { items: localItems }, { withCredentials: true })
      .subscribe(mergedWishlist => {
        this.wishlist.set(mergedWishlist);
        if (this.isBrowser()) {
          localStorage.setItem(this.storageKey, JSON.stringify(mergedWishlist));
        }
      });
  }

  loadFromDB(dbWishlist: number[]) {
    this.wishlist.set(dbWishlist || []);
    if (this.isBrowser()) {
      localStorage.setItem(this.storageKey, JSON.stringify(dbWishlist || []));
    }
  }

  // Called on page refresh/session restore — fetches DB state without re-merging local
  loadFromDBRemote() {
    this.http.get<number[]>(`${environment.apiUrl}/accounts/wishlist/sync/`, { withCredentials: true })
      .subscribe(dbWishlist => {
        this.wishlist.set(dbWishlist);
        if (this.isBrowser()) {
          localStorage.setItem(this.storageKey, JSON.stringify(dbWishlist));
        }
      });
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

    if (this.isLoggedIn()) {
      this.http.post(`${environment.apiUrl}/accounts/wishlist/toggle/`, { productId }, { withCredentials: true }).subscribe();
    }
  }
  
  clearWishlist(localOnly = false) {
    this.wishlist.set([]);
    if (this.isBrowser()) localStorage.removeItem(this.storageKey);
    
    if (!localOnly && this.isLoggedIn()) {
      this.http.post(`${environment.apiUrl}/accounts/wishlist/clear/`, {}, { withCredentials: true }).subscribe();
    }
  }

  public isLoggedIn() {
    return this.isBrowser() && !!localStorage.getItem('auth_user');
  }

  private isBrowser() {
    return typeof window !== 'undefined' && typeof localStorage !== 'undefined';
  }
}
