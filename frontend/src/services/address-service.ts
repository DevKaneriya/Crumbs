import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

export interface Address {
  id?: number;
  first_name: string;
  last_name: string;
  address: string;
  apartment?: string;
  city: string;
  state: string;
  pin_code: string;
  phone_no: string;
  is_default: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class AddressService {

  private storageKey = 'addresses';

  constructor() {
    if (this.isBrowser() && !localStorage.getItem(this.storageKey)) {
      const initialAddresses: Address[] = [
        {
          id: 1,
          first_name: 'John',
          last_name: 'Doe',
          address: '123 Main Street',
          apartment: 'Apt 4B',
          city: 'Mumbai',
          state: 'Maharashtra',
          pin_code: '400001',
          phone_no: '9876543210',
          is_default: true
        }
      ];
      localStorage.setItem(this.storageKey, JSON.stringify(initialAddresses));
    }
  }

  private getStored(): Address[] {
    if (!this.isBrowser()) return [];
    return JSON.parse(localStorage.getItem(this.storageKey) || '[]');
  }

  private saveStored(addresses: Address[]) {
    if (this.isBrowser()) {
      localStorage.setItem(this.storageKey, JSON.stringify(addresses));
    }
  }

  getAddresses(): Observable<Address[]> {
    return of(this.getStored());
  }

  addAddress(address: Address): Observable<Address> {
    const list = this.getStored();
    const newAddress = { ...address, id: Date.now() };
    if (newAddress.is_default) {
      list.forEach(a => a.is_default = false);
    }
    list.push(newAddress);
    this.saveStored(list);
    return of(newAddress);
  }

  updateAddress(id: number, address: Address): Observable<Address> {
    const list = this.getStored();
    const index = list.findIndex(a => a.id === id);
    if (index !== -1) {
      const updated = { ...list[index], ...address };
      if (updated.is_default) {
        list.forEach(a => a.is_default = false);
      }
      list[index] = updated;
      this.saveStored(list);
      return of(updated);
    }
    return of(address);
  }

  deleteAddress(id: number): Observable<any> {
    let list = this.getStored();
    list = list.filter(a => a.id !== id);
    this.saveStored(list);
    return of({ success: true });
  }

  private isBrowser() {
    return typeof window !== 'undefined' && typeof localStorage !== 'undefined';
  }
}
