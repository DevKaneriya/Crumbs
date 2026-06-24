import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { Auth } from '../../services/auth';
import { Header } from '../header/header';
import { Footer } from '../footer/footer';

@Component({
  selector: 'app-reset-password',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, Header, Footer],
  templateUrl: './reset-password.html',
  styleUrl: './reset-password.css'
})
export class ResetPassword implements OnInit {
  uid = '';
  token = '';
  newPassword = '';
  confirmPassword = '';
  isSubmitting = false;
  errorMessage = '';
  successMessage = '';
  invalidLink = false;

  constructor(
    private auth: Auth,
    private router: Router,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    // Get uid and token from query parameters
    this.route.queryParams.subscribe(params => {
      // Angular's ActivatedRoute automatically decodes URL parameters
      // But in case they're double-encoded, we handle it here
      this.uid = params['uid'] || '';
      this.token = params['token'] || '';
      
      console.log('Received URL params:', { uid: this.uid, token: this.token });
      
      if (!this.uid || !this.token) {
        this.invalidLink = true;
        this.errorMessage = 'Invalid password reset link.';
      }
    });
  }

  onSubmit() {
    this.errorMessage = '';
    this.successMessage = '';

    // Validation
    if (!this.newPassword || !this.confirmPassword) {
      this.errorMessage = 'Please fill in all fields.';
      return;
    }

    if (this.newPassword.length < 8) {
      this.errorMessage = 'Password must be at least 8 characters long.';
      return;
    }

    if (this.newPassword !== this.confirmPassword) {
      this.errorMessage = 'Passwords do not match.';
      return;
    }

    this.isSubmitting = true;

    this.auth.confirmPasswordReset(this.uid, this.token, this.newPassword).subscribe({
      next: (response) => {
        this.isSubmitting = false;
        this.successMessage = response.message;
        
        // Redirect to login after 3 seconds
        setTimeout(() => {
          this.router.navigate(['/account/login']);
        }, 3000);
      },
      error: (error) => {
        this.isSubmitting = false;
        
        if (error.error?.token) {
          this.errorMessage = 'This password reset link has expired or is invalid. Please request a new one.';
        } else if (error.error?.uid) {
          this.errorMessage = 'Invalid reset link. Please request a new password reset.';
        } else if (error.error?.new_password) {
          this.errorMessage = Array.isArray(error.error.new_password) 
            ? error.error.new_password.join(' ')
            : error.error.new_password;
        } else {
          this.errorMessage = error.error?.message || 'An error occurred. Please try again.';
        }
      }
    });
  }
}
