import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OrderBySelectorComponent } from './order-by-selector.component';

describe('OrderBySelectorComponent', () => {
  let component: OrderBySelectorComponent;
  let fixture: ComponentFixture<OrderBySelectorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OrderBySelectorComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(OrderBySelectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
