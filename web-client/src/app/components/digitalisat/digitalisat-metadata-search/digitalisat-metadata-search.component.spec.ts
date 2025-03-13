import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DigitalisatMetadataSearchComponent } from './digitalisat-metadata-search.component';

describe('DigitalisatMetadataSearchComponent', () => {
  let component: DigitalisatMetadataSearchComponent;
  let fixture: ComponentFixture<DigitalisatMetadataSearchComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DigitalisatMetadataSearchComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DigitalisatMetadataSearchComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
