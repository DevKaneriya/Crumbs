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

  name = '';
  email = '';
  password = '';

  constructor(
    public auth: Auth,
    private router: Router,
  ) { }

  register() {
    this.auth.register({
      name: this.name,
      email: this.email,
      password: this.password
    }).subscribe(res => {
      console.log('Registered:', res);
      this.router.navigate(['/']);
    });
  }

}
