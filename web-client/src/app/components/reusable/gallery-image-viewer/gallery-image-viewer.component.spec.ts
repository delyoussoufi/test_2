import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GalleryImageViewerComponent } from './gallery-image-viewer.component';

describe('GalleryImageViewerComponent', () => {
  let component: GalleryImageViewerComponent;
  let fixture: ComponentFixture<GalleryImageViewerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GalleryImageViewerComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GalleryImageViewerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
