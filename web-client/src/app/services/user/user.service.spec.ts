import { TestBed, inject } from '@angular/core/testing';

import { UserService } from './user.service';

describe('BeerService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [UserService]
    });
  });

  it('should be created', inject([UserService], (service: UserService) => {
    expect(service).toBeTruthy();
  }));
});
