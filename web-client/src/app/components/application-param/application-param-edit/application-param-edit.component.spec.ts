import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { ApplicationParamEditComponent } from './application-param-edit.component';

describe('ApplicationParamEditComponent', () => {
  let component: ApplicationParamEditComponent;
  let fixture: ComponentFixture<ApplicationParamEditComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ ApplicationParamEditComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ApplicationParamEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
