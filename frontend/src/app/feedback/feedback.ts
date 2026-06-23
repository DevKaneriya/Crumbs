import { AfterViewInit, Component } from '@angular/core';
import { CommonModule } from '@angular/common';

declare const $: any;

@Component({
  selector: 'app-feedback',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './feedback.html',
  styleUrl: './feedback.css'
})
export class Feedback implements AfterViewInit {

  feedback = [
    {
      header: "Refreshing & Authentic!",
      content: "The flavors are so authentic, it reminds me of traditional mukhwas after meals at home. Love the freshness that lasts long.",
      name: "Anita Sharma",
      stars: 5
    },
    {
      header: "Perfect After-Meal Treat",
      content: "This mukhwas is the perfect way to end a meal. Not too sweet, not too strong — just balanced. My family loves it!",
      name: "Rahul Mehta",
      stars: 5
    },
    {
      header: "So Many Varieties!",
      content: "I ordered the assorted pack and every flavor was unique. The supari mix was my favorite. Definitely ordering again.",
      name: "Sneha Kapoor",
      stars: 5
    },
    {
      header: "Takes Me Back",
      content: "Tastes just like the traditional mukhwas my grandmother used to make. It’s nostalgic and refreshing.",
      name: "Amit Verma",
      stars: 4
    },
    {
      header: "Sugar-Free Surprise",
      content: "I was skeptical about the sugar-free version, but it’s absolutely delicious! Great option for health-conscious people.",
      name: "Priya Nair",
      stars: 5
    },
    {
      header: "Best for Guests",
      content: "Whenever I serve this mukhwas to guests, they always ask where I got it from. Beautiful packaging too!",
      name: "Vikram Joshi",
      stars: 5
    },
    {
      header: "Crunchy & Fresh",
      content: "The crunch of the seeds with the perfect hint of sweetness is amazing. Keeps breath fresh for hours.",
      name: "Neha Gupta",
      stars: 4
    },
    {
      header: "Lovely Pan Flavor",
      content: "The pan-flavored mukhwas is my absolute favorite. It’s sweet, refreshing, and tastes very premium.",
      name: "Rohit Bansal",
      stars: 5
    },
    {
      header: "Great for Gifting",
      content: "I gifted the combo pack to a friend, and she loved it! It’s such a unique and thoughtful gift idea.",
      name: "Kavita Patel",
      stars: 5
    }
  ];

  getArray(n: number): any[] {
  return Array(n);
}



  ngAfterViewInit() {
    setTimeout(() => {
      $(".feedbackcarousel").slick({
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

    }, 500);
  }

}
