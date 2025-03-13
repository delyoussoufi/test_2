import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DigitalisatInfoComponent } from './digitalisat-info.component';

describe('DigitalisatInfoComponent', () => {
  let component: DigitalisatInfoComponent;
  let fixture: ComponentFixture<DigitalisatInfoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DigitalisatInfoComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DigitalisatInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
