import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DigitalisatEditComponent } from './digitalisat-edit.component';

describe('DigitalisatEditComponent', () => {
  let component: DigitalisatEditComponent;
  let fixture: ComponentFixture<DigitalisatEditComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DigitalisatEditComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DigitalisatEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
