import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { Auth } from '../../services/auth';
import { FormsModule } from '@angular/forms';
import { Header } from "../header/header";
import { Footer } from "../footer/footer";


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, Header, Footer],
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export class Login implements OnInit {

  email = '';
  password = '';
  isSubmitting = false;
  errorMessage = '';
  successMessage = '';
  isLoggingOut = false;
  private returnUrl: string = '/account';

  constructor(
    public auth: Auth,
    private router: Router,
    private route: ActivatedRoute,
  ) { }

  ngOnInit() {
    // Get return URL from query params or default to /account
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/account';
  }

  login() {
    this.isSubmitting = true;
    this.errorMessage = '';
    this.successMessage = '';
    this.auth.login({ email: this.email, password: this.password }).subscribe({
      next: () => {
        this.isSubmitting = false;
        this.successMessage = 'Login successful. Redirecting...';
        this.router.navigateByUrl(this.returnUrl, { replaceUrl: true });
      },
      error: () => {
        this.isSubmitting = false;
        this.errorMessage = 'Login failed. Please check your email and password.';
      }
    });
  }

  logout() {
    this.isLoggingOut = true;
    this.auth.logout().subscribe({
      next: () => {
        this.isLoggingOut = false;
        this.router.navigate(['/account/login'], { replaceUrl: true });
      },
      error: () => {
        this.isLoggingOut = false;
        this.errorMessage = 'Logout failed. Please try again.';
      }
    });
  }

  getUser() {
    this.auth.user().subscribe(res => console.log(res));
  }
}
