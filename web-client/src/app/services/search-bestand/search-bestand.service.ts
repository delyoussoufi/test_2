import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { ServerUrl } from '../../statics/server-url';
import {SearchBestand} from '../../model/model.search-bestand';

@Injectable()
export class SearchBestandService {

  constructor(private http: HttpClient) { }

  get(id: string): Observable<SearchBestand> {
    return this.http.get<SearchBestand>(ServerUrl.rootUrl + '/rest/admin/searchBestaende/' + id);
  }

  create(searchBestand: SearchBestand): Observable<any> {
    return this.http.post(ServerUrl.rootUrl + '/rest/admin/searchBestaende', searchBestand).pipe(
      map((response: Response) => {
        return response;
      }));
  }

  delete(searchBestand: SearchBestand): Observable<any> {
    return this.http.delete(ServerUrl.rootUrl + '/rest/admin/searchBestaende/' + searchBestand.id);
  }

  search(params: HttpParams): Observable<any> {
    return this.http.get(ServerUrl.rootUrl + '/rest/admin/searchBestaende/search', { params });
  }

  pauseBestand(bestand_id: string, pause: boolean): Observable<boolean> {
    return this.http.post<boolean>(ServerUrl.rootUrl + '/rest/admin/searchBestaende/pauseBestand',
      {search_bestand_id: bestand_id, pause: pause});
  }

}
