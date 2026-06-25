import { Component, OnInit } from '@angular/core';
import { Header } from "../header/header";
import { Footer } from "../footer/footer";
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Wishlistservice } from '../../services/wishlistservice';
import { CatalogService } from '../../services/catalog.service';
import { ProductList } from '../../models/catalog.models';

@Component({
  selector: 'app-wishlist-page',
  standalone: true,
  imports: [CommonModule, Header, Footer],
  templateUrl: './wishlist-page.html',
  styleUrl: './wishlist-page.css'
})
export class WishlistPage implements OnInit {

  wishlist: any[] = [];
  filteredProducts: ProductList[] = [];

  constructor(
    private router: Router,
    public wishlistService: Wishlistservice,
    private catalogService: CatalogService
  ) { }

  ngOnInit(): void {
    this.loadWishlist();
  }

  loadWishlist() {
    this.wishlist = this.wishlistService.getWishlist();
    
    // Load all products and filter by wishlist
    this.catalogService.getProducts().subscribe({
      next: (products) => {
        this.filteredProducts = products.filter((p: ProductList) =>
          this.wishlist.includes(p.id)
        );
      },
      error: (err) => console.error('Error loading products:', err)
    });
  }

  navigate(slug: string) {
    this.router.navigate(['/products', slug]).then(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  navigateTo() {
    this.router.navigate(["/collections/all-products"]).then(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  toggleWishlist(product: any, event: Event) {
    event.stopPropagation();
    this.wishlistService.removeFromWishlist(product.id);
    this.loadWishlist();
  }
}
