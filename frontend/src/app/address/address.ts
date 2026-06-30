import { Component, OnInit } from '@angular/core';
import { Header } from "../header/header";
import { Footer } from "../footer/footer";
import { Auth } from '../../services/auth';
import { Router } from '@angular/router';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AddressService, Address } from '../../services/address-service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-address',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, Header, Footer],
  templateUrl: './address.html',
  styleUrl: './address.css'
})
export class AddressComponent implements OnInit {

  addresses: Address[] = [];
  addMode = false;
  editIndex: number | null = null;
  addressForm!: FormGroup;
  length: number | null = null;
  user: any = null;
  
  constructor(
    public auth: Auth,
    private router: Router,
    private fb: FormBuilder,
    public addressService: AddressService
  ) { }

  ngOnInit(): void {
    if (!this.auth.isLoggedIn()) {
      this.router.navigate(['/account/login'], { 
        queryParams: { returnUrl: '/account/address' }
      });
      return;
    }

    this.auth.currentUser$.subscribe(user => {
      this.user = user;
    });

    this.loadAddresses();
    this.initForm();
  }

  initForm(address?: Address) {
    this.addressForm = this.fb.group({
      first_name: [address?.first_name || '', Validators.required],
      last_name: [address?.last_name || '', Validators.required],
      address: [address?.address || '', Validators.required],
      apartment: [address?.apartment || ''],
      city: [address?.city || '', Validators.required],
      state: [address?.state || '', Validators.required],
      pin_code: [address?.pin_code || '', Validators.required],
      phone_no: [address?.phone_no || '', Validators.required],
      is_default: [address?.is_default || false]
    });
  }

  loadAddresses() {
    this.addressService.getAddresses().subscribe(data => {
      this.addresses = data;
      this.length = this.addresses.length
    });
  }

  toggleAdd() {
    this.addMode = !this.addMode;
    this.editIndex = null;
    this.initForm();
  }

  saveNew() {
    if (this.addressForm.invalid) return;
    this.addressService.addAddress(this.addressForm.value).subscribe(() => {
      this.loadAddresses();
      this.addMode = false;
    });
  }

  editAddress(index: number) {
    this.editIndex = index;
    this.addMode = false;
    this.initForm(this.addresses[index]);
  }

  updateAddress(id: number) {
    if (this.addressForm.invalid) return;
    this.addressService.updateAddress(id, this.addressForm.value).subscribe(() => {
      this.loadAddresses();
      this.editIndex = null;
    });
  }

  cancelEdit() {
    this.editIndex = null;
  }

  deleteAddress(id: number) {
    this.addressService.deleteAddress(id).subscribe(() => {
      this.loadAddresses();
    });
  }

  logout() {
    this.auth.logout().subscribe();
    this.router.navigate(['/']);
  }
}
