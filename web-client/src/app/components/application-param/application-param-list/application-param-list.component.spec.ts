import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { ApplicationParamListComponent } from './application-param-list.component';

describe('ApplicationParamEditComponent', () => {
  let component: ApplicationParamListComponent;
  let fixture: ComponentFixture<ApplicationParamListComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ ApplicationParamListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ApplicationParamListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
