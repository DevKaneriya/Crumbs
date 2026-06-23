import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import * as productsData from '../../Jsonfile/product.json';
import { Router } from '@angular/router';
import { Wishlistservice } from '../../services/wishlistservice';


declare const $: any;

@Component({
  selector: 'app-product-swiper',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './product-swiper.html',
  styleUrls: ['./product-swiper.css']
})
export class ProductSwiper {

  products: any = (productsData as any).default;

  constructor(
    private router: Router,
    public wishlistService: Wishlistservice
  ) { }

  navigate(slug: string) {

    if (this.isDragging) { this.isDragging = false; return; }

    this.router.navigate(["/products", slug]).then(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }


  toggleWishlist(product: any, event: Event) {
    event.stopPropagation();
    this.wishlistService.toggleWishlist(product.id);
  }

  isInWishlist(product: any) {
    return this.wishlistService.isInWishlist(product.id);
  }

  isDragging = false;
  mobileBreakpoint = 1025;

  ngAfterViewInit() {
    setTimeout(() => {
      $(".product-carousel").slick({
        dots: false,
        arrows: false,
        infinite: true,
        slidesToScroll: 1,
        slidesToShow: 3,
        accessibility: true,
        variableWidth: true,
        focusOnSelect: false,
        centerMode: false,
        autoplay: true,
        autoplaySpeed: 3000,
        responsive: [
          {
            breakpoint: 1200,
            settings: { slidesToShow: 2, slidesToScroll: 2, arrows: false },
          },
          {
            breakpoint: 767,
            settings: { slidesToShow: 1, slidesToScroll: 1, arrows: false },
          },
          {
            breakpoint: 576,
            settings: { slidesToShow: 1, slidesToScroll: 1, arrows: false },
          },
        ],
      });

      if (window.innerWidth > this.mobileBreakpoint) {

        $(".product-carousel").on("mousedown touchstart", () => this.isDragging = false);
        $(".product-carousel").on("mousemove touchmove", () => this.isDragging = true);
      }

      $("#SliderArrowL").on("click", () => $(".product-carousel").slick("slickPrev"));
      $("#SliderArrowR").on("click", () => $(".product-carousel").slick("slickNext"));

    }, 500);
  }

}