import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OcrImageViewerComponent } from './ocr-image-viewer.component';

describe('OcrImageViewerComponent', () => {
  let component: OcrImageViewerComponent;
  let fixture: ComponentFixture<OcrImageViewerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OcrImageViewerComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(OcrImageViewerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
