import { Component } from '@angular/core';
import { Header } from '../header/header';
import { Footer } from '../footer/footer';

@Component({
  selector: 'app-return-refund',
  standalone: true,
  imports: [Header, Footer],
  templateUrl: './return-refund.html',
  styleUrl: './return-refund.css'
})
export class ReturnRefund {}
