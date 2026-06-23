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

  @HostListener('window:scroll')
  onScroll() {
    this.isVisible = window.scrollY > 100; 
  }

  scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}
