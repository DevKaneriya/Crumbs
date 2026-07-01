import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  OrderService,
  AdminOrder,
  OrderStats,
  AdminOrderFilters,
  StatusHistoryEntry,
  StockVariant,
  CustomerInsight,
  OrderLog,
  AdminLogsFilters,
} from '../../services/order.service';
import { Auth } from '../../services/auth';

export type AdminTab = 'dashboard' | 'orders' | 'stock' | 'customers' | 'logs';

@Component({
  selector: 'app-admin-orders',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-orders.html',
  styleUrl: './admin-orders.css',
})
export class AdminOrders implements OnInit {

  activeTab: AdminTab = 'dashboard';

  // ── Dashboard / Stats ─────────────────────────────────────────────────────
  stats: OrderStats | null = null;
  statsLoading = true;

  // ── Orders tab ────────────────────────────────────────────────────────────
  orders: AdminOrder[] = [];
  ordersLoading = true;
  selectedOrder: AdminOrder | null = null;
  detailLoading = false;
  updateLoading = false;
  updateSuccess = false;
  ordersErrorMsg = '';
  newStatus = '';
  updateNote = '';
  variantTogglingIds: Set<number> = new Set();

  filters: AdminOrderFilters = {};
  searchInput = '';
  selectedStatusFilter = '';
  selectedPaymentFilter = '';
  dateFrom = '';
  dateTo = '';

  // ── Stock tab ─────────────────────────────────────────────────────────────
  stockItems: StockVariant[] = [];
  stockLoading = false;
  stockSearchInput = '';
  stockFilter: '' | 'true' | 'false' = '';
  stockTogglingId: number | null = null;
  stockError = '';

  // ── Customers tab ─────────────────────────────────────────────────────────
  customers: CustomerInsight[] = [];
  customersLoading = false;
  customerSearch = '';
  customerOrdering = '-total_spent';
  customersError = '';
  expandedCustomerId: number | null = null;
  customerOrders: AdminOrder[] = [];
  customerOrdersLoading = false;

  // ── Logs tab ───────────────────────────────────────────────────────────────
  logs: OrderLog[] = [];
  logsLoading = false;
  logsError = '';
  logSearchInput = '';
  logStatusFromFilter = '';
  logStatusToFilter = '';
  logDateFrom = '';
  logDateTo = '';
  logFilters: AdminLogsFilters = {};

  readonly STATUS_OPTIONS = ['Pending', 'Paid', 'Shipped', 'Delivered', 'Cancelled'];
  readonly PAYMENT_OPTIONS = ['COD', 'Card', 'UPI', 'NetBanking', 'Wallet'];

  constructor(
    private orderService: OrderService,
    public auth: Auth,
  ) {}

  ngOnInit(): void {
    this.loadStats();
    this.loadOrders();
  }

  // ── Tab navigation ────────────────────────────────────────────────────────

  setTab(tab: AdminTab): void {
    this.activeTab = tab;
    this.selectedOrder = null;
    if (tab === 'stock' && this.stockItems.length === 0) this.loadStock();
    if (tab === 'customers' && this.customers.length === 0) this.loadCustomers();
    if (tab === 'logs' && this.logs.length === 0) this.loadLogs();
  }

  // ── Stats ─────────────────────────────────────────────────────────────────

  loadStats(): void {
    this.statsLoading = true;
    this.orderService.adminGetStats().subscribe({
      next: (data) => { this.stats = data; this.statsLoading = false; },
      error: () => { this.statsLoading = false; },
    });
  }

  // ── Orders ────────────────────────────────────────────────────────────────

  loadOrders(): void {
    this.ordersLoading = true;
    this.ordersErrorMsg = '';
    this.orderService.adminGetOrders(this.filters).subscribe({
      next: (data) => { this.orders = data; this.ordersLoading = false; },
      error: () => { this.ordersErrorMsg = 'Failed to load orders.'; this.ordersLoading = false; },
    });
  }

  applyFilters(): void {
    this.filters = {
      status: this.selectedStatusFilter || undefined,
      payment: this.selectedPaymentFilter || undefined,
      search: this.searchInput.trim() || undefined,
      date_from: this.dateFrom || undefined,
      date_to: this.dateTo || undefined,
    };
    this.loadOrders();
  }

  clearFilters(): void {
    this.searchInput = '';
    this.selectedStatusFilter = '';
    this.selectedPaymentFilter = '';
    this.dateFrom = '';
    this.dateTo = '';
    this.filters = {};
    this.loadOrders();
  }

  openDetail(order: AdminOrder): void {
    this.selectedOrder = null;
    this.detailLoading = true;
    this.newStatus = order.status;
    this.updateNote = '';
    this.updateSuccess = false;
    this.ordersErrorMsg = '';
    this.orderService.adminGetOrderDetail(order.id).subscribe({
      next: (data) => { this.selectedOrder = data; this.newStatus = data.status; this.detailLoading = false; },
      error: () => { this.detailLoading = false; this.ordersErrorMsg = 'Could not load order details.'; },
    });
  }

