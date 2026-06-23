import { Component } from '@angular/core';
import { Header } from "../header/header";
import { Footer } from "../footer/footer";
@Component({
  selector: 'app-privacy-policy',
  standalone: true,
  imports: [Header, Footer],
  templateUrl: './privacy-policy.html',
  styleUrl: './privacy-policy.css'
})
export class PrivacyPolicy {

}
