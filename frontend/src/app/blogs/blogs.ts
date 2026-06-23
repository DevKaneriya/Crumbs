import { Component } from '@angular/core';
import { Header } from "../header/header";
import { Footer } from "../footer/footer";
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-blogs',
  standalone: true,
  imports: [CommonModule, Header, Footer],
  templateUrl: './blogs.html',
  styleUrl: './blogs.css'
})
export class Blogs {

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
