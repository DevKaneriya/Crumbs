import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../environments/environment';

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
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/accounts/address/`;

  getAddresses(): Observable<Address[]> {
    return this.http.get<Address[]>(this.apiUrl, { withCredentials: true });
  }

  addAddress(address: Address): Observable<Address> {
    return this.http.post<Address>(this.apiUrl, address, { withCredentials: true });
  }

  updateAddress(id: number, address: Address): Observable<Address> {
    return this.http.put<Address>(`${this.apiUrl}${id}/`, address, { withCredentials: true });
  }

  deleteAddress(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}${id}/`, { withCredentials: true });
  }
}
