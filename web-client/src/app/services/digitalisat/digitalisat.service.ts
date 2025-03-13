import {Injectable} from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';

import {Digitalisat} from '../../model/model.digitalisat';
import {ServerUrl} from '../../statics/server-url';
import {SearchResult} from '../../model/model.search-result';
import {UserDigitalisatComment} from '../../model/model.user-digitalisat-comment';
import {DigitalisatImage} from '../../model/model.digitalisat-image';
import {OcrData, SearchTermsFound} from '../../model/model.ocr-data';
import {EnumClassificationStatus} from '../../enums/enum.digitalisat-working-status';
import {DigitalisatInfo} from '../../model/model.digitalisat-info';
import {FoundEntities} from '../../model/model.found-entities';

@Injectable()
export class DigitalisatService {

  constructor(private http: HttpClient) { }

  get(id: string): Observable<Digitalisat> {
    return this.http.get<Digitalisat>(ServerUrl.rootUrl + '/rest/digitalisate/' + id);
  }

  totalOpenDigitalisateInCategory(categoryId: string = ''): Observable<number> {
    return this.http.get<number>(ServerUrl.rootUrl + '/rest/digitalisate/totalOpenDigitalisateInCategory/' + categoryId);
  }

  update(digitalisat: Digitalisat): Observable<any> {
    return this.http.put(ServerUrl.rootUrl + '/rest/digitalisate', digitalisat).pipe(
      map((response: Response) => {
        return response;
      }));
  }

  search(params: HttpParams): Observable<SearchResult<Digitalisat>> {
    return this.http.get<SearchResult<Digitalisat>>(ServerUrl.rootUrl + '/rest/digitalisate/search', { params });
  }

  export_search(params: HttpParams): Observable<Blob> {
    return this.http.get(ServerUrl.rootUrl + '/rest/digitalisate/export-search', { params, responseType: 'blob'});
  }

  addComment(digitalisat_comment: UserDigitalisatComment): Observable<UserDigitalisatComment> {
    return this.http.post<UserDigitalisatComment>(ServerUrl.rootUrl + '/rest/digitalisate/addComment', digitalisat_comment);
  }

  getComments(digitalisat_id: string): Observable<Array<UserDigitalisatComment>> {
    return this.http.get<Array<UserDigitalisatComment>>(ServerUrl.rootUrl + '/rest/digitalisate/getComments/' + digitalisat_id);
  }

  updateComment(digitalisat_comment: UserDigitalisatComment): Observable<boolean> {
    return this.http.post<boolean>(ServerUrl.rootUrl + '/rest/digitalisate/updateComment', digitalisat_comment);
  }

  deleteComment(digitalisat_comment: UserDigitalisatComment): Observable<boolean> {
    return this.http.delete<boolean>(ServerUrl.rootUrl + '/rest/digitalisate/deleteComment/' + digitalisat_comment.id);
  }

  getImagesFromDigitalisat(id: string, textSearch = ''): Observable<Array<DigitalisatImage>> {
    const params = new HttpParams({ fromObject: {'textSearch': textSearch.trim()} });
    return this.http.get<Array<DigitalisatImage>>(ServerUrl.rootUrl + '/rest/digitalisate/digitalisatImages?digitalisatId=' + id, {params});
  }

  getImagesFromDigitalisatAndCategory(digitalisatId: string, categoryId: string, textSearch = ''): Observable<Array<DigitalisatImage>> {
    const params = new HttpParams({ fromObject: {'textSearch': textSearch.trim()} });
    return this.http.get<Array<DigitalisatImage>>(ServerUrl.rootUrl + '/rest/digitalisate/' +
      'digitalisatImagesCategory?digitalisatId=' + digitalisatId + '&categoryId=' + categoryId, {params});
  }

  downloadImage(imageId: string): Observable<Blob> {
    return this.http.get(ServerUrl.rootUrl + '/rest/digitalisate/image?imageId=' + imageId, {
      responseType: 'blob'
    });
  }

