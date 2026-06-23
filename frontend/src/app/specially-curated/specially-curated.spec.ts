import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SpeciallyCurated } from './specially-curated';

describe('SpeciallyCurated', () => {
  let component: SpeciallyCurated;
  let fixture: ComponentFixture<SpeciallyCurated>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SpeciallyCurated]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SpeciallyCurated);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
