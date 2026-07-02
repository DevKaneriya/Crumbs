import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

// ── Customer-facing types ──────────────────────────────────────────────────

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
  razorpay_order_id: string | null;
  created_at: string;
  items: OrderItem[];
}

// ── Razorpay types ─────────────────────────────────────────────────────────

export interface RazorpayOrderResponse {
  razorpay_order_id: string;
  amount: number;        // in paise
  currency: string;
  key_id: string;
  order_db_id: number;
}

export interface RazorpayCreateOrderPayload {
  full_name: string;
  phone: string;
  address_line: string;
  city: string;
  state: string;
  pincode: string;
  payment_method: string;
}

export interface RazorpayVerifyPayload {
  razorpay_order_id: string;
  razorpay_payment_id: string;
  razorpay_signature: string;
  order_db_id: number;
}

// ── Admin order types ──────────────────────────────────────────────────────

export interface StatusHistoryEntry {
  id: number;
  old_status: string;
  new_status: string;
  note: string;
  changed_by: string | null;
  changed_at: string;
}

export interface AdminOrder extends Order {
  customer_email: string;
  updated_at: string;
  status_history: StatusHistoryEntry[];
}

export interface TopProduct {
  product_name: string;
  units_sold: number;
  revenue: number;
}

export interface DailyTrend {
  day: string;
  count: number;
  revenue: number | null;
}

export interface OrderStats {
  total_orders: number;
  total_revenue: number;
  pending: number;
  paid: number;
  shipped: number;
  delivered: number;
  cancelled: number;
  recent_orders: number;
  recent_revenue: number;
  total_customers: number;
  customers_with_orders: number;
  top_products: TopProduct[];
  daily_trend: DailyTrend[];
}

export interface AdminOrderFilters {
  status?: string;
  payment?: string;
  search?: string;
  date_from?: string;
  date_to?: string;
}

export interface OrderUpdatePayload {
  status: string;
  note?: string;
}

// ── Admin stock types ──────────────────────────────────────────────────────

export interface StockVariant {
  id: number;
  product_name: string;
  product_short: string;
  weight: string;
  original_price: string;
  discounted_price: string;
  in_stock: boolean;
}

// ── Admin customer types ───────────────────────────────────────────────────

export interface CustomerInsight {
  user_id: number;
  email: string;
  first_name: string;
  last_name: string;
  total_orders: number;
  total_spent: number;
  last_order: string;
  delivered_orders: number;
  cancelled_orders: number;
}

// ── Admin logs types ───────────────────────────────────────────────────────

export interface OrderLog {
  id: number;
  order_id: number;
  customer_email: string;
  customer_name: string;
  total_amount: string;
  old_status: string;
  new_status: string;
  note: string;
  changed_by_email: string | null;
  changed_at: string;
}

export interface AdminLogsFilters {
  status_from?: string;
  status_to?: string;
  search?: string;
  date_from?: string;
  date_to?: string;
}

@Injectable({ providedIn: 'root' })
export class OrderService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/orders`;
  private catalogBase = `${environment.apiUrl}/catalog`;

  // ── Customer ──────────────────────────────────────────────────────────────

  getMyOrders(): Observable<Order[]> {
    return this.http.get<Order[]>(`${this.base}/my-orders/`, { withCredentials: true });
  }

  getMyOrderDetail(id: number): Observable<Order> {
    return this.http.get<Order>(`${this.base}/my-orders/${id}/`, { withCredentials: true });
  }

  /**
   * Step 1: Call backend to create a Razorpay order.
   * Returns the razorpay_order_id, amount (paise), currency, key_id, and
   * the Django order's DB id so we can reference it during verification.
   */
  createRazorpayOrder(payload: RazorpayCreateOrderPayload): Observable<RazorpayOrderResponse> {
    return this.http.post<RazorpayOrderResponse>(
      `${this.base}/razorpay/create-order/`,
      payload,
      { withCredentials: true }
    );
  }

  /**
   * Step 2: After Razorpay modal succeeds, send the three Razorpay identifiers
   * to the backend for HMAC-SHA256 signature verification.
   * On success the backend marks the order Paid and clears the cart.
   */
  verifyRazorpayPayment(payload: RazorpayVerifyPayload): Observable<Order> {
    return this.http.post<Order>(
      `${this.base}/razorpay/verify-payment/`,
      payload,
      { withCredentials: true }
    );
  }

  // ── Admin orders ──────────────────────────────────────────────────────────

  adminGetOrders(filters: AdminOrderFilters = {}): Observable<AdminOrder[]> {
    let params = new HttpParams();
    if (filters.status)    params = params.set('status', filters.status);
    if (filters.payment)   params = params.set('payment', filters.payment);
    if (filters.search)    params = params.set('search', filters.search);
    if (filters.date_from) params = params.set('date_from', filters.date_from);
    if (filters.date_to)   params = params.set('date_to', filters.date_to);
    return this.http.get<AdminOrder[]>(`${this.base}/admin/`, { params, withCredentials: true });
  }

  adminGetOrderDetail(id: number): Observable<AdminOrder> {
    return this.http.get<AdminOrder>(`${this.base}/admin/${id}/`, { withCredentials: true });
  }

  adminUpdateOrder(id: number, payload: OrderUpdatePayload): Observable<AdminOrder> {
    return this.http.patch<AdminOrder>(`${this.base}/admin/${id}/update/`, payload, { withCredentials: true });
  }

  adminGetStats(): Observable<OrderStats> {
    return this.http.get<OrderStats>(`${this.base}/admin/stats/`, { withCredentials: true });
  }

  // ── Admin stock ───────────────────────────────────────────────────────────

  adminGetStock(search?: string, inStock?: boolean): Observable<StockVariant[]> {
    let params = new HttpParams();
    if (search)              params = params.set('search', search);
    if (inStock !== undefined) params = params.set('in_stock', String(inStock));
    return this.http.get<StockVariant[]>(`${this.catalogBase}/admin/stock/`, { params, withCredentials: true });
  }

  adminToggleStock(id: number, inStock: boolean): Observable<StockVariant> {
    return this.http.patch<StockVariant>(
      `${this.catalogBase}/admin/stock/${id}/`,
      { in_stock: inStock },
      { withCredentials: true }
    );
  }

  // ── Admin customers ───────────────────────────────────────────────────────

  adminGetCustomers(search?: string, ordering?: string): Observable<CustomerInsight[]> {
    let params = new HttpParams();
    if (search)   params = params.set('search', search);
    if (ordering) params = params.set('ordering', ordering);
    return this.http.get<CustomerInsight[]>(`${this.base}/admin/customers/`, { params, withCredentials: true });
  }

  // ── Admin logs ────────────────────────────────────────────────────────────

  adminGetLogs(filters: AdminLogsFilters = {}): Observable<OrderLog[]> {
    let params = new HttpParams();
    if (filters.status_from) params = params.set('status_from', filters.status_from);
    if (filters.status_to)   params = params.set('status_to', filters.status_to);
    if (filters.search)      params = params.set('search', filters.search);
    if (filters.date_from)   params = params.set('date_from', filters.date_from);
    if (filters.date_to)     params = params.set('date_to', filters.date_to);
    return this.http.get<OrderLog[]>(`${this.base}/admin/logs/`, { params, withCredentials: true });
  }
}
