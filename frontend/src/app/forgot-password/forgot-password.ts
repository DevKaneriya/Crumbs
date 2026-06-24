import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { Auth } from '../../services/auth';
import { Header } from '../header/header';
import { Footer } from '../footer/footer';

@Component({
  selector: 'app-forgot-password',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, Header, Footer],
  templateUrl: './forgot-password.html',
  styleUrl: './forgot-password.css'
})
export class ForgotPassword {
  email = '';
  isSubmitting = false;
  errorMessage = '';
  successMessage = '';

  constructor(
    private auth: Auth,
    private router: Router
  ) {}

  onSubmit() {
    if (!this.email) {
      this.errorMessage = 'Please enter your email address.';
      return;
    }

    this.isSubmitting = true;
    this.errorMessage = '';
    this.successMessage = '';

    this.auth.requestPasswordReset(this.email).subscribe({
      next: (response) => {
        this.isSubmitting = false;
        this.successMessage = response.message;
        this.email = '';
      },
      error: (error) => {
        this.isSubmitting = false;
        this.errorMessage = error.error?.message || 'An error occurred. Please try again.';
      }
    });
  }
}
