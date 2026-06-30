import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { CatalogService } from '../../services/catalog.service';
import { Category as CategoryModel } from '../../models/catalog.models';

@Component({
  selector: 'app-category',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './category.html',
  styleUrl: './category.css'
})
export class Category implements OnInit {

  constructor(
    private router: Router,
    private catalogService: CatalogService
  ) { }

  categories: CategoryModel[] = [];
  selectedCategory: CategoryModel[] = [];
  isLoading = true;

  ngOnInit() {
    this.isLoading = true;
    this.catalogService.getCategories().subscribe({
      next: (categories) => {
        this.categories = categories;
        this.selectedCategory = this.categories.slice(1, 9);
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Error loading categories:', err);
        this.isLoading = false;
      }
    });
  }

  navigate(slug: string) {
    this.router.navigate(['/collections', slug]).then(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

}
