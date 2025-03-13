import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { VorgangListComponent } from './vorgang-list.component';

describe('VorgangListComponent', () => {
  let component: VorgangListComponent;
  let fixture: ComponentFixture<VorgangListComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ VorgangListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(VorgangListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
