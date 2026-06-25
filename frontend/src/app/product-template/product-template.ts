import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CatalogService } from '../../services/catalog.service';
import { Category } from '../../models/catalog.models';

@Component({
  selector: 'app-product-template',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './product-template.html',
  styleUrls: ['./product-template.css']
})
export class ProductTemplate implements OnInit {

  categories: Category[] = [];

  constructor(
    private router: Router,
    private catalogService: CatalogService
  ) { }

  ngOnInit() {
    this.catalogService.getCategories().subscribe({
      next: (categories) => {
        this.categories = categories;
      },
      error: (err) => console.error('Error loading categories:', err)
    });
  }

  navigate(slug: string) {
    this.router.navigate(['/collections', slug]).then(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

}
