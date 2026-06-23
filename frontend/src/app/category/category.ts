import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import * as categories from '../../Jsonfile/categories.json'
import { Router } from '@angular/router';
@Component({
  selector: 'app-category',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './category.html',
  styleUrl: './category.css'
})
export class Category {

  constructor(private router: Router) { }

  categories:any = (categories as any).default.categories;

  selectedCategory: any = [];

  ngOnInit() {
    this.selectedCategory = this.categories.slice(1, 9);
  }

  navigate(slug: string) {
    this.router.navigate(['/collections', slug]).then(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

}
