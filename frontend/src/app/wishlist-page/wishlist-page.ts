import { Component, OnInit } from '@angular/core';
import { Header } from "../header/header";
import { Footer } from "../footer/footer";
import { Router } from '@angular/router';
import * as productsData from '../../Jsonfile/product.json';
import { CommonModule } from '@angular/common';
import { Wishlistservice } from '../../services/wishlistservice';

@Component({
  selector: 'app-wishlist-page',
  standalone: true,
  imports: [CommonModule, Header, Footer],
  templateUrl: './wishlist-page.html',
  styleUrl: './wishlist-page.css'
})
export class WishlistPage implements OnInit {

  wishlist: any[] = [];
  products: any = (productsData as any).default;
  filteredProducts: any[] = [];

  constructor(
    private router: Router,
    public wishlistService: Wishlistservice
  ) { }

  ngOnInit(): void {
    this.wishlist = this.wishlistService.getWishlist();
    this.filteredProducts = this.products.filter((p: { id: any }) =>
      this.wishlist.includes(p.id)
    );
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
    this.wishlist = this.wishlistService.getWishlist();
    this.filteredProducts = this.products.filter((p: { id: any }) =>
      this.wishlist.includes(p.id)
    );
  }
}
