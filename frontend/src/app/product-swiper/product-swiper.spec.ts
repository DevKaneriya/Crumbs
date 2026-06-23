import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProductSwiper } from './product-swiper';

describe('ProductSwiper', () => {
  let component: ProductSwiper;
  let fixture: ComponentFixture<ProductSwiper>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProductSwiper]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ProductSwiper);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
