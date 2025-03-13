import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { SearchBestandComponent } from './search-bestand.component';

describe('SearchBestandComponent', () => {
  let component: SearchBestandComponent;
  let fixture: ComponentFixture<SearchBestandComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ SearchBestandComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SearchBestandComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
