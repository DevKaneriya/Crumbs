import { Injectable } from '@angular/core';
import { of } from 'rxjs';
import { Wishlistservice } from './wishlistservice';
import { Cartservice } from './cartservice';

@Injectable({
  providedIn: 'root'
})
export class Auth {

  private tokenKey = 'auth_token';

  constructor(
    private wishlistService: Wishlistservice,
    private cartService: Cartservice
  ) { }

  register(data: { name: string; email: string; password: string }) {
    if (this.isBrowser()) {
      localStorage.setItem(this.tokenKey, 'mock_token_12345');
      localStorage.setItem('user_name', data.name);
      localStorage.setItem('user_email', data.email);
    }
    return of({ token: 'mock_token_12345', user: { name: data.name, email: data.email, wishlist: [] } });
  }

  login(data: { email: string; password: string }) {
    if (this.isBrowser()) {
      localStorage.setItem(this.tokenKey, 'mock_token_12345');
      localStorage.setItem('user_name', 'Mock User');
      localStorage.setItem('user_email', data.email);
    }
    return of({ token: 'mock_token_12345', user: { name: 'Mock User', email: data.email, wishlist: [] } });
  }

  logout() {
    if (this.isBrowser()) {
      localStorage.removeItem(this.tokenKey);
      localStorage.removeItem('user_name');
      localStorage.removeItem('user_email');
    }
    return of({ message: 'Logged out successfully', wishlist: [] });
  }

  user() {
    if (this.isBrowser()) {
      return of({
        name: localStorage.getItem('user_name') || 'Guest',
        email: localStorage.getItem('user_email') || ''
      });
    }
    return of({ name: 'Guest', email: '' });
  }

  getToken() {
    if (!this.isBrowser()) return null;
    return localStorage.getItem(this.tokenKey);
  }

  isLoggedIn() {
    return !!this.getToken();
  }

  isBrowser(): boolean {
    return typeof window !== 'undefined' && !!window.localStorage;
  }
}
