import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { DigitalisatListComponent } from './digitalisat-list.component';

describe('DigitalisateListComponent', () => {
  let component: DigitalisatListComponent;
  let fixture: ComponentFixture<DigitalisatListComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ DigitalisatListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DigitalisatListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
