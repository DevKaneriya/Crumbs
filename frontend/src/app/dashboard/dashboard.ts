import { Component, OnInit } from '@angular/core';
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
export class Dashboard implements OnInit {

  isLoggingOut = false;
  logoutError = '';

  constructor(
    public auth: Auth,
    private router: Router,
  ){}

  ngOnInit() {
    // Double-check authentication on component init
    if (!this.auth.isLoggedIn()) {
      this.router.navigate(['/account/login'], { 
        queryParams: { returnUrl: '/account' }
      });
    }
  }

  logout() {
    this.isLoggingOut = true;
    this.logoutError = '';
    this.auth.logout().subscribe({
      next: () => {
        this.isLoggingOut = false;
        this.router.navigate(['/account/login'], { replaceUrl: true });
      },
      error: () => {
        this.isLoggingOut = false;
        this.logoutError = 'Logout failed. Please try again.';
      }
    });
  }

}
