import { Component, effect, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { Cartservice, CartItem } from '../../services/cartservice';
import { Auth } from '../../services/auth';
import { CatalogService } from '../../services/catalog.service';
import { AddressService, Address } from '../../services/address-service';
import { ProductList } from '../../models/catalog.models';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Header } from "../header/header";
import { Footer } from "../footer/footer";

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

  /** Controls whether the address picker panel is open */
  showAddressPicker = false;

  /** 'add' = new address form, 'edit' = editing an existing one, null = picker list */
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

  constructor(
    public cartService: Cartservice,
    private auth: Auth,
    private router: Router,
    private catalogService: CatalogService,
    private addressService: AddressService,
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
        // Pick the default address, fall back to the first one
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
          // Auto-select the newly added address
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
      first_name: '',
      last_name: '',
      address: '',
      apartment: '',
      city: '',
      state: '',
      pin_code: '',
      phone_no: '',
      is_default: false
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
  }

  // ─── Place Order ─────────────────────────────────────────────────────────

  placeOrder() {
    if (this.cartItems.length === 0) return;

    if (!this.selectedAddress) {
      alert('Please add a shipping address before placing your order.');
      return;
    }

    this.isPlacingOrder = true;

    const addr = this.selectedAddress;
    const payload = {
      full_name:    `${addr.first_name} ${addr.last_name}`,
      phone:        addr.phone_no,
      address_line: addr.apartment ? `${addr.address}, ${addr.apartment}` : addr.address,
      city:         addr.city,
      state:        addr.state,
      pincode:      addr.pin_code,
      payment_method: this.paymentMethod
    };

    this.http.post<any>(`${environment.apiUrl}/orders/checkout/`, payload, { withCredentials: true }).subscribe({
      next: (res) => {
        this.isPlacingOrder = false;
        this.orderSuccess = true;
        this.orderId = res.id;
        this.cartService.clearCart(true);
      },
      error: (err) => {
        this.isPlacingOrder = false;
        alert(err.error?.error || 'Failed to place order. Please try again.');
        console.error(err);
      }
    });
  }

  continueShopping() {
    this.router.navigate(['/collections']);
  }
}
