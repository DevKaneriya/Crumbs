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

  constructor(private catalogService: CatalogService) { }

  ngOnInit() {
    this.catalogService.getCategories().subscribe({
      next: (categories) => {
        this.categories = categories;
      },
      error: (err) => console.error('Error loading categories:', err)
    });
  }

}
