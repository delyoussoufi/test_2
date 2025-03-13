import {Component, OnInit, TemplateRef} from '@angular/core';
import { HttpParams } from '@angular/common/http';

import {BsModalService} from 'ngx-bootstrap/modal';
import {BsModalRef} from 'ngx-bootstrap/modal/bs-modal-ref.service';

import {SearchBestandSearch} from '../../../model/model.search-bestand-search';
import {ConversionService} from '../../../services/conversion/conversion.service';
import {ToasterNotificationService} from '../../../services/notification/toaster-notification.service';
import {ComponentUtils} from '../../component.utils';
import {SearchBestand} from '../../../model/model.search-bestand';
import {SearchBestandService} from '../../../services/search-bestand/search-bestand.service';

@Component({
    selector: 'app-search-bestand-list',
    templateUrl: './search-bestand-list.component.html',
    styleUrls: ['./search-bestand-list.component.css'],
    standalone: false
})
export class SearchBestandListComponent extends ComponentUtils implements OnInit {

  private static BESTAND_PAUSED_STATUS = 'PAUSED';
  private static BESTAND_RUNNING_STATUS = 'RUNNING';


  deleteSearchBestand: SearchBestand;
  deleteModalRef: BsModalRef;
  searchParams: SearchBestandSearch = new SearchBestandSearch();
  searchBestaende: Array<SearchBestand>;
  isCollapsed = true;
  orderBy = '';
  orderDirection = 'DESC';
  page = 1;
  itemsPerPage = 10;
  totalItems = 0;

  constructor(private conversionService: ConversionService, private searchBestandService: SearchBestandService,
    private modalService: BsModalService, private toasterNotificationService: ToasterNotificationService) {
      super(toasterNotificationService);
  }

  get bestandPausedStatus(): string {
    return SearchBestandListComponent.BESTAND_PAUSED_STATUS;
  }

  get bestandRunningStatus(): string {
    return SearchBestandListComponent.BESTAND_RUNNING_STATUS;
  }

  ngOnInit() {
    this.search();
  }

  collapse() {
    this.isCollapsed = !this.isCollapsed;
  }

  onBestandPauseSwitchValueChange(status: boolean, bestand: SearchBestand) {
    this.searchBestandService.pauseBestand(bestand.id, !status).subscribe(
      changedPause => {
        if (!changedPause) {
          this.showErrorMessage('Cant pause this bestand now. Please try it later');
        }
        this.search();
      });
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
    this.orderDirection = 'DESC';
    this.searchParams = new SearchBestandSearch();
  }

  resetFiltersAndSearch() {
    this.resetFilters();
    this.search();
  }

  buildQueryParams(page, orderBy, pageSize?: number): HttpParams {
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

    if (this.searchParams.name) {
      params['name'] = this.searchParams.name;
    }

    if (this.searchParams.operator) {
      params['operator'] = this.searchParams.operator;
    }

    if (this.orderBy) {
      params['orderBy'] = this.orderBy;
    }
    if (this.orderDirection) {
      params['orderDirection'] = String(this.orderDirection);
    }
    params['firstResult'] = String((page - 1) * this.itemsPerPage);
    params['maxResults'] = pageSize ? pageSize : this.itemsPerPage;
    return new HttpParams({ fromObject: params });
  }

  search() {
    this.searchBestandService.search(this.buildQueryParams(this.page, null)).subscribe(
      data => {
        this.searchBestaende = data?.resultList;
        this.totalItems = data?.totalCount;
      }
    );
    this.isCollapsed = true;
  }

  sort(orderBy: string) {
    this.searchBestandService.search(this.buildQueryParams(1, orderBy)).subscribe(
      data => {
        this.searchBestaende = data.resultList;
        this.totalItems = data.totalCount;
        this.page = 1;
      },
      error => console.log(error)
    );
  }

  openDeleteModal(template: TemplateRef<any>, searchBestand: SearchBestand) {
    this.deleteModalRef = this.modalService.show(template);
    this.deleteSearchBestand = searchBestand;
  }

  closeDeleteModal() {
    this.deleteModalRef.hide();
    this.deleteModalRef = null;
  }

  deleteSearchBestandFromModal() {
    if (this.deleteSearchBestand) {
      this.searchBestandService.delete(this.deleteSearchBestand).subscribe(
        (data) => {
          if (data) {
            if (this.deleteSearchBestand) {
              const index = this.searchBestaende.indexOf(this.deleteSearchBestand);
              if (index > -1) {
                this.searchBestaende.splice(index, 1);
              }
            }
            this.deleteSearchBestand = null;
            this.toasterNotificationService.showSuccessMessage('Suchbestand gelöscht.');
          } else {
            this.toasterNotificationService.showErrorMessage('Suchbestand konnte nicht gelöscht werden.');
          }
        });
    }
    this.closeDeleteModal();
  }

}
