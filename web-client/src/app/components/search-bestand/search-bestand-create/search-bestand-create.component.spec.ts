import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { SearchBestandCreateComponent } from './search-bestand-create.component';

describe('SearchBestandCreateComponent', () => {
  let component: SearchBestandCreateComponent;
  let fixture: ComponentFixture<SearchBestandCreateComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ SearchBestandCreateComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SearchBestandCreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
