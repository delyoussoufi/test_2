import { TestBed, inject } from '@angular/core/testing';

import { SearchCategoryService } from './search-category.service';

describe('SearchCategoryService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [SearchCategoryService]
    });
  });

  it('should be created', inject([SearchCategoryService], (service: SearchCategoryService) => {
    expect(service).toBeTruthy();
  }));
});
