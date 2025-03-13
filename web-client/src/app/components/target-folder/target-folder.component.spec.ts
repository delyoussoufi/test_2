import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { TargetFolderComponent } from './target-folder.component';

describe('TargetFolderComponent', () => {
  let component: TargetFolderComponent;
  let fixture: ComponentFixture<TargetFolderComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ TargetFolderComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TargetFolderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
