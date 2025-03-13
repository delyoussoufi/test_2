import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { SearchCategoryEditComponent } from './search-category-edit.component';

describe('SearchCategoryEditComponent', () => {
  let component: SearchCategoryEditComponent;
  let fixture: ComponentFixture<SearchCategoryEditComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ SearchCategoryEditComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SearchCategoryEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
