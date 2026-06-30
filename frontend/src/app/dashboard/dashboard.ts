import { Component, OnInit } from '@angular/core';
import { Auth } from '../../services/auth';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { Header } from "../header/header";
import { Footer } from "../footer/footer";
import { AddressService, Address } from '../../services/address-service';
import { Wishlistservice } from '../../services/wishlistservice';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, Header, Footer],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css'
})
export class Dashboard implements OnInit {

  isLoggingOut = false;
  logoutError = '';
  user: any = null;
  addresses: Address[] = [];
  defaultAddress: Address | null = null;
  wishlistItemsCount = 0;

  constructor(
    public auth: Auth,
    private router: Router,
    private addressService: AddressService,
    private wishlistService: Wishlistservice
  ){}

  ngOnInit() {
    // Double-check authentication on component init
    if (!this.auth.isLoggedIn()) {
      this.router.navigate(['/account/login'], { 
        queryParams: { returnUrl: '/account' }
      });
      return;
    }

    // Subscribe to auth user
    this.auth.currentUser$.subscribe(user => {
      this.user = user;
    });

    // Load addresses to find default
    this.loadAddresses();

    // Get wishlist count
    this.wishlistItemsCount = this.wishlistService.wishlistCount();
  }

  loadAddresses() {
    this.addressService.getAddresses().subscribe({
      next: (data) => {
        this.addresses = data;
        this.defaultAddress = data.find(addr => addr.is_default) || (data.length > 0 ? data[0] : null);
      },
      error: (err) => console.error('Error loading addresses for dashboard:', err)
    });
  }

  logout() {
    this.isLoggingOut = true;
    this.logoutError = '';
    this.auth.logout().subscribe({
      next: () => {
        this.isLoggingOut = false;
        this.router.navigate(['/account/login'], { replaceUrl: true });
      },
      error: () => {
        this.isLoggingOut = false;
        this.logoutError = 'Logout failed. Please try again.';
      }
    });
  }

}
