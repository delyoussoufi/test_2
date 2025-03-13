import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import {BsModalService} from 'ngx-bootstrap/modal';

import { ConversionService } from '../../../services/conversion/conversion.service';
import { ToasterNotificationService } from '../../../services/notification/toaster-notification.service';
import { SearchCategoryService } from '../../../services/search-category/search-category.service';
import {SearchCategoryComponent} from '../search-category.component';

@Component({
    selector: 'app-search-category-edit',
    templateUrl: './search-category-edit.component.html',
    styleUrls: ['./search-category-edit.component.css'],
    standalone: false
})
export class SearchCategoryEditComponent extends SearchCategoryComponent implements OnInit {

  constructor(private conversionService: ConversionService, private modalService: BsModalService,
    private toasterNotificationService: ToasterNotificationService,
    private route: ActivatedRoute, private searchCategoryService: SearchCategoryService) {
      super(modalService, toasterNotificationService);
      this.route.params.subscribe(params => {
        if (params && params.id) {
          this.searchCategoryService.get(params.id).subscribe(
            data => {
              this.searchCategory = data;
              this.prepareSearchTermsForPresentation(this.searchCategory);
            }
          );
        }
      });
  }

  ngOnInit() {
  }

  updateSearchCategory() {
    this.searchCategoryService.update(this.searchCategory).subscribe(
      data => {
          super.showSuccessMessage('Suchkategorie wurde geändert.');
        },
        error => {
          super.showErrorMessage('Suchkategorie konnte nicht geändert werden.');
          console.log(error);
        }
      );
  }

}
