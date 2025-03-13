import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MetadataCommentsViewComponent } from './metadata-comments-view.component';

describe('MetadataCommentsViewComponent', () => {
  let component: MetadataCommentsViewComponent;
  let fixture: ComponentFixture<MetadataCommentsViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MetadataCommentsViewComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MetadataCommentsViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
