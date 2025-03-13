import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { VorgangViewComponent } from './vorgang-view.component';

describe('VorgangViewComponent', () => {
  let component: VorgangViewComponent;
  let fixture: ComponentFixture<VorgangViewComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ VorgangViewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(VorgangViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
