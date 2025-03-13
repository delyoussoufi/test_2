import { TestBed, inject } from '@angular/core/testing';

import { VorgangService } from './vorgang.service';

describe('VorgangService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [VorgangService]
    });
  });

  it('should be created', inject([VorgangService], (service: VorgangService) => {
    expect(service).toBeTruthy();
  }));
});
