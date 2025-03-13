import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { SearchBestandListComponent } from './search-bestand-list.component';

describe('SearchBestandListComponent', () => {
  let component: SearchBestandListComponent;
  let fixture: ComponentFixture<SearchBestandListComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ SearchBestandListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SearchBestandListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
