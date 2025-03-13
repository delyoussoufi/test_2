import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DigitalisatImageViewComponent } from './digitalisat-image-view.component';

describe('DigitalisatImageViewComponent', () => {
  let component: DigitalisatImageViewComponent;
  let fixture: ComponentFixture<DigitalisatImageViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DigitalisatImageViewComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DigitalisatImageViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
