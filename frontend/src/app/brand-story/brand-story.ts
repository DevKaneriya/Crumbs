import { Component, OnInit, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-brand-story',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './brand-story.html',
  styleUrl: './brand-story.css'
})
export class BrandStory implements AfterViewInit {
  isVisible = false;

  @ViewChild('storySection') storySection!: ElementRef;

  constructor(private router: Router) {}

  ngAfterViewInit() {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          this.isVisible = true;
          observer.disconnect();
        }
      },
      { threshold: 0.2 }
    );
    observer.observe(this.storySection.nativeElement);
  }

  navigate() {
    this.router.navigate(['/collections']).then(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
}
