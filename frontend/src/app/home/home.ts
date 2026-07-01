import { Component } from '@angular/core';
import { Header } from "../header/header";
import { ProductTemplate } from "../product-template/product-template";
import { HeroPage } from "../hero-page/hero-page";
import { ProductSwiper } from "../product-swiper/product-swiper";
import { Footer } from "../footer/footer";
import { Feedback } from "../feedback/feedback";
import { Category } from "../category/category";
import { Marque } from "../marque/marque";
import { SpeciallyCurated } from "../specially-curated/specially-curated";
import { WhyChooseUs } from "../why-choose-us/why-choose-us";
import { BrandStory } from "../brand-story/brand-story";
import { StatsCounter } from "../stats-counter/stats-counter";
import { InstagramFeed } from "../instagram-feed/instagram-feed";
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, Header, ProductTemplate, HeroPage, ProductSwiper, Category, Feedback, Footer, Marque, SpeciallyCurated, WhyChooseUs, BrandStory, StatsCounter, InstagramFeed],
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class Home {

  constructor(private router: Router) { }

  navigate(slug: string) {
    this.router.navigate(['/blogs', slug]).then(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  blogs = [
    {
      img: "assets/blogs/blog1.png",
      title: "The Story Behind the Word Mukhwas",
      route: "story-behind-the-word-mukhwas"
    },
    {
      img: "assets/blogs/blog2.jpg",
      title: "Health Benefits of Mukhwas Ingredients",
      route: "health-benefits-of-mukhwas-ingredients"
    },
    {
      img: "assets/blogs/blog3.png",
      title: "Why Restaurants Always Serve Fennel Seeds After Meals",
      route: "why-restaurants-serve-fennel-seeds-after-meals"
    }
  ]

}
