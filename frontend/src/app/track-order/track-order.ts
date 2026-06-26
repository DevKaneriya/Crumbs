import { Component } from '@angular/core';
import { Header } from '../header/header';
import { Footer } from '../footer/footer';

@Component({
  selector: 'app-track-order',
  standalone: true,
  imports: [Header, Footer],
  templateUrl: './track-order.html',
  styleUrl: './track-order.css'
})
export class TrackOrder {}
