import { CommonModule } from '@angular/common';
import { Component, signal, HostListener } from '@angular/core';
import { RouterOutlet } from '@angular/router';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CommonModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('angular-project');

  isVisible = false;
  scrollProgress = 0;
  circumference = 2 * Math.PI * 21; // 2πr where r=21

  @HostListener('window:scroll')
  onScroll() {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    
    this.scrollProgress = (scrollTop / scrollHeight) * 100;
    this.isVisible = scrollTop > 100; 
  }

  scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}
