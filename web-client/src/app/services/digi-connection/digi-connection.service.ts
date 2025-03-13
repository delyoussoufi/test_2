import {Injectable} from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import {Observable} from 'rxjs';

import {ServerUrl} from '../../statics/server-url';

@Injectable()
export class DigiConnectionService {

  constructor(private http: HttpClient) { }

  searchBestaende(params: HttpParams): Observable<any> {
    return this.http.get<any>(ServerUrl.rootUrl + '/rest/digi/bestand/search', { params });
  }

}
