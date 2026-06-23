import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WishlistPage } from './wishlist-page';

describe('WatchlistPage', () => {
  let component: WishlistPage;
  let fixture: ComponentFixture<WishlistPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [WishlistPage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(WishlistPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