  getOcrData(imageId: string): Observable<OcrData> {
    return this.http.get<OcrData>(ServerUrl.rootUrl + '/rest/digitalisate/ocrData?imageId=' + imageId);
  }

  getFoundTerms(imageId: string, categoryId: string): Observable<Array<SearchTermsFound>> {
    return this.http.get<Array<SearchTermsFound>>(ServerUrl.rootUrl + '/rest/digitalisate/foundTerms?imageId='
      + imageId + '&categoryId=' + categoryId);
  }

  removeDigitalisateFilesFromClassification(digitalisatId: string, categoryId: string): Observable<boolean> {
    return this.http.delete<boolean>(ServerUrl.rootUrl + '/rest/digitalisate/removeAllFileFromClassification/'
      + digitalisatId + '/' + categoryId);
  }

  removeImageFromCategory(imageId: string, categoryId: string): Observable<boolean> {
    return this.http.delete<boolean>(ServerUrl.rootUrl + '/rest/digitalisate/removeFileFromClassification/'
      + imageId + '/' + categoryId);
  }

  addFileToClassification(imageId: string, categoryId: string): Observable<boolean> {
    return this.http.post<boolean>(ServerUrl.rootUrl + '/rest/digitalisate/addFileToClassification',
      {'image_id': imageId, 'category_id': categoryId});
  }

  changeClassificationStatus(digitalisatId: string, categoryId: string, status: EnumClassificationStatus): Observable<boolean> {
    return this.http.post<boolean>(ServerUrl.rootUrl + '/rest/digitalisate/changeClassificationStatus',
      {'digitalisat_id': digitalisatId, 'category_id': categoryId, 'status': status});
  }

  changeClassificationOwnership(digitalisatId: string, categoryId: string, status: boolean): Observable<boolean> {
    return this.http.post<boolean>(ServerUrl.rootUrl + '/rest/digitalisate/changeClassificationOwnership',
      {'digitalisat_id': digitalisatId, 'category_id': categoryId, 'has_ownership': status});
  }

  changeClassificationLocation(digitalisatId: string, categoryId: string, status: boolean): Observable<boolean> {
    return this.http.post<boolean>(ServerUrl.rootUrl + '/rest/digitalisate/changeClassificationLocation',
      {'digitalisat_id': digitalisatId, 'category_id': categoryId, 'has_location': status});
  }

  reclassifyDigitalisat(digitalisatId: string, categoryId= ''): Observable<Digitalisat> {
    return this.http.post<Digitalisat>(ServerUrl.rootUrl + '/rest/digitalisate/reclassifyDigitalisat',
      {'digitalisat_id': digitalisatId, 'category_id': categoryId});
  }

  unlockDigitalisatClassification(digitalisatId: string, categoryId: string): Observable<Digitalisat> {
    return this.http.post<Digitalisat>(ServerUrl.rootUrl + '/rest/digitalisate/unlockDigitalisatClassification',
      {'digitalisat_id': digitalisatId, 'category_id': categoryId});
  }

  addToReclassifyJob(categoryId= ''): Observable<string> {
    return this.http.post<string>(ServerUrl.rootUrl + '/rest/digitalisate/addToReclassifyJob',
      {'category_id': categoryId});
  }

  isClassificationRunning(): Observable<boolean> {
    return this.http.get<boolean>(ServerUrl.rootUrl + '/rest/digitalisate/isClassificationRunning');
  }

  getInfo(): Observable<[DigitalisatInfo]> {
    return this.http.get<[DigitalisatInfo]>(ServerUrl.rootUrl + '/rest/digitalisate/info');
  }

  getImageNers(imageId: string, cleanText = true): Observable<FoundEntities> {
    const params = new HttpParams({ fromObject: {'image_id': imageId.trim(), 'clean_text': cleanText} });
    return this.http.get<FoundEntities>(ServerUrl.rootUrl + '/rest/digitalisate/imageNERs', {params});
  }

}
