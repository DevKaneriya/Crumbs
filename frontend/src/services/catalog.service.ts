import { Injectable, signal } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, map, shareReplay, tap } from 'rxjs';
import { environment } from '../environments/environment';
import {
  Category,
  CategoryWithProducts,
  Product,
  ProductList
} from '../models/catalog.models';

@Injectable({
  providedIn: 'root'
})
export class CatalogService {
  private apiUrl = `${environment.apiUrl}/catalog`;

  private readonly categoryRouteOrder = [
    'all-products',
    'best-sellers',
    'sugar-free',
    'mukhwas',
    'churan',
    'supari',
    'pan',
    'tiny-miny',
    'gifts-combos',
  ];
  
  // Cache for categories and products
  private categoriesCache$ = signal<Category[] | null>(null);
  private productsCache$ = signal<ProductList[] | null>(null);

  constructor(private http: HttpClient) { }

  private sortCategories(categories: Category[]): Category[] {
    return [...categories].sort((a, b) => {
      const orderA = a.display_order ?? this.categoryRouteOrder.indexOf(a.route);
      const orderB = b.display_order ?? this.categoryRouteOrder.indexOf(b.route);
      return (orderA === -1 ? 999 : orderA) - (orderB === -1 ? 999 : orderB);
    });
  }

  // ============== Categories ==============

  /**
   * Get all categories
   */
  getCategories(): Observable<Category[]> {
    return this.http.get<Category[]>(`${this.apiUrl}/categories/`).pipe(
      map(categories => this.sortCategories(categories)),
      tap(categories => this.categoriesCache$.set(categories)),
      shareReplay(1)
    );
  }

  /**
   * Get a single category by route
   */
  getCategory(route: string): Observable<Category> {
    return this.http.get<Category>(`${this.apiUrl}/categories/${route}/`);
  }

  /**
   * Get category with its products
   */
  getCategoryWithProducts(route: string): Observable<CategoryWithProducts> {
    return this.http.get<CategoryWithProducts>(
      `${this.apiUrl}/categories/${route}/products/`
    );
  }

  // ============== Products ==============

  /**
   * Get all products with optional filters
   */
  getProducts(filters?: {
    search?: string;
    category?: string;
    ordering?: string;
  }): Observable<ProductList[]> {
    let params = new HttpParams();

    if (filters?.search) {
      params = params.set('search', filters.search);
    }
    if (filters?.category) {
      params = params.set('categories__route', filters.category);
    }
    if (filters?.ordering) {
      params = params.set('ordering', filters.ordering);
    }

    return this.http.get<ProductList[]>(`${this.apiUrl}/products/`, { params }).pipe(
      tap(products => this.productsCache$.set(products)),
      shareReplay(1)
    );
  }

  /**
   * Get a single product by short (slug)
   */
  getProduct(short: string): Observable<Product> {
    return this.http.get<Product>(`${this.apiUrl}/products/${short}/`);
  }
}
