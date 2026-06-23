import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { Router} from '@angular/router';
import * as categories from '../../Jsonfile/categories.json';

@Component({
  selector: 'app-product-template',
  standalone: true, 
  imports: [CommonModule],
  templateUrl: './product-template.html',
  styleUrls: ['./product-template.css']
})
export class ProductTemplate {

  categories: any = (categories as any).default.categories ;


  constructor(private router: Router ) { }

  navigate(slug: string) {
    this.router.navigate(['/collections', slug]).then(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

}
