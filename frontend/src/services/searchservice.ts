import { Injectable, signal, effect } from '@angular/core';
import { CatalogService } from './catalog.service';
import { ProductList, Category } from '../models/catalog.models';

@Injectable({
  providedIn: 'root'
})
export class Searchservice {

  isOpen = signal(false);
  mode = signal<'small' | 'large'>('small');
  query = signal('');

  private allProducts = signal<ProductList[]>([]);
  private allCategories = signal<Category[]>([]);

  constructor(private catalogService: CatalogService) {
    // Load products and categories from API
    this.loadData();

    if (this.isBrowser()) {
      effect(() => {
        if (this.isOpen()) {
          document.body.classList.add('no-scroll');
        } else {
          document.body.classList.remove('no-scroll');
        }
      });
    }
  }

  private loadData() {
    this.catalogService.getProducts().subscribe({
      next: (products) => this.allProducts.set(products),
      error: (err) => console.error('Error loading products:', err)
    });

    this.catalogService.getCategories().subscribe({
      next: (categories) => this.allCategories.set(categories),
      error: (err) => console.error('Error loading categories:', err)
    });
  }

  openSmall() {
    this.isOpen.set(true);
    this.mode.set('small');
  }

  openLarge() {
    this.isOpen.set(true);
    this.mode.set('large');
  }

  setQuery(q: string) {
    this.query.set(q);
  }

  reset() {
    this.query.set('');
    this.mode.set('small');
    this.isOpen.set(false);
  }

  resultsFor(query: string) {
    const q = query.trim().toLowerCase();
    if (!q) {
      return { products: [] as ProductList[], categories: [] as Category[], suggestions: [] as string[] };
    }

    const prods = this.allProducts().filter(p =>
      p.name.toLowerCase().includes(q) || p.short.toLowerCase().includes(q)
    );

    const cats = this.allCategories().filter(c =>
      c.name.toLowerCase().includes(q) || c.text.toLowerCase().includes(q) || c.route.toLowerCase().includes(q)
    );

    const wordSet = new Set<string>();
    for (const p of this.allProducts()) {
      p.name.split(/\s+/).forEach(w => {
        const lw = w.toLowerCase();
        if (lw.startsWith(q)) wordSet.add(lw);
      });
    }

    for (const c of this.allCategories()) {
      const lw = c.name.toLowerCase();
      if (lw.startsWith(q)) wordSet.add(lw);
    }

    const suggestions = Array.from(wordSet).sort().slice(0, 8);
    return { products: prods, categories: cats, suggestions };
  }

  private isBrowser() {
    return typeof window !== 'undefined';
  }
}
