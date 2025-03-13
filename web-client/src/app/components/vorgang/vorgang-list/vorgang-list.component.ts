import {Component, OnInit, TemplateRef} from '@angular/core';
import { HttpParams } from '@angular/common/http';
import {BsModalService} from 'ngx-bootstrap/modal';
import {BsModalRef} from 'ngx-bootstrap/modal/bs-modal-ref.service';
import {ToasterNotificationService} from '../../../services/notification/toaster-notification.service';
import {Vorgang} from '../../../model/model.vorgang';
import {VorgangSearch} from '../../../model/model.vorgang-search';
import {VorgangService} from '../../../services/vorgang/vorgang.service';
import {ComponentUtils} from '../../component.utils';
import {SearchCategory} from '../../../model/model.search-category';
import {SearchCategoryService} from '../../../services/search-category/search-category.service';
import {Observable} from "rxjs";

@Component({
    selector: 'app-vorgang-list',
    templateUrl: './vorgang-list.component.html',
    styleUrls: ['./vorgang-list.component.css'],
    standalone: false
})
export class VorgangListComponent extends ComponentUtils implements OnInit {

  selectedSearchCategory: SearchCategory = null;
  searchCategories$: Observable<SearchCategory[]>;
  vorgaenge: Vorgang[];

  // TODO old parameters clean it.
  deleteVorgang: Vorgang;
  deleteModalRef: BsModalRef;
  searchParams: VorgangSearch = new VorgangSearch();
  // sessionSearchParams: VorgangSessionSearch = new VorgangSessionSearch();
  isCollapsed = true;
  orderBy = "vorgang_order";
  orderDirection = 'DESC';
  page = 1;
  itemsPerPage = 10;
  totalItems = 0;


  constructor(private vorgangService: VorgangService,
              private searchCategoryService: SearchCategoryService,
              private modalService: BsModalService, private toasterNotificationService: ToasterNotificationService) {
      super(toasterNotificationService);
      this.fetchAllSearchCategories();
  }

  ngOnInit() {
    this.search();
  }

  fetchAllSearchCategories() {
    this.searchCategories$ = this.searchCategoryService.all();
  }

  onChangeSearchCategory(selectedSearchCategory: SearchCategory) {
    if (selectedSearchCategory) {
      this.selectedSearchCategory = selectedSearchCategory;
    } else {
      this.selectedSearchCategory = null;
    }
    this.search();
  }

  pageChanged(event: any) {
    console.log();
    this.page = event.page;
    this.search();
  }

  itemsPerPageChanged(itemsPerPage: number) {
    this.itemsPerPage = itemsPerPage;
    this.page = 1;
    this.search();
  }

  buildQueryParams(page: number, orderBy: string, pageSize?: number): HttpParams {
    if (this.orderBy && this.orderBy === orderBy) {
      if (this.orderDirection) {
        this.orderDirection = this.orderDirection === 'DESC' ? 'ASC' : 'DESC';
      }
    }
    if (orderBy) {
      this.orderBy = orderBy;
    }
    if (!this.orderDirection) {
      this.orderDirection = 'DESC';
    }
    const params = {};

    this.searchParams.searchCategoryId = this.selectedSearchCategory?.id;
    if (this.searchParams.searchCategoryId) {
      params['searchCategoryId'] = this.searchParams.searchCategoryId;
    }
    if (this.orderBy) {
      params['orderBy'] = this.orderBy;
    }
    if (this.orderDirection) {
      params['orderDirection'] = String(this.orderDirection);
    }
    params['page'] = page;
    params['perPage'] = pageSize ? pageSize : this.itemsPerPage;
    // localStorage.setItem(this.sessionSearchParamsKey, JSON.stringify(this.sessionSearchParams));
    return new HttpParams({ fromObject: params });
  }

  search(orderBy = null) {
    this.vorgangService.search(this.buildQueryParams(this.page, orderBy)).subscribe({
      next: data => {
      this.vorgaenge = data.resultList;
      this.totalItems = data.totalCount;
      // this.sessionSearchParams.totalItems = this.totalItems;
      // localStorage.setItem(this.sessionSearchParamsKey, JSON.stringify(this.sessionSearchParams));
    },
      error: error => console.log(error)
    });
    this.isCollapsed = true;
  }

  openDeleteModal(template: TemplateRef<any>, vorgang: Vorgang) {
    this.deleteModalRef = this.modalService.show(template);
    this.deleteVorgang = vorgang;
  }

  closeDeleteModal() {
    this.deleteModalRef.hide();
    this.deleteModalRef = null;
  }

  deleteVorgangFromModal() {

    if (this.deleteVorgang) {
      this.vorgangService.delete(this.deleteVorgang).subscribe({
        next: wasDeleted => {
          if (wasDeleted) {
            this.toasterNotificationService.showSuccessMessage('Vorgang ' + this.deleteVorgang.name + 'wurde gelöscht');
            this.removeItemFromList(this.vorgaenge, this.deleteVorgang);
            this.deleteVorgang = null;
          } else {
            this.toasterNotificationService.showErrorMessage(this.deleteVorgang.name + ' konnte nicht gelöscht werden');
          }
          this.closeDeleteModal();
        },
        error: error => {
          console.log(error);
          this.closeDeleteModal();
        }
      });
    }
  }

}
