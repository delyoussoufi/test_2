import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SelectableImageComponent } from './selectable-image.component';

describe('SelectableImageComponent', () => {
  let component: SelectableImageComponent;
  let fixture: ComponentFixture<SelectableImageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SelectableImageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SelectableImageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
