import { Component, OnInit } from '@angular/core';
import { HttpParams } from '@angular/common/http';

import { ConversionService } from './../../../services/conversion/conversion.service';
import { ComponentUtils } from './../../component.utils';
import { ExceptionSearch } from './../../../model/model.exception-search';
import { ExceptionService } from './../../../services/exception/exception.service';
import { ToasterNotificationService } from './../../../services/notification/toaster-notification.service';

@Component({
    selector: 'app-exception-list',
    templateUrl: './exception-list.component.html',
    styleUrls: ['./exception-list.component.css'],
    standalone: false
})
export class ExceptionListComponent extends ComponentUtils implements OnInit {

  searchResult: ExceptionSearch = new ExceptionSearch();
  exceptionLogs: Array<any>;
  isCollapsed = true;
  orderBy = '';
  orderDirection = 'DESC';
  page = 1;
  itemsPerPage = 10;
  totalItems = 0;

  constructor(private exceptionService: ExceptionService, private conversionService: ConversionService,
    private toasterNotificationService: ToasterNotificationService) {
    super(toasterNotificationService);
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
    this.searchResult = new ExceptionSearch();
  }

  resetFiltersAndSearch() {
    this.resetFilters();
    this.search();
  }

  buildQueryParams(page, orderBy): HttpParams {
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
    if (this.searchResult.stacktrace) {
      params['stacktrace'] = this.searchResult.stacktrace;
    }
    if (this.searchResult.hash) {
      params['hash'] = String(this.searchResult.hash);
    }
    if (this.searchResult.von) {
      params['dateVon'] = this.conversionService.convertDateToGermanDateString(this.searchResult.von);
    }
    if (this.searchResult.bis) {
      params['dateBis'] = this.conversionService.convertDateToGermanDateString(this.searchResult.bis);
    }
    if (this.orderBy) {
      params['orderBy'] = String(this.orderBy);
    }
    if (this.orderDirection) {
      params['orderDirection'] = String(this.orderDirection);
    }
    params['firstResult'] = String((page - 1) * this.itemsPerPage);
    params['maxResults'] = this.itemsPerPage;
    return new HttpParams({ fromObject: params });
  }

  search() {
    this.exceptionService.search(this.buildQueryParams(this.page, null)).subscribe(
      data => {
        this.exceptionLogs = data.resultList;
        this.totalItems = data.totalCount;
      },
      error => console.log(error)
    );
    this.isCollapsed = true;
  }

}
