import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { ServerUrl } from '../../statics/server-url';
import { User } from '../../model/model.user';
import {Role} from '../../model/model.role';
import {Right} from '../../model/model.right';

@Injectable()
export class UserService {

  constructor(private http: HttpClient) { }

  search(params: HttpParams): Observable<any> {
    return this.http.get(ServerUrl.rootUrl + '/rest/users/search', {params});
  }

  get(id: string): Observable<User> {
    return this.http.get<User>(ServerUrl.rootUrl + '/rest/users/' + id);
  }

  getRoles(): Observable<Role[]> {
    return this.http.get<Role[]>(ServerUrl.rootUrl + '/rest/users/roles');
  }

  getRights(): Observable<Right[]> {
    return this.http.get<Right[]>(ServerUrl.rootUrl + '/rest/users/rights');
  }

  getRightsByRole(roleId: string): Observable<string[]> {
    return this.http.get<string[]>(ServerUrl.rootUrl + '/rest/users/rightsByRole/' + roleId);
  }

  create(user: User): Observable<User> {
    return this.http.post<User>(ServerUrl.rootUrl + '/rest/users/create', user);
  }

  update(user: User): Observable<User> {
    return this.http.put<User>(ServerUrl.rootUrl + '/rest/users', user);
  }

  delete(user: User): Observable<any> {
    return this.http.delete(ServerUrl.rootUrl + '/rest/users/' + user.userId);
  }
}
