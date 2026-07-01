import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-instagram-feed',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './instagram-feed.html',
  styleUrl: './instagram-feed.css'
})
export class InstagramFeed {

  images = [
    { src: 'assets/insta1.png', alt: 'Mukhwas jar with chai' },
    { src: 'assets/insta2.png', alt: 'Colorful fennel seeds in brass bowl' },
    { src: 'assets/insta3.png', alt: 'Gift box of assorted mukhwas' },
    { src: 'assets/insta4.png', alt: 'Silver spoons with mouth fresheners' },
    { src: 'assets/insta5.png', alt: 'Traditional paan presentation' },
    { src: 'assets/insta6.png', alt: 'Festive dining table with mukhwas' }
  ];
}
