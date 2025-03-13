import {Injectable} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Observable} from 'rxjs';
import {ServerUrl} from '../../statics/server-url';


@Injectable()
export class ReportingService {

  constructor(private http: HttpClient) {
  }

  // printBestellzettel(data: Order[]): Observable<Blob> {
  //   return this.http.post(ServerUrl.rootUrl + '/rest/report/bestellzettel', data, {responseType: 'blob'});
  // }

}
