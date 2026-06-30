import { Component, OnInit } from '@angular/core';
import { Header } from "../header/header";
import { Footer } from "../footer/footer";
import { CommonModule } from '@angular/common';
import { CatalogService } from '../../services/catalog.service';
import { Category } from '../../models/catalog.models';

@Component({
  selector: 'app-collection-page',
  standalone: true,
  imports: [Header, Footer, CommonModule],
  templateUrl: './collection-page.html',
  styleUrl: './collection-page.css'
})
export class CollectionPage implements OnInit {

  categories: Category[] = [];
  isLoading = true;

  constructor(private catalogService: CatalogService) { }

  ngOnInit() {
    this.isLoading = true;
    this.catalogService.getCategories().subscribe({
      next: (categories) => {
        this.categories = categories;
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Error loading categories:', err);
        this.isLoading = false;
      }
    });
  }

}