  closeDetail(): void {
    this.selectedOrder = null;
    this.updateSuccess = false;
    this.ordersErrorMsg = '';
  }

  submitUpdate(): void {
    if (!this.selectedOrder || !this.newStatus) return;
    this.updateLoading = true;
    this.updateSuccess = false;
    this.ordersErrorMsg = '';
    this.orderService.adminUpdateOrder(this.selectedOrder.id, { status: this.newStatus, note: this.updateNote })
      .subscribe({
        next: (updated) => {
          this.selectedOrder = updated;
          this.newStatus = updated.status;
          this.updateNote = '';
          this.updateLoading = false;
          this.updateSuccess = true;
          const idx = this.orders.findIndex((o) => o.id === updated.id);
          if (idx !== -1) this.orders[idx] = updated;
          // refresh stats counts
          this.loadStats();
          setTimeout(() => (this.updateSuccess = false), 3000);
        },
        error: () => { this.updateLoading = false; this.ordersErrorMsg = 'Update failed.'; },
      });
  }

  totalItems(order: AdminOrder): number {
    return order.items.reduce((s, i) => s + i.quantity, 0);
  }

  // ── Stock ─────────────────────────────────────────────────────────────────

  loadStock(): void {
    this.stockLoading = true;
    this.stockError = '';
    const inStockVal = this.stockFilter === 'true' ? true : this.stockFilter === 'false' ? false : undefined;
    this.orderService.adminGetStock(this.stockSearchInput.trim() || undefined, inStockVal).subscribe({
      next: (data) => { this.stockItems = data; this.stockLoading = false; },
      error: () => { this.stockError = 'Failed to load stock.'; this.stockLoading = false; },
    });
  }

  toggleStock(variant: StockVariant): void {
    this.stockTogglingId = variant.id;
    this.orderService.adminToggleStock(variant.id, !variant.in_stock).subscribe({
      next: (updated) => {
        this.stockItems = this.stockItems.map(v => v.id === updated.id ? updated : v);
        this.stockTogglingId = null;
      },
      error: () => { this.stockTogglingId = null; },
    });
  }

  get outOfStockCount(): number {
    return this.stockItems.filter((v) => !v.in_stock).length;
  }

  get inStockCount(): number {
    return this.stockItems.filter((v) => v.in_stock).length;
  }

  // ── Customers ─────────────────────────────────────────────────────────────

  loadCustomers(): void {
    this.customersLoading = true;
    this.customersError = '';
    this.orderService.adminGetCustomers(
      this.customerSearch.trim() || undefined,
      this.customerOrdering
    ).subscribe({
      next: (data) => { this.customers = data; this.customersLoading = false; },
      error: () => { this.customersError = 'Failed to load customers.'; this.customersLoading = false; },
    });
  }

  sortCustomers(field: string): void {
    if (this.customerOrdering === `-${field}`) {
      this.customerOrdering = field;
    } else {
      this.customerOrdering = `-${field}`;
    }
    this.loadCustomers();
  }

  sortIcon(field: string): string {
    if (this.customerOrdering === `-${field}`) return 'fa-sort-down';
    if (this.customerOrdering === field) return 'fa-sort-up';
    return 'fa-sort';
  }

  toggleCustomerOrders(customer: CustomerInsight): void {
    if (this.expandedCustomerId === customer.user_id) {
      this.expandedCustomerId = null;
      this.customerOrders = [];
      return;
    }
    this.expandedCustomerId = customer.user_id;
    this.customerOrdersLoading = true;
    this.customerOrders = [];
    // Filter orders for this customer from already-loaded orders list
    // If orders tab not loaded yet, fetch all orders
    if (this.orders.length > 0) {
      this.customerOrders = this.orders.filter(o => o.customer_email === customer.email);
      this.customerOrdersLoading = false;
    } else {
      this.orderService.adminGetOrders({ search: customer.email }).subscribe({
        next: (data) => { this.customerOrders = data; this.customerOrdersLoading = false; },
        error: () => { this.customerOrdersLoading = false; },
      });
    }
  }

  // ── Logs ───────────────────────────────────────────────────────────────────

  loadLogs(): void {
    this.logsLoading = true;
    this.logsError = '';
    this.orderService.adminGetLogs(this.logFilters).subscribe({
      next: (data) => { this.logs = data; this.logsLoading = false; },
      error: () => { this.logsError = 'Failed to load logs.'; this.logsLoading = false; },
    });
  }

  applyLogFilters(): void {
    this.logFilters = {
      status_from: this.logStatusFromFilter || undefined,
      status_to: this.logStatusToFilter || undefined,
      search: this.logSearchInput.trim() || undefined,
      date_from: this.logDateFrom || undefined,
      date_to: this.logDateTo || undefined,
    };
    this.loadLogs();
  }

