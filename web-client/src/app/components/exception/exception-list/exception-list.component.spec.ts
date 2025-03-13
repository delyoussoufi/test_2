import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { ExceptionListComponent } from './exception-list.component';

describe('ExceptionListComponent', () => {
  let component: ExceptionListComponent;
  let fixture: ComponentFixture<ExceptionListComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ ExceptionListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ExceptionListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
