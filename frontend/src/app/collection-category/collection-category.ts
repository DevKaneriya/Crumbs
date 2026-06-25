import { Component, OnInit } from '@angular/core';
import { Header } from "../header/header";
import { Footer } from "../footer/footer";
import { ProductTemplate } from "../product-template/product-template";
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { Wishlistservice } from '../../services/wishlistservice';
import { CatalogService } from '../../services/catalog.service';
import { ProductList, Category } from '../../models/catalog.models';

@Component({
  selector: 'app-collection-category',
  standalone: true,
  imports: [Header, Footer, ProductTemplate, CommonModule],
  templateUrl: './collection-category.html',
  styleUrl: './collection-category.css'
})
export class CollectionCategory implements OnInit {

  categoriesId: string | null = null;
  filteredProducts: ProductList[] = [];
  currentCategory: Category | null = null;

  constructor(
    private activeRoute: ActivatedRoute,
    private router: Router,
    public wishlistService: Wishlistservice,
    private catalogService: CatalogService
  ) { }

  navigate(slug: string) {
    this.router.navigate(['/products', slug]).then(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  ngOnInit(): void {
    this.activeRoute.paramMap.subscribe(params => {
      this.categoriesId = params.get('route');

      if (this.categoriesId === 'all-products') {
        // Load all products
        this.catalogService.getProducts().subscribe({
          next: (products) => {
            this.filteredProducts = products;
          },
          error: (err) => console.error('Error loading products:', err)
        });
        
        // Load the "all-products" category info
        this.catalogService.getCategory('all-products').subscribe({
          next: (category) => {
            this.currentCategory = category;
          },
          error: (err) => console.error('Error loading category:', err)
        });
      } else if (this.categoriesId) {
        // Load products for specific category
        this.catalogService.getProducts({ category: this.categoriesId }).subscribe({
          next: (products) => {
            this.filteredProducts = products;
          },
          error: (err) => console.error('Error loading products:', err)
        });
        
        // Load category info
        this.catalogService.getCategory(this.categoriesId).subscribe({
          next: (category) => {
            this.currentCategory = category;
          },
          error: (err) => console.error('Error loading category:', err)
        });
      } else {
        this.filteredProducts = [];
      }
    });
  }


  toggleWishlist(product: any, event: Event) {
    event.stopPropagation();
    this.wishlistService.toggleWishlist(product.id);
  }

  isInWishlist(product: any) {
    return this.wishlistService.isInWishlist(product.id);
  }


}