  clearLogFilters(): void {
    this.logSearchInput = '';
    this.logStatusFromFilter = '';
    this.logStatusToFilter = '';
    this.logDateFrom = '';
    this.logDateTo = '';
    this.logFilters = {};
    this.loadLogs();
  }

  exportLogsCSV(): void {
    if (this.logs.length === 0) {
      alert('No logs to export');
      return;
    }

    // Create CSV content
    const headers = ['Order ID', 'Customer Name', 'Email', 'Amount', 'Status Change', 'Changed By', 'Changed At', 'Note'];
    const rows = this.logs.map(log => [
      log.order_id,
      log.customer_name,
      log.customer_email,
      '₹' + log.total_amount,
      `${log.old_status} → ${log.new_status}`,
      log.changed_by_email || 'System',
      new Date(log.changed_at).toLocaleString(),
      log.note || '',
    ]);

    const csv = [
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${cell}"`).join(',')),
    ].join('\n');

    // Download
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `order-logs-${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
    window.URL.revokeObjectURL(url);
  }

  // ── Shared helpers ────────────────────────────────────────────────────────

  statusClass(status: string): string {
    const map: Record<string, string> = {
      Pending: 'status-pending',
      Paid: 'status-paid',
      Shipped: 'status-shipped',
      Delivered: 'status-delivered',
      Cancelled: 'status-cancelled',
    };
    return map[status] ?? 'status-pending';
  }

  trackById(_: number, item: { id: number }): number {
    return item.id;
  }

  get topDailyRevenue(): number {
    if (!this.stats?.daily_trend?.length) return 0;
    return Math.max(...this.stats.daily_trend.map(d => Number(d.revenue) || 0));
  }

  // Check if any items in order are available (helper for stock status)
  hasAnyItems(order: AdminOrder): boolean {
    return order.items.length > 0;
  }

  // ── Inline stock toggle from the Orders detail panel ──────────────────────

  /**
   * Key format: "<product_name>|<variant_weight>" — available synchronously
   * from the template so the spinner shows immediately on click.
   */
  private togglingKey(productName: string, variantWeight: string): string {
    return `${productName}|${variantWeight}`;
  }

  isItemStockToggling(productName: string, variantWeight: string): boolean {
    return this._togglingKeys.has(this.togglingKey(productName, variantWeight));
  }

  // String-keyed set so we can show the spinner before we even know the variant ID
  private _togglingKeys = new Set<string>();

  /** Returns the known in_stock state for a variant from the stockItems cache, or null if unknown. */
  getItemStockState(productName: string, variantWeight: string): boolean | null {
    const v = this.stockItems.find(
      s => s.product_name === productName && s.weight === variantWeight
    );
    return v ? v.in_stock : null;
  }

  toggleItemStock(productName: string, variantWeight: string): void {
    const key = this.togglingKey(productName, variantWeight);
    if (this._togglingKeys.has(key)) return; // already in flight
    this._togglingKeys.add(key);
    this.ordersErrorMsg = '';

    // Try to find variant in the already-loaded stockItems cache first
    const cached = this.stockItems.find(
      s => s.product_name === productName && s.weight === variantWeight
    );

    if (cached) {
      this._doToggle(cached, key);
    } else {
      // Cache miss — fetch only by product name (targeted, not full list)
      this.orderService.adminGetStock(productName).subscribe({
        next: (variants) => {
          // Merge fetched variants into the cache so future calls are instant
          for (const v of variants) {
            if (!this.stockItems.find(s => s.id === v.id)) {
              this.stockItems.push(v);
            }
          }
          const found = variants.find(v => v.weight === variantWeight);
          if (found) {
            this._doToggle(found, key);
          } else {
            this._togglingKeys.delete(key);
            this.ordersErrorMsg = `Variant "${variantWeight}" not found for "${productName}".`;
          }
        },
        error: () => {
          this._togglingKeys.delete(key);
          this.ordersErrorMsg = 'Failed to load variant data.';
        },
      });
    }
  }

  private _doToggle(variant: StockVariant, key: string): void {
    this.orderService.adminToggleStock(variant.id, !variant.in_stock).subscribe({
      next: (updated) => {
        // Patch the stockItems cache in-place (no full re-fetch needed)
        const idx = this.stockItems.findIndex(s => s.id === updated.id);
        if (idx !== -1) this.stockItems[idx] = updated;
        else this.stockItems.push(updated);
        this._togglingKeys.delete(key);
        // Refresh the sidebar badge count and stats
        this.loadStats();
      },
      error: () => {
        this._togglingKeys.delete(key);
        this.ordersErrorMsg = 'Failed to update stock status.';
      },
    });
  }

  isVariantToggling(): boolean {
    return this._togglingKeys.size > 0;
  }
}
