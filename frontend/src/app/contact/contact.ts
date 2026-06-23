import { Component } from '@angular/core';
import { Footer } from "../footer/footer";
import { Header } from "../header/header";

@Component({
  selector: 'app-contact',
  standalone: true,
  imports: [Footer, Header],
  templateUrl: './contact.html',
  styleUrl: './contact.css'
})
export class Contact {

}
