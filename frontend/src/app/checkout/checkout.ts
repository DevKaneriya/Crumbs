import { Component, effect, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { Cartservice, CartItem } from '../../services/cartservice';
import { Auth } from '../../services/auth';
import { CatalogService } from '../../services/catalog.service';
import { AddressService, Address } from '../../services/address-service';
import { OrderService } from '../../services/order.service';
import { ProductList } from '../../models/catalog.models';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Header } from "../header/header";
import { Footer } from "../footer/footer";

// Razorpay is loaded via CDN in index.html; declare it so TypeScript is happy
declare var Razorpay: any;

@Component({
  selector: 'app-checkout',
  standalone: true,
  imports: [CommonModule, FormsModule, Header, Footer],
  templateUrl: './checkout.html',
  styleUrl: './checkout.css'
})
export class CheckoutComponent implements OnInit {
  products: ProductList[] = [];
  cartItems: any[] = [];
  totalAmount: number = 0;

  // ─── Address state ───────────────────────────────────────────────────────
  addresses: Address[] = [];
  selectedAddress: Address | null = null;
  addressesLoading = true;

  showAddressPicker = false;
  addressFormMode: 'add' | 'edit' | null = null;
  addressForm: Address = this.emptyAddressForm();
  addressFormSaving = false;
  addressFormError = '';

  // ─── Payment state ───────────────────────────────────────────────────────
  paymentMethod = 'COD';
  paymentOptions = [
    { id: 'Card',       label: 'Credit / Debit Card', icon: 'fas fa-credit-card' },
    { id: 'UPI',        label: 'UPI / QR',            icon: 'fas fa-qrcode' },
    { id: 'Wallet',     label: 'Wallets',              icon: 'fas fa-wallet' },
    { id: 'NetBanking', label: 'Net Banking',          icon: 'fas fa-university' },
    { id: 'COD',        label: 'Cash on Delivery',     icon: 'fas fa-money-bill-wave' }
  ];

  isPlacingOrder = false;
  orderSuccess = false;
  orderId = '';

  // ─── Razorpay error state ────────────────────────────────────────────────
  paymentError = '';

  constructor(
    public cartService: Cartservice,
    private auth: Auth,
    private router: Router,
    private catalogService: CatalogService,
    private addressService: AddressService,
    private orderService: OrderService,
    private http: HttpClient
  ) {
    effect(() => { this.loadCart(); });
  }

  ngOnInit() {
    if (!this.auth.isLoggedIn()) {
      this.router.navigate(['/account/login']);
      return;
    }

    this.loadAddresses();

    this.catalogService.getProducts().subscribe({
      next: (products) => {
        this.products = products;
        this.loadCart();
      },
      error: (err) => console.error('Error loading products for checkout:', err)
    });
  }

  // ─── Address helpers ─────────────────────────────────────────────────────

  loadAddresses() {
    this.addressesLoading = true;
    this.addressService.getAddresses().subscribe({
      next: (list) => {
        this.addresses = list;
        this.selectedAddress =
          list.find(a => a.is_default) ?? (list.length > 0 ? list[0] : null);
        this.addressesLoading = false;
      },
      error: () => {
        this.addresses = [];
        this.selectedAddress = null;
        this.addressesLoading = false;
      }
    });
  }

  openAddressPicker() {
    this.addressFormMode = null;
    this.showAddressPicker = true;
  }

  closeAddressPicker() {
    this.showAddressPicker = false;
    this.addressFormMode = null;
    this.addressFormError = '';
  }

  selectAddress(addr: Address) {
    this.selectedAddress = addr;
    this.closeAddressPicker();
  }

  openAddForm() {
    this.addressForm = this.emptyAddressForm();
    this.addressFormError = '';
    this.addressFormMode = 'add';
  }

  openEditForm(addr: Address) {
    this.addressForm = { ...addr };
    this.addressFormError = '';
    this.addressFormMode = 'edit';
  }

  backToPickerList() {
    this.addressFormMode = null;
    this.addressFormError = '';
  }

