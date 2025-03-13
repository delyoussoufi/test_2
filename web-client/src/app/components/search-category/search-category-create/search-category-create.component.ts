import {Component, OnInit} from '@angular/core';

import {BsModalService} from 'ngx-bootstrap/modal';

import {ConversionService} from '../../../services/conversion/conversion.service';
import {ToasterNotificationService} from '../../../services/notification/toaster-notification.service';
import {SearchCategory} from '../../../model/model.search-category';
import {SearchCategoryService} from '../../../services/search-category/search-category.service';
import {SearchTerm} from '../../../model/model.search-term';
import {SearchCategoryComponent} from '../search-category.component';

@Component({
    selector: 'app-search-category-create',
    templateUrl: './search-category-create.component.html',
    styleUrls: ['./search-category-create.component.css'],
    standalone: false
})
export class SearchCategoryCreateComponent extends SearchCategoryComponent implements OnInit {

  constructor(private conversionService: ConversionService, private searchCategoryService: SearchCategoryService,
    private modalService: BsModalService, private toasterNotificationService: ToasterNotificationService) {
    super(modalService, toasterNotificationService);
  }

  ngOnInit() {
    if (!this.searchCategory.searchTerms) {
      this.searchCategory.searchTerms = new Array<SearchTerm>();
    }
  }

  createSearchCategory() {
    this.searchCategoryService.create(this.searchCategory).subscribe(
      data => {
        this.searchCategory = new SearchCategory();
        super.showSuccessMessage('Suchkategorie wurde erstellt.');
      },
      error => {
        if (error.error && error.error.message) {
          super.showErrorMessage(error.error.message);
        } else {
          super.showErrorMessage('Suchkategorie konnte nicht erstellt werden.');
        }
        console.log(error);
      }
    );
  }

}
