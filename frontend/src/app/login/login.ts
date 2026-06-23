import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { Router } from '@angular/router';
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
export class Login {

  email = '';
  password = '';

  constructor(
    public auth: Auth,
    private router: Router,
  ) { }

  login() {
    this.auth.login({ email: this.email, password: this.password }).subscribe(res => {
      this.router.navigate(['/']);
    });
  }

  logout() {
    this.auth.logout().subscribe();
  }

  getUser() {
    this.auth.user().subscribe(res => console.log(res));
  }
}
