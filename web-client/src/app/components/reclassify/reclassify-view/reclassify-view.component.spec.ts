import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReclassifyViewComponent } from './reclassify-view.component';

describe('ReclassifyViewComponent', () => {
  let component: ReclassifyViewComponent;
  let fixture: ComponentFixture<ReclassifyViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ReclassifyViewComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ReclassifyViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
