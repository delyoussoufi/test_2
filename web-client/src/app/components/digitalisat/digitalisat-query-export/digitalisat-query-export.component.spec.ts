import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DigitalisatQueryExportComponent } from './digitalisat-query-export.component';

describe('DigitalisatQueryExportComponent', () => {
  let component: DigitalisatQueryExportComponent;
  let fixture: ComponentFixture<DigitalisatQueryExportComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DigitalisatQueryExportComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(DigitalisatQueryExportComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
