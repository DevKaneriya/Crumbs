import { Component } from '@angular/core';
import { Header } from "../header/header";
import { Footer } from "../footer/footer";
import { CommonModule } from '@angular/common';
import * as productsData from '../../Jsonfile/product.json'
import { ActivatedRoute } from '@angular/router';
import { Cartservice } from '../../services/cartservice';


@Component({
  selector: 'app-product-page',
  standalone: true,
  imports: [Header, Footer, CommonModule],
  templateUrl: './product-page.html',
  styleUrl: './product-page.css'
})
export class ProductPage {

  products: any = (productsData as any).default;
  productsId: any | null;
  selectedProduct: any;
  selectedWeight: { weight: string; original: number; discounted: number } | null = null;
  quantity: number = 1;


  constructor(private route: ActivatedRoute,
    private cartService: Cartservice
  ) { }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.productsId = params.get('short');

      if (this.productsId) {
        this.selectedProduct = this.products.find(
          (p: any) => p.short === this.productsId
        );
      }
    });
    this.imageList = this.selectedProduct.image;
    this.selectedWeight = this.selectedProduct.price[0];
  }

  increaseQty() {
    this.quantity++;
  }

  decreaseQty() {
    if (this.quantity > 1) {
      this.quantity--;
    }
  }

  selectWeight(priceObj: any) {
    this.selectedWeight = priceObj;
  }



  addToCart() {
    if (!this.selectedWeight) return;
    this.cartService.addToCart(
      this.selectedProduct.id,  
      this.selectedWeight.weight,  
      this.quantity                
    );
    alert('Product added to cart!');
  }

  imageList: string[] = [];


  selectedImage = this.imageList[0];
  currentIndex = 0;
  hovering = false;

  selectImage(index: number) {
    this.currentIndex = index;
    this.selectedImage = this.imageList[this.currentIndex];
  }

  nextImage() {
    this.currentIndex = (this.currentIndex + 1) % this.imageList.length;
    this.selectedImage = this.imageList[this.currentIndex];
  }

  prevImage() {
    this.currentIndex = (this.currentIndex - 1 + this.imageList.length) % this.imageList.length;
    this.selectedImage = this.imageList[this.currentIndex];
  }

}
