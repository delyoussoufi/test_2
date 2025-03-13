import { TestBed, inject } from '@angular/core/testing';

import { SearchBestandService } from './search-bestand.service';

describe('SearchBestandService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [SearchBestandService]
    });
  });

  it('should be created', inject([SearchBestandService], (service: SearchBestandService) => {
    expect(service).toBeTruthy();
  }));
});
