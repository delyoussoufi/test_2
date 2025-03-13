import { TestBed, inject } from '@angular/core/testing';

import { DigiConnectionService } from './digi-connection.service';

describe('DigiConnectionService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [DigiConnectionService]
    });
  });

  it('should be created', inject([DigiConnectionService], (service: DigiConnectionService) => {
    expect(service).toBeTruthy();
  }));
});
