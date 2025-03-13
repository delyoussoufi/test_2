import {SearchCategory} from '../../model/model.search-category';
import {Injectable} from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {ServerUrl} from '../../statics/server-url';
import {SearchResult} from '../../model/model.search-result';

@Injectable()
export class SearchCategoryService {

  constructor(private http: HttpClient) { }

  get(id: string): Observable<SearchCategory> {
    return this.http.get<SearchCategory>(ServerUrl.rootUrl + '/rest/searchCategories/' + id);
  }

  all(removeUnclassified= false): Observable<Array<SearchCategory>> {
    const obs$ = this.http.get<Array<SearchCategory>>(ServerUrl.rootUrl + '/rest/searchCategories/all');
    if (removeUnclassified) {
      return obs$.pipe(
        map((data => {
          return data.filter(sc => sc.name !== 'Unclassified');
        })));
    }
    return obs$;
  }

  create(searchCategory: SearchCategory): Observable<any> {
    return this.http.post(ServerUrl.rootUrl + '/rest/searchCategories', searchCategory).pipe(
      map((response: Response) => {
        return response;
      }));
  }

  update(searchCategory: SearchCategory): Observable<any> {
    return this.http.put(ServerUrl.rootUrl + '/rest/searchCategories', searchCategory).pipe(
      map((response: Response) => {
        return response;
      }));
  }

  exportAllSearchCategoriesToExcel() {
    const params = new HttpParams();
    const options = { params, responseType: 'arraybuffer' as 'arraybuffer' };
    this.http.post(ServerUrl.rootUrl + '/rest/searchCategories/exportSearchCategoriesExcel', null,
      options)
      .subscribe({
        next: data =>
          this.downloadFile(data, 'application/xlsx', 'SuchkategorieExport.xlsx'),
        error: error =>
          console.log(error)
      });
  }

  reorder(searchCategories: Array<SearchCategory>): Observable<boolean> {
    return this.http.post<boolean>(ServerUrl.rootUrl + '/rest/searchCategories/reorder', searchCategories);
  }

  exportSearchResultToExcel(params: HttpParams) {
    const options = { params, responseType: 'arraybuffer' as 'arraybuffer' };
    this.http.post(ServerUrl.rootUrl + '/rest/searchCategories/exportSearchCategoriesExcelSearch', null,
      options).subscribe({
        next: data =>
          this.downloadFile(data, 'application/xlsx', 'SuchkategorieExportSuche.xlsx'),
        error: error =>
          console.log(error)
      });
  }

  exportClassificationResults(categoryId: string): Observable<Blob>  {
    return this.http.get(ServerUrl.rootUrl + '/rest/searchCategories/export-classification-results/' + categoryId,
      { responseType: 'blob'});
  }



  downloadFile(data: any, type: string, filename: string): string {
    const url = window.URL.createObjectURL(new Blob([data], {type: type}));

    // create hidden dom element (so it works in all browsers)
    const a = document.createElement('a');
    a.setAttribute('style', 'display:none;');
    document.body.appendChild(a);

    // create file, attach to hidden element and open hidden element
    a.href = url;
    a.download = filename;
    a.click();
    return url;
  }

  delete(searchCategory: SearchCategory): Observable<any> {
    return this.http.delete(ServerUrl.rootUrl + '/rest/searchCategories/' + searchCategory.id);
  }

  search(params: HttpParams): Observable<SearchResult<SearchCategory>> {
    return this.http.get<SearchResult<SearchCategory>>(ServerUrl.rootUrl + '/rest/searchCategories/search', { params });
  }

}
