import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { SearchCategoryCreateComponent } from './search-category-create.component';

describe('SearchCategoryCreateComponent', () => {
  let component: SearchCategoryCreateComponent;
  let fixture: ComponentFixture<SearchCategoryCreateComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ SearchCategoryCreateComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SearchCategoryCreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
