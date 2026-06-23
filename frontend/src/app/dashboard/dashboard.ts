import { Component } from '@angular/core';
import { Auth } from '../../services/auth';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { Header } from "../header/header";
import { Footer } from "../footer/footer";

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, Header, Footer],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css'
})
export class Dashboard  {

  constructor(
    public auth: Auth,
    private router: Router,
  ){}


  logout() {
    this.auth.logout().subscribe();
    this.router.navigate(['/']);
  }

}
