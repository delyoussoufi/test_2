import { TestBed, inject } from '@angular/core/testing';

import { ApplicationParamService } from './application-param.service';

describe('ApplicationParamService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ApplicationParamService]
    });
  });

  it('should be created', inject([ApplicationParamService], (service: ApplicationParamService) => {
    expect(service).toBeTruthy();
  }));
});
