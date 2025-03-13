import {TemplateRef} from '@angular/core';

import {BsModalRef} from 'ngx-bootstrap/modal/bs-modal-ref.service';
import {BsModalService} from 'ngx-bootstrap/modal';

import { ToasterNotificationService } from '../../services/notification/toaster-notification.service';
import { SearchCategory } from '../../model/model.search-category';
import {ComponentUtils} from '../component.utils';
import {SearchTerm} from '../../model/model.search-term';
import {SearchTermOperator} from '../../model/model.search-term-operator';
import {SearchBlacklist} from '../../model/model.search-blacklist';
import {SearchIgnoreList} from '../../model/model.search-ignore-list';

export class SearchCategoryComponent extends ComponentUtils {

  addSearchTermError = '';
  modalRef: BsModalRef;
  addSearchTermModalRef: BsModalRef;
  addValueToSearchFromModalRef: BsModalRef;
  addSearchTerms: Array<String> = new Array<String>();
  searchCategory: SearchCategory = new SearchCategory();
  selectedSearchTermOperator: string;
  searchTermOperators: Array<SearchTermOperator> = new Array<SearchTermOperator>();
  andPageName = '#AND_PAGE#';
  andAllName = '#AND_ALL#';
  modalValue = '';

  constructor(private _modalService: BsModalService,
    private _toasterNotificationService: ToasterNotificationService) {
    super(_toasterNotificationService);
    this.searchTermOperators.push(new SearchTermOperator(this.andPageName, 'Und auf einer Seite'));
    this.searchTermOperators.push(new SearchTermOperator(this.andAllName, 'Und auf allen Seiten'));
  }

  // addSearchTermValue() {
  //   this.addSearchTerms.push('');
  // }

  openModal(template: TemplateRef<any>) {
    this.modalRef = this._modalService.show(template);
  }

  closeModal() {
    this.modalRef?.hide();
    this.modalRef = null;
  }

  openAddSearchTermModal(template: TemplateRef<any>) {
    this.addSearchTermModalRef = this._modalService.show(template);
    this.addSearchTerms.push('');
  }

  openAddValueToSearchFromModal(template: TemplateRef<any>) {
    this.addValueToSearchFromModalRef = this._modalService.show(template);
  }

  addBlackListValueFromModal() {
    const value = this.modalValue?.trim();
    if (value) {
      const addSearchBlacklist = new SearchBlacklist();
      addSearchBlacklist.categoryId = this.searchCategory.id;
      addSearchBlacklist.value = value;
      const v = this.searchCategory.blacklist.filter(e => e.value === value);
      if (v.length === 0) {
        this.searchCategory.blacklist.push(addSearchBlacklist);
      }
    }
    this.closeAddValueToSearchFromModal();
  }

  addIgnoreListValueFromModal() {
    const value = this.modalValue?.trim();
    if (value) {
      const addSearchIgnoreList = new SearchIgnoreList();
      addSearchIgnoreList.categoryId = this.searchCategory.id;
      addSearchIgnoreList.value = value;
      const v = this.searchCategory.ignoreList.filter(e => e.value === value);
      if (v.length === 0) {
        this.searchCategory.ignoreList.push(addSearchIgnoreList);
      }
    }
    this.closeAddValueToSearchFromModal();
  }

  closeAddSearchTermModal() {
    this.addSearchTermModalRef.hide();
    this.addSearchTermModalRef = null;
    this.resetAddSearchTermModal();
  }

  closeAddValueToSearchFromModal() {
    this.addValueToSearchFromModalRef?.hide();
    this.addValueToSearchFromModalRef = null;
    this.modalValue = '';
  }

  private resetAddSearchTermModal() {
    this.addSearchTermError = '';
    this.addSearchTerms = new Array<String>();
    this.selectedSearchTermOperator = null;
  }

  trackByFn(index, item) {
    return index;
  }

  onChangeSearchTermOperator(selectedSearchTermOperator: string) {
    if (selectedSearchTermOperator) {
      this.selectedSearchTermOperator = selectedSearchTermOperator;
    } else {
      this.selectedSearchTermOperator = null;
    }
  }

  addSearchTermFromModal() {
    for (const searchTerm of this.addSearchTerms) {
      if (searchTerm === '') {
        this.addSearchTermError = 'Bitte für alle Suchbegriffe einen Wert festlegen.';
        return;
      }
    }
    if (this.addSearchTerms.length > 1 && !this.selectedSearchTermOperator) {
      this.addSearchTermError = 'Bitte einen Suchoperator festlegen.';
      return;
    }
    const addSearchTerm = new SearchTerm();
    addSearchTerm.searchValue = '';
    if (this.addSearchTerms) {
      addSearchTerm.categoryId = this.searchCategory.id;
      this.addSearchTerms.forEach((searchTermValue, index) => {
        addSearchTerm.searchValue += searchTermValue;
        if (index + 1 < this.addSearchTerms.length) {
          addSearchTerm.searchValue += this.selectedSearchTermOperator;
        }
      });
      for (const searchTerm of this.searchCategory.searchTerms) {
        if (searchTerm.searchValue === addSearchTerm.searchValue) {
          this.addSearchTermError = 'Diesen Suchbegriff haben Sie bereits hinzugefügt.';
          return;
        }
      }
    }
    this.searchCategory.searchTerms.push(addSearchTerm);
    this.prepareSearchTermsForPresentation(this.searchCategory);
    this.closeAddSearchTermModal();
  }

  prepareSearchTermsForPresentation(searchCategory: SearchCategory) {
    for (const searchTerm of searchCategory.searchTerms) {
      searchTerm.visualSearchValue = '';
      if (searchTerm.searchValue.indexOf(this.andPageName) >= 0) {
        this.prepareSearchTermOperator(searchTerm, this.andPageName);
      }
      if (searchTerm.searchValue.indexOf(this.andAllName) >= 0) {
        this.prepareSearchTermOperator(searchTerm, this.andAllName);
      }
      if (searchTerm.visualSearchValue === '') {
        searchTerm.visualSearchValue = searchTerm.searchValue;
      }
    }
  }

  private prepareSearchTermOperator(searchTerm: SearchTerm, operatorName: string) {
    const parts = searchTerm.searchValue.split(operatorName);
    parts.forEach((part, index) => {
      searchTerm.visualSearchValue += part;
      if (index + 1 < parts.length) {
        if (operatorName === this.andPageName) {
          searchTerm.visualSearchValue += '&nbsp;<span class="badge badge-primary">UND</span>&nbsp;';
        } else if (operatorName === this.andAllName) {
          searchTerm.visualSearchValue += '&nbsp;<span class="badge badge-success">UND</span>&nbsp;';
        }
      }
    });
  }

  deleteSearchTerm(searchTerm: SearchTerm) {
    this.removeItemFromList(this.searchCategory.searchTerms, searchTerm);
  }

  deleteBlacklistTerm(value: SearchBlacklist) {
    this.removeItemFromList(this.searchCategory.blacklist, value);
  }

  deleteIgnoreListTerm(value: SearchIgnoreList) {
    this.removeItemFromList(this.searchCategory.ignoreList, value);
  }

}
