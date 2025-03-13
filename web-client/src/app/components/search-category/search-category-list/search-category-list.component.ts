import { HttpParams } from '@angular/common/http';
import {Component, OnInit, TemplateRef} from '@angular/core';

import {BsModalService} from 'ngx-bootstrap/modal';
import {BsModalRef} from 'ngx-bootstrap/modal/bs-modal-ref.service';

import {SearchCategorySearch} from '../../../model/model.search-category-search';
import {ConversionService} from '../../../services/conversion/conversion.service';
import {ToasterNotificationService} from '../../../services/notification/toaster-notification.service';
import {SearchCategoryService} from '../../../services/search-category/search-category.service';
import {SearchCategory} from '../../../model/model.search-category';
import {SearchTerm} from '../../../model/model.search-term';
import {SearchCategoryComponent} from '../search-category.component';
import {SearchBlacklist} from '../../../model/model.search-blacklist';
import {
  DigitalisatQueryExportComponent
} from "../../digitalisat/digitalisat-query-export/digitalisat-query-export.component";

@Component({
    selector: 'app-search-category-list',
    templateUrl: './search-category-list.component.html',
    styleUrls: ['./search-category-list.component.css'],
    standalone: false
})
export class SearchCategoryListComponent extends SearchCategoryComponent implements OnInit {

  deleteSearchCategory: SearchCategory;
  deleteModalRef: BsModalRef;
  exportModalRef: BsModalRef;
  searchParams: SearchCategorySearch = new SearchCategorySearch();
  exportType;
  searchCategories: Array<SearchCategory>;
  isCollapsed = true;
  orderBy = '';
  orderDirection = 'ASC';
  page = 1;
  itemsPerPage = 10;
  totalItems = 0;

  constructor(private conversionService: ConversionService, private searchCategoryService: SearchCategoryService,
    private modalService: BsModalService, private toasterNotificationService: ToasterNotificationService) {
      super(modalService, toasterNotificationService);
  }

  ngOnInit() {
    this.search();
  }

  collapse() {
    this.isCollapsed = !this.isCollapsed;
  }

  pageChanged(event) {
    this.page = event.page;
    this.search();
  }

  itemsPerPageChanged(itemsPerPage) {
    this.itemsPerPage = itemsPerPage;
    this.page = 1;
    this.search();
  }

  resetFilters() {
    this.page = 1;
    this.itemsPerPage = 10;
    this.orderBy = '';
    this.orderDirection = 'ASC';
    this.searchParams = new SearchCategorySearch();
  }

  resetFiltersAndSearch() {
    this.resetFilters();
    this.search();
  }

  buildQueryParams(page, orderBy, pageSize?: number): HttpParams {
    this.searchParams.searchBy = 'name, description';
    this.searchParams.searchValue = [this.searchParams.name, this.searchParams.description];
    this.searchParams.orderBy = orderBy;
    this.searchParams.orderDesc = this.orderDirection === 'DESC';
    this.searchParams.perPage = pageSize ? pageSize : this.itemsPerPage;
    this.searchParams.page = page;
    const params = this.searchParams.toDict();
    return new HttpParams({ fromObject: params });
  }

  search() {
    this.searchCategoryService.search(this.buildQueryParams(this.page, 'order')).subscribe(
      data => {
        this.searchCategories = data.resultList;
        this.prepareSearchCategoriesForPresentation();
        this.totalItems = data.totalCount;
      },
      error => console.log(error)
    );
    this.isCollapsed = true;
  }

  sort(orderBy: string) {
    this.searchCategoryService.search(this.buildQueryParams(this.page, orderBy)).subscribe(
      data => {
        this.searchCategories = data.resultList;
        this.prepareSearchCategoriesForPresentation();
        this.totalItems = data.totalCount;
      },
      error => console.log(error)
    );
    this.orderDirection = this.orderDirection === 'DESC' ? 'ASC' : 'DESC';
  }

  prepareSearchCategoriesForPresentation() {
    this.searchCategories.forEach((searchCategory) => {
      this.prepareSearchTermsForPresentation(searchCategory);
    });
  }

  openExportModal(template: TemplateRef<any>) {
    this.exportModalRef = this.modalService.show(template);
  }

  closeExportModal() {
    this.exportModalRef.hide();
    this.exportModalRef = null;
  }

  exportSearchCategoriesFromModal() {
    if (this.exportType) {
      if (this.exportType === 'search') {
        const params = this.buildQueryParams(1, null, -1);
        this.searchCategoryService.exportSearchResultToExcel(params);
      } else if (this.exportType === 'all') {
        this.searchCategoryService.exportAllSearchCategoriesToExcel();
      }
    } else {
      this.showErrorMessage('Bitte einen Datenbereich auswählen.');
    }
    this.closeExportModal();
  }

  openDeleteModal(template: TemplateRef<any>, searchCategory: SearchCategory) {
    this.deleteModalRef = this.modalService.show(template);
    this.deleteSearchCategory = searchCategory;
  }

  closeDeleteModal() {
    this.deleteModalRef.hide();
    this.deleteModalRef = null;
  }

  deleteSearchCategoryFromModal() {
    if (this.deleteSearchCategory) {
      this.searchCategoryService.delete(this.deleteSearchCategory).subscribe(
        (data) => {
          if (data) {
            if (this.deleteSearchCategory) {
              const index = this.searchCategories.indexOf(this.deleteSearchCategory);
              if (index > -1) {
                this.searchCategories.splice(index, 1);
              }
            }
            this.deleteSearchCategory = null;
            this.toasterNotificationService.showSuccessMessage('Suchkategorie gelöscht.');
          } else {
            this.toasterNotificationService.showErrorMessage('Suchkategorie konnte nicht gelöscht werden.');
          }
        });
    }
    this.closeDeleteModal();
  }

  displaySearchValues(search: Array<SearchTerm> | Array<SearchBlacklist>, limit= 10) {
    let returnString = '';
    const size = search.length;
    if (search && size > 0) {
      const searchTermValues: Array<string> = search.slice(0, limit).map(
        (t) => t.hasOwnProperty('visualSearchValue') ? t.visualSearchValue : t.value);
      returnString = searchTermValues.join(', ');
      if (size > limit) {
        returnString += ' ...';
      }
    }
    return returnString;
  }

  reorderSearchCategories() {
    this.searchCategories.map((sc, idx) => sc.order = idx + 1);
    this.searchCategoryService.reorder(this.searchCategories).subscribe();
  }

  exportCategoryResults(exportQueryRef: DigitalisatQueryExportComponent, categoryId: string){
    exportQueryRef.fetchFileService$ = this.searchCategoryService.exportClassificationResults(categoryId);
    exportQueryRef.openModal();
  }

}