  saveAddress() {
    if (!this.addressFormValid()) {
      this.addressFormError = 'Please fill in all required fields.';
      return;
    }

    this.addressFormSaving = true;
    this.addressFormError = '';

    if (this.addressFormMode === 'add') {
      this.addressService.addAddress(this.addressForm).subscribe({
        next: (saved) => {
          this.addresses.push(saved);
          this.selectedAddress = saved;
          this.addressFormSaving = false;
          this.closeAddressPicker();
        },
        error: () => {
          this.addressFormError = 'Failed to save address. Please try again.';
          this.addressFormSaving = false;
        }
      });
    } else if (this.addressFormMode === 'edit' && this.addressForm.id != null) {
      this.addressService.updateAddress(this.addressForm.id, this.addressForm).subscribe({
        next: (updated) => {
          const idx = this.addresses.findIndex(a => a.id === updated.id);
          if (idx !== -1) this.addresses[idx] = updated;
          if (this.selectedAddress?.id === updated.id) this.selectedAddress = updated;
          this.addressFormSaving = false;
          this.backToPickerList();
        },
        error: () => {
          this.addressFormError = 'Failed to update address. Please try again.';
          this.addressFormSaving = false;
        }
      });
    }
  }

  deleteAddress(addr: Address, event: MouseEvent) {
    event.stopPropagation();
    if (!addr.id || !confirm('Remove this address?')) return;
    this.addressService.deleteAddress(addr.id).subscribe({
      next: () => {
        this.addresses = this.addresses.filter(a => a.id !== addr.id);
        if (this.selectedAddress?.id === addr.id) {
          this.selectedAddress =
            this.addresses.find(a => a.is_default) ?? (this.addresses[0] ?? null);
        }
      }
    });
  }

  private addressFormValid(): boolean {
    const f = this.addressForm;
    return !!(f.first_name && f.last_name && f.address && f.city && f.state && f.pin_code && f.phone_no);
  }

  private emptyAddressForm(): Address {
    return {
      first_name: '', last_name: '', address: '', apartment: '',
      city: '', state: '', pin_code: '', phone_no: '', is_default: false
    };
  }

  // ─── Cart ────────────────────────────────────────────────────────────────

  loadCart() {
    const cart: CartItem[] = this.cartService.cart();
    if (this.products.length === 0) return;

    this.cartItems = cart.map(item => {
      const product = this.products.find((p: ProductList) => p.id === item.productId);
      if (!product) return null;
      const variant = product.variants.find(v => v.weight === item.variant);
      if (!variant) return null;
      const discountedPrice = parseFloat(variant.discounted_price);
      return {
        productId: item.productId,
        variant: item.variant,
        quantity: item.quantity,
        name: product.name,
        image: product.images[0]?.image_path,
        price: discountedPrice,
        subtotal: discountedPrice * item.quantity
      };
    }).filter(item => item !== null);

    this.totalAmount = this.cartItems.reduce((sum, item) => sum + item.subtotal, 0);

    if (this.cartItems.length === 0 && !this.orderSuccess) {
      this.router.navigate(['/']);
    }
  }

  // ─── Payment ─────────────────────────────────────────────────────────────

  setPaymentMethod(method: string) {
    this.paymentMethod = method;
    this.paymentError = '';
  }

  get isCOD(): boolean {
    return this.paymentMethod === 'COD';
  }

  // ─── Place Order (entry point) ────────────────────────────────────────────

  placeOrder() {
    if (this.cartItems.length === 0) return;

    if (!this.selectedAddress) {
      alert('Please add a shipping address before placing your order.');
      return;
    }

    this.paymentError = '';

    if (this.isCOD) {
      this.placeCodOrder();
    } else {
      this.initiateRazorpayPayment();
    }
  }

  // ─── COD flow (unchanged) ─────────────────────────────────────────────────

