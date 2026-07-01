import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

export interface OrderItem {
  id: number;
  product_name: string;
  variant_weight: string;
  quantity: number;
  price_at_purchase: string;
  subtotal: number;
}

export interface Order {
  id: number;
  full_name: string;
  phone: string;
  address_line: string;
  city: string;
  state: string;
  pincode: string;
  total_amount: string;
  status: 'Pending' | 'Paid' | 'Shipped' | 'Delivered' | 'Cancelled';
  payment_method: string;
  payment_id: string | null;
  created_at: string;
  items: OrderItem[];
}

@Injectable({ providedIn: 'root' })
export class OrderService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/orders`;

  getMyOrders(): Observable<Order[]> {
    return this.http.get<Order[]>(`${this.base}/my-orders/`, { withCredentials: true });
  }
}
