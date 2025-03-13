import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import {Observable, of} from 'rxjs';
import { map } from 'rxjs/operators';

import {User} from '../../model/model.user';
import { ServerUrl } from '../../statics/server-url';
import {ProfileUser} from "../../model/model.profile-user";

@Injectable()
export class ProfileService {

  constructor(private http: HttpClient) {}

  public get(): Observable<User | null> {
    const currentUser: User = JSON.parse(localStorage.getItem('currentUser'));
    if (currentUser != null && currentUser.username != null) {
      return this.http.get<User>(ServerUrl.rootUrl + '/rest/profile?username=' + currentUser.username);
    }
    return of(null);
  }

  public update(user: ProfileUser): Observable<User> {
    return this.http.post<User>(ServerUrl.rootUrl + '/rest/profile/update', user);
  }

}
