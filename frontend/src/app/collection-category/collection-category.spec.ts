import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CollectionCategory } from './collection-category';

describe('CollectionCategory', () => {
  let component: CollectionCategory;
  let fixture: ComponentFixture<CollectionCategory>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CollectionCategory]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CollectionCategory);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
