import {Injectable} from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import {Observable} from 'rxjs';

import {Vorgang} from '../../model/model.vorgang';
import {ServerUrl} from '../../statics/server-url';
import {DigitalisatImage} from '../../model/model.digitalisat-image';
import {VorgangCreate} from '../../model/model.vorgang-create';
import {SearchResult} from '../../model/model.search-result';

@Injectable()
export class VorgangService {

  constructor(private http: HttpClient) { }

  get(id: string): Observable<Vorgang> {
    return this.http.get<Vorgang>(ServerUrl.rootUrl + '/rest/vorgaenge/' + id);
  }

  search(params: HttpParams): Observable<SearchResult<Vorgang>> {
    return this.http.get<SearchResult<Vorgang>>(ServerUrl.rootUrl + '/rest/vorgaenge/search', { params });
  }

  create(category_id: string, digitalisat_id: string, images: Array<DigitalisatImage>): Observable<any> {
    const body = new VorgangCreate();
    body.category_id = category_id;
    body.digitalisat_id = digitalisat_id;
    body.images_ids = images.map((i) => i.id);
    return this.http.post(ServerUrl.rootUrl + '/rest/vorgaenge/create', body);
  }

  delete(vorgang: Vorgang): Observable<boolean> {
    return this.http.delete<boolean>(ServerUrl.rootUrl + '/rest/vorgaenge/delete/' + vorgang.id);
  }

  getImages(vorgangId: string): Observable<Array<DigitalisatImage>> {
    return this.http.get<Array<DigitalisatImage>>(ServerUrl.rootUrl + '/rest/vorgaenge/vorgangImagesId/' + vorgangId);
  }

  downloadPdf(vorgang: Vorgang): Observable<Blob> {
    return this.http.get(ServerUrl.rootUrl + '/rest/vorgaenge/pdf/' + vorgang.id, {responseType: 'blob'});
  }
}
