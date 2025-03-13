import { TestBed, inject } from '@angular/core/testing';

import { DigitalisatService } from './digitalisat.service';

describe('DigitalisatService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [DigitalisatService]
    });
  });

  it('should be created', inject([DigitalisatService], (service: DigitalisatService) => {
    expect(service).toBeTruthy();
  }));
});
