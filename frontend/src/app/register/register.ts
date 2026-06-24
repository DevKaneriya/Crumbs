import { Component } from '@angular/core';
import { Auth } from '../../services/auth';
import { Footer } from "../footer/footer";
import { Header } from "../header/header";
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';


@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, Footer, Header, FormsModule],
  templateUrl: './register.html',
  styleUrl: './register.css'
})
export class Register {

  firstName = '';
  lastName = '';
  email = '';
  password = '';
  isSubmitting = false;
  errorMessage = '';
  successMessage = '';

  constructor(
    public auth: Auth,
    private router: Router,
  ) { }

  register() {
    this.isSubmitting = true;
    this.errorMessage = '';
    this.successMessage = '';
    this.auth.register({
      first_name: this.firstName,
      last_name: this.lastName,
      email: this.email,
      password: this.password
    }).subscribe({
      next: () => {
        this.isSubmitting = false;
        this.successMessage = 'Account created successfully. Redirecting to your account...';
        this.router.navigate(['/account'], { replaceUrl: true });
      },
      error: () => {
        this.isSubmitting = false;
        this.errorMessage = 'Registration failed. Please check your details and try again.';
      }
    });
  }

}
