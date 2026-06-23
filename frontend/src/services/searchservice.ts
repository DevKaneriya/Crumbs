import { Injectable, signal, effect } from '@angular/core';
import products from '../Jsonfile/product.json';
import categoriesData from '../Jsonfile/categories.json';

type Product = typeof products[number];
type Category = (typeof categoriesData)['categories'][number];

@Injectable({
  providedIn: 'root'
})
export class Searchservice {

  isOpen = signal(false);
  mode = signal<'small' | 'large'>('small');
  query = signal('');

  private allProducts = signal<Product[]>(products as Product[]);
  private allCategories = signal<Category[]>(categoriesData.categories as Category[]);

  constructor() {
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
      return { products: [] as Product[], categories: [] as Category[], suggestions: [] as string[] };
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
