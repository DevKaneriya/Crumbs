import { Component, OnInit } from '@angular/core';
import { Header } from "../header/header";
import { Footer } from "../footer/footer";
import { ProductTemplate } from "../product-template/product-template";
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { Wishlistservice } from '../../services/wishlistservice';
import * as productsData from '../../Jsonfile/product.json';
import * as categories from '../../Jsonfile/categories.json';

@Component({
  selector: 'app-collection-category',
  standalone: true,
  imports: [Header, Footer, ProductTemplate, CommonModule ],
  templateUrl: './collection-category.html',
  styleUrl: './collection-category.css'
})
export class CollectionCategory implements OnInit {

  categoriesId: string | null = null;
  filteredProducts: any[] = [];
  categories: any = (categories as any).default.categories;
  products: any = (productsData as any).default;

  constructor(
    private activeRoute: ActivatedRoute,
    private router: Router,
    public wishlistService: Wishlistservice
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
        this.filteredProducts = this.products;
      } else if (this.categoriesId) {
        this.filteredProducts = this.products.filter(
          (product: any) => product.categories.includes(this.categoriesId)
        );
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
