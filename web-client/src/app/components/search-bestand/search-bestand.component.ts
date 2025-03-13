import {Component, OnInit, TemplateRef} from '@angular/core';


import { ToasterNotificationService } from './../../services/notification/toaster-notification.service';
import { SearchCategory } from './../../model/model.search-category';
import {ComponentUtils} from '../component.utils';
import {BsModalRef} from 'ngx-bootstrap/modal/bs-modal-ref.service';
import {SearchTerm} from '../../model/model.search-term';
import {BsModalService} from 'ngx-bootstrap/modal';

export class SearchBestandComponent extends ComponentUtils {

  addSearchTermError = '';
  addSearchTermModalRef: BsModalRef;
  addSearchTerm: SearchTerm = new SearchTerm();
  searchCategory: SearchCategory = new SearchCategory();

  constructor(private _modalService: BsModalService,
    private _toasterNotificationService: ToasterNotificationService) {
    super(_toasterNotificationService);
  }

  openAddSearchTermModal(template: TemplateRef<any>) {
    this.addSearchTermModalRef = this._modalService.show(template);
    this.addSearchTerm.categoryId = this.searchCategory.id;
  }

  closeAddSearchTermModal() {
    this.addSearchTermModalRef.hide();
    this.addSearchTermModalRef = null;
    this.resetAddSearchTermModal();
  }

  private resetAddSearchTermModal() {
    this.addSearchTermError = '';
    this.addSearchTerm = new SearchTerm();
  }

  addSearchTermFromModal() {
    if (this.addSearchTerm.searchValue) {
      for (const searchTerm of this.searchCategory.searchTerms) {
        if (searchTerm.searchValue === this.addSearchTerm.searchValue) {
          this.addSearchTermError = 'Diesen Suchbegriff haben Sie bereits hinzugefügt.';
          return;
        }
      }
    }
    this.searchCategory.searchTerms.push(this.addSearchTerm);
    this.closeAddSearchTermModal();
  }

  deleteSearchTerm(searchTerm: SearchTerm) {
    const index = this.searchCategory.searchTerms.indexOf(searchTerm);
    if (index > -1) {
      this.searchCategory.searchTerms.splice(index, 1);
    }
  }

}
