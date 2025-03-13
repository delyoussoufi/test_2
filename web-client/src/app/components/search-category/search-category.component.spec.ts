import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { SearchCategoryComponent } from './search-category.component';

describe('SearchCategoryComponent', () => {
  let component: SearchCategoryComponent;
  let fixture: ComponentFixture<SearchCategoryComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ SearchCategoryComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SearchCategoryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
