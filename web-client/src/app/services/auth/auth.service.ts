import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { map } from 'rxjs/operators';
import { Observable } from 'rxjs';

import { ServerUrl } from '../../statics/server-url';
import { User } from '../../model/model.user';

@Injectable()
export class AuthService {

  constructor(private http: HttpClient, private router: Router) { }

  public logIn(user: User): Observable<User> {

    // creating base64 encoded String from username and password
    // const base64Credential: string = btoa(user.username + ':' + user.password);

    const httpOptions = {
      headers: new HttpHeaders({
        'Accept': 'application/json',
        /*'Authorization':  'Basic ' + base64Credential,*/
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
      })
    };

    const body = 'username=' + encodeURIComponent(user.username) + '&password=' + encodeURIComponent(user.password);

    return this.http.post<User>(ServerUrl.rootUrl + '/rest/authentication/authenticateUser', body, httpOptions).pipe(
      map((user) => {
        // login successful if there's a jwt token in the response
        if (user) {
          // store user details  in local storage to keep user logged in between page refreshes
          localStorage.setItem('currentUser', JSON.stringify(user));
        }
        return user;
      }));
  }

  public hasToken(userTokenn: String, userId: String): Observable<boolean> {
    return this.http.get<boolean>(ServerUrl.rootUrl + '/rest/authentication/hasToken?userToken=' + userTokenn
        + '&userId=' + userId);
  }

  public logOut() {
    localStorage.removeItem('currentUser');
    this.router.navigate(['/home']).then();
  }
}
