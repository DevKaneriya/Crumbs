import { Component } from '@angular/core';
import { Header } from '../header/header';
import { Footer } from '../footer/footer';

@Component({
  selector: 'app-customized-order',
  standalone: true,
  imports: [Header, Footer],
  templateUrl: './customized-order.html',
  styleUrl: './customized-order.css'
})
export class CustomizedOrder {}
