import { Component } from '@angular/core';
import { Header } from "../header/header";
import { Footer } from "../footer/footer";
import { CommonModule } from '@angular/common';
import * as categories from '../../Jsonfile/categories.json'

@Component({
  selector: 'app-collection-page',
  standalone: true,
  imports: [Header, Footer, CommonModule],
  templateUrl: './collection-page.html',
  styleUrl: './collection-page.css'
})
export class CollectionPage {

  categories:any = (categories as any).default.categories;

}