  private placeCodOrder() {
    this.isPlacingOrder = true;
    const addr = this.selectedAddress!;
    const payload = {
      full_name:      `${addr.first_name} ${addr.last_name}`,
      phone:          addr.phone_no,
      address_line:   addr.apartment ? `${addr.address}, ${addr.apartment}` : addr.address,
      city:           addr.city,
      state:          addr.state,
      pincode:        addr.pin_code,
      payment_method: 'COD'
    };

    // COD still uses the original single-step checkout endpoint
    this.http.post<any>(
      `${environment.apiUrl}/orders/checkout/`,
      payload,
      { withCredentials: true }
    ).subscribe({
      next: (res: any) => {
        this.isPlacingOrder = false;
        this.orderSuccess = true;
        this.orderId = res.id;
        this.cartService.clearCart(true);
      },
      error: (err: any) => {
        this.isPlacingOrder = false;
        this.paymentError = err.error?.error || 'Failed to place order. Please try again.';
      }
    });
  }

  // ─── Razorpay flow ────────────────────────────────────────────────────────

  private initiateRazorpayPayment() {
    this.isPlacingOrder = true;
    const addr = this.selectedAddress!;

    const createPayload = {
      full_name:      `${addr.first_name} ${addr.last_name}`,
      phone:          addr.phone_no,
      address_line:   addr.apartment ? `${addr.address}, ${addr.apartment}` : addr.address,
      city:           addr.city,
      state:          addr.state,
      pincode:        addr.pin_code,
      payment_method: this.paymentMethod
    };

    // Step 1 — create Razorpay order on backend
    this.orderService.createRazorpayOrder(createPayload).subscribe({
      next: (rzpOrder) => {
        this.isPlacingOrder = false;
        this.openRazorpayModal(rzpOrder);
      },
      error: (err) => {
        this.isPlacingOrder = false;
        this.paymentError = err.error?.error || 'Could not initiate payment. Please try again.';
      }
    });
  }

  private openRazorpayModal(rzpOrder: any) {
    const addr = this.selectedAddress!;

    const options = {
      key:          rzpOrder.key_id,
      amount:       rzpOrder.amount,        // paise — Razorpay displays ₹ automatically
      currency:     rzpOrder.currency,
      name:         'Crumbs',
      description:  `Order #${rzpOrder.order_db_id}`,
      order_id:     rzpOrder.razorpay_order_id,
      prefill: {
        name:    `${addr.first_name} ${addr.last_name}`,
        contact: addr.phone_no,
      },
      theme: {
        color: '#4f46e5'                    // match your brand colour
      },
      modal: {
        ondismiss: () => {
          // User closed the modal without paying
          this.isPlacingOrder = false;
          this.paymentError = 'Payment was cancelled. You can try again.';
        }
      },
      // Step 2 — called by Razorpay on successful payment
      handler: (response: any) => {
        this.verifyPayment(response, rzpOrder.order_db_id);
      }
    };

    const rzp = new Razorpay(options);

    // Handle payment failures inside the modal (wrong card, etc.)
    rzp.on('payment.failed', (response: any) => {
      this.isPlacingOrder = false;
      this.paymentError =
        response.error?.description ||
        'Payment failed. Please try a different payment method.';
      rzp.close();
    });

    rzp.open();
  }

  private verifyPayment(razorpayResponse: any, orderDbId: number) {
    this.isPlacingOrder = true;
    this.paymentError = '';

    const verifyPayload = {
      razorpay_order_id:   razorpayResponse.razorpay_order_id,
      razorpay_payment_id: razorpayResponse.razorpay_payment_id,
      razorpay_signature:  razorpayResponse.razorpay_signature,
      order_db_id:         orderDbId
    };

    this.orderService.verifyRazorpayPayment(verifyPayload).subscribe({
      next: (order) => {
        this.isPlacingOrder = false;
        this.orderSuccess = true;
        this.orderId = String(order.id);
        this.cartService.clearCart(true);
      },
      error: (err) => {
        this.isPlacingOrder = false;
        this.paymentError =
          err.error?.error ||
          'Payment verification failed. Please contact support with your payment ID: ' +
          razorpayResponse.razorpay_payment_id;
      }
    });
  }

  continueShopping() {
    this.router.navigate(['/collections']);
  }
}
