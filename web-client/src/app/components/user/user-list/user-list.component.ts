import { Component, OnInit, TemplateRef } from '@angular/core';
import { HttpParams } from '@angular/common/http';

import { BsModalService } from 'ngx-bootstrap/modal';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';

import { ComponentUtils } from '../../component.utils';
import { ToasterNotificationService } from '../../../services/notification/toaster-notification.service';
import { User } from '../../../model/model.user';
import { UserSearch } from '../../../model/model.user-search';
import { UserService } from '../../../services/user/user.service';

@Component({
    selector: 'app-user-list',
    templateUrl: './user-list.component.html',
    styleUrls: ['./user-list.component.css'],
    providers: [UserService],
    standalone: false
})
export class UserListComponent extends ComponentUtils implements OnInit {

  deleteUser: User;
  deleteModalRef: BsModalRef;
  searchParams: UserSearch = new UserSearch();
  users: User[];
  isCollapsed = true;
  orderBy = '';
  orderDirection = 'DESC';
  page = 1;
  itemsPerPage = 10;
  totalItems = 0;

  constructor(private userService: UserService, private modalService: BsModalService,
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
    this.searchParams = new UserSearch();
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
    if (this.searchParams.username) {
      params['username'] = this.searchParams.username;
    }
    if (this.searchParams.forename) {
      params['forename'] = this.searchParams.forename;
    }
    if (this.searchParams.surname) {
      params['surname'] = this.searchParams.surname;
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
    params['maxResults'] = this.itemsPerPage;
    return new HttpParams({ fromObject: params });
  }

  search() {
    this.userService.search(this.buildQueryParams(this.page, null)).subscribe(
      data => {
        this.users = data.resultList;
        this.totalItems = data.totalCount;
      },
      error => console.log(error)
    );
    this.isCollapsed = true;
  }

  openDeleteModal(template: TemplateRef<any>, user: User) {
    this.deleteModalRef = this.modalService.show(template);
    this.deleteUser = user;
  }

  closeDeleteModal() {
    this.deleteModalRef.hide();
    this.deleteModalRef = null;
  }

  deleteUserFromModal() {
    if (this.deleteUser) {
      this.userService.delete(this.deleteUser).subscribe(
        () =>  {
          if (this.deleteUser) {
            const index = this.users.indexOf(this.deleteUser);
            if (index > -1) {
              this.users.splice(index, 1);
            }
          }
          this.deleteUser = null;
          this.toasterNotificationService.showSuccessMessage('Nutzer gelöscht.');
      });
    }
    this.closeDeleteModal();
  }
}
