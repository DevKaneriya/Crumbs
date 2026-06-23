import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  selector: 'app-why-choose-us',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './why-choose-us.html',
  styleUrl: './why-choose-us.css'
})
export class WhyChooseUs {

  qualities = [
    {
      icon: 'bi bi-star-fill',
      title: 'Premium Ingredients',
      description: 'We use only top-quality natural ingredients for authentic taste.'
    },
    {
      icon: 'bi bi-shield-check',
      title: 'Hygienic Preparation',
      description: 'Prepared in clean, certified kitchens with high hygiene standards.'
    },
    {
      icon: 'bi bi-award',
      title: 'Traditional Taste',
      description: 'Experience rich, traditional flavors crafted with care.'
    },
    {
      icon: 'bi bi-truck',
      title: 'Fast Delivery',
      description: 'Get your favorites delivered fresh and fast to your door.'
    }
  ];


}
