import { CommonModule } from '@angular/common';
import { Component, HostListener, computed } from '@angular/core';
import { Searchservice } from '../../services/searchservice';
import { Router } from '@angular/router';



@Component({
  selector: 'app-search-small',
  standalone: true,
  imports: [ CommonModule ],
  templateUrl: './search-small.html',
  styleUrl: './search-small.css'
})
export class SearchSmall {

  constructor(
    private router: Router,
    public state: Searchservice) { }

  results = computed(() => this.state.resultsFor(this.state.query()));

  navCol(slug: string) {
    this.router.navigate(['/collections', slug]).then(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
      this.close();
    });
  }

  navPro(slug: string) {
    this.router.navigate(['/products', slug]).then(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
      this.close();
    });
  }

  set(val: string) {
    this.state.setQuery(val);
  }

  onInput(evt: Event) {
    const val = (evt.target as HTMLInputElement).value;
    this.state.setQuery(val);
  }

  close() { this.state.reset(); }

  @HostListener('window:keydown.escape') onEsc() { this.close(); }

}
