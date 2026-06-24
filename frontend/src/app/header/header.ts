import { Component, HostListener, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { Wishlistservice } from '../../services/wishlistservice';
import { Searchservice } from '../../services/searchservice';
import { SearchSmall } from '../search-small/search-small';
import { Cartservice } from '../../services/cartservice';
import { Cart } from "../cart/cart";

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [CommonModule, RouterLink, SearchSmall, Cart],
  templateUrl: './header.html',
  styleUrls: ['./header.css']
})
export class Header implements OnInit {
  isMenuOpen = false;

  constructor(
    private router: Router,
    public wishlistService: Wishlistservice,
    public search: Searchservice,
    public cartService: Cartservice
  ) { }

  ngOnInit(): void {
    // Wishlist loads from local storage inside the Wishlistservice constructor
  }

  openSearch() {
    this.isMenuOpen = false;
    this.search.openSmall();
  }

  toggleCart() {
    this.cartService.toggleCart();
    this.isMenuOpen = false;
  }

  closeCart() {
    this.cartService.closeCart();
  }

  toggleMenu() {
    this.isMenuOpen = !this.isMenuOpen;
  }

  @HostListener('window:scroll', [])
  onWindowScroll() {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    document.documentElement.style.setProperty('--scroll', scrollTop + "px");
  }

  navigate(path: string) {
    this.router.navigate([path]);
    if (this.isMenuOpen && window.innerWidth <= 1024) {
      this.toggleMenu();
    }
  }
}
