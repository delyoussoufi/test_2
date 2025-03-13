import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { Observable } from 'rxjs';

import { ServerUrl } from '../../statics/server-url';

@Injectable()
export class ExceptionService {

  constructor(private http: HttpClient) {}

  get(id: string): Observable<any> {
    return this.http.get(ServerUrl.rootUrl + '/rest/admin/exceptions/' + id);
  }

  search(params: HttpParams): Observable<any> {
    return this.http.get(ServerUrl.rootUrl + '/rest/admin/exceptions/search', {params});
  }
}
