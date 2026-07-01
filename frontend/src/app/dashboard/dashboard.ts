import { Component, OnInit } from '@angular/core';
import { Auth } from '../../services/auth';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { Header } from "../header/header";
import { Footer } from "../footer/footer";
import { AddressService, Address } from '../../services/address-service';
import { Wishlistservice } from '../../services/wishlistservice';
import { OrderService, Order } from '../../services/order.service';

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

  orders: Order[] = [];
  ordersLoading = true;
  expandedOrderId: number | null = null;

  constructor(
    public auth: Auth,
    private router: Router,
    private addressService: AddressService,
    private wishlistService: Wishlistservice,
    private orderService: OrderService
  ) {}

  ngOnInit() {
    if (!this.auth.isLoggedIn()) {
      this.router.navigate(['/account/login'], { queryParams: { returnUrl: '/account' } });
      return;
    }

    this.auth.currentUser$.subscribe(user => { this.user = user; });
    this.loadAddresses();
    this.loadOrders();
    this.wishlistItemsCount = this.wishlistService.wishlistCount();
  }

  loadAddresses() {
    this.addressService.getAddresses().subscribe({
      next: (data) => {
        this.addresses = data;
        this.defaultAddress = data.find(a => a.is_default) ?? (data[0] ?? null);
      },
      error: (err) => console.error('Error loading addresses:', err)
    });
  }

  loadOrders() {
    this.ordersLoading = true;
    this.orderService.getMyOrders().subscribe({
      next: (data) => {
        this.orders = data;
        this.ordersLoading = false;
      },
      error: (err) => {
        console.error('Error loading orders:', err);
        this.ordersLoading = false;
      }
    });
  }

  toggleOrder(orderId: number) {
    this.expandedOrderId = this.expandedOrderId === orderId ? null : orderId;
  }

  /** Returns a CSS class name based on order status */
  statusClass(status: string): string {
    const map: Record<string, string> = {
      Pending:   'status-pending',
      Paid:      'status-paid',
      Shipped:   'status-shipped',
      Delivered: 'status-delivered',
      Cancelled: 'status-cancelled',
    };
    return map[status] ?? 'status-pending';
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
