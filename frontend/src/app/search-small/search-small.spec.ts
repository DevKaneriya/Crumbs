import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchSmall } from './search-small';

describe('SearchSmall', () => {
  let component: SearchSmall;
  let fixture: ComponentFixture<SearchSmall>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SearchSmall]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SearchSmall);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
