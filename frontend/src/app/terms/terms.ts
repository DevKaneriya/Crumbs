import { Component } from '@angular/core';
import { Header } from "../header/header";
import { Footer } from "../footer/footer";

@Component({
  selector: 'app-terms',
  standalone: true,
  imports: [Header, Footer],
  templateUrl: './terms.html',
  styleUrl: './terms.css'
})
export class Terms {

}
