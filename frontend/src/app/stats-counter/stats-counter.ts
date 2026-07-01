import { Component, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Stat {
  icon: string;
  value: number;
  suffix: string;
  label: string;
  current: number;
}

@Component({
  selector: 'app-stats-counter',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './stats-counter.html',
  styleUrl: './stats-counter.css'
})
export class StatsCounter implements AfterViewInit {
  @ViewChild('statsSection') statsSection!: ElementRef;

  stats: Stat[] = [
    { icon: 'fas fa-smile-beam', value: 5000, suffix: '+', label: 'Happy Customers', current: 0 },
    { icon: 'fas fa-box-open', value: 50, suffix: '+', label: 'Premium Products', current: 0 },
    { icon: 'fas fa-award', value: 10, suffix: '+', label: 'Years of Trust', current: 0 },
    { icon: 'fas fa-shipping-fast', value: 25000, suffix: '+', label: 'Orders Delivered', current: 0 }
  ];

  hasAnimated = false;

  ngAfterViewInit() {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !this.hasAnimated) {
          this.hasAnimated = true;
          this.animateCounters();
          observer.disconnect();
        }
      },
      { threshold: 0.3 }
    );
    observer.observe(this.statsSection.nativeElement);
  }

  private animateCounters() {
    const duration = 2000; // 2 seconds
    const fps = 60;
    const totalFrames = (duration / 1000) * fps;

    this.stats.forEach(stat => {
      let frame = 0;
      const increment = stat.value / totalFrames;
      const timer = setInterval(() => {
        frame++;
        stat.current = Math.min(Math.round(increment * frame), stat.value);
        if (frame >= totalFrames) {
          stat.current = stat.value;
          clearInterval(timer);
        }
      }, 1000 / fps);
    });
  }

  formatNumber(n: number): string {
    if (n >= 1000) {
      return n.toLocaleString('en-IN');
    }
    return n.toString();
  }
}
