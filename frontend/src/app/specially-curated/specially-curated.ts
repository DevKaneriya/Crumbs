import { CommonModule } from '@angular/common';
import { Component} from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-specially-curated',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './specially-curated.html',
  styleUrl: './specially-curated.css'
})
export class SpeciallyCurated {
    
  constructor(private router: Router ) { }

  navigate(slug: string) {
    this.router.navigate([slug]).then(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
  
}
