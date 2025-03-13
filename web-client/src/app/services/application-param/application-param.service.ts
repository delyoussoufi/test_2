import { ApplicationParam } from './../../model/model.application-param';
import { Observable } from 'rxjs';
import {map, tap} from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { ServerUrl } from '../../statics/server-url';
import {TargetFolder} from '../../model/model.target-folder';
import {SystemInfo} from '../../model/model.system-info';

@Injectable()
export class ApplicationParamService {
  constructor(private http: HttpClient) { }

  get(id: string): Observable<ApplicationParam> {
    return this.http.get<ApplicationParam>(ServerUrl.rootUrl + '/rest/admin/applicationParams/' + id);
  }

  getAll(): Observable<Array<ApplicationParam>> {
    return this.http.get<Array<ApplicationParam>>(ServerUrl.rootUrl + '/rest/admin/applicationParams');
  }

  update(param: ApplicationParam): Observable<ApplicationParam> {
    return this.http.put<ApplicationParam>(ServerUrl.rootUrl + '/rest/admin/applicationParams', param).pipe(
      map((response: ApplicationParam) => {
        return response;
      }));
  }

  getSystemInfo(): Observable<SystemInfo> {
    return this.http.get<SystemInfo>(ServerUrl.rootUrl + '/rest/admin/diskInfo');
  }

  getTargetFolders(): Observable<Array<TargetFolder>> {
    return this.http.get<Array<TargetFolder>>(ServerUrl.rootUrl + '/rest/admin/targetFolders');
  }

  createTargetFolder(targetFolder: TargetFolder): Observable<TargetFolder> {
    return this.http.post<TargetFolder>(ServerUrl.rootUrl + '/rest/admin/targetFolders/create', targetFolder).pipe(
      tap((newTargetFolder: TargetFolder) => {
        return newTargetFolder;
      }));
  }

  activateTargetFolder(targetFolderId: string): Observable<Array<TargetFolder>> {
    return this.http.post<Array<TargetFolder>>(ServerUrl.rootUrl + '/rest/admin/targetFolders/activate/' + targetFolderId, null).pipe(
      tap((targetFolders: Array<TargetFolder>) => {
        return targetFolders;
      }));
  }

  deleteTargetFolder(targetFolderId: string): Observable<any> {
    return this.http.delete(ServerUrl.rootUrl + '/rest/admin/targetFolders/' + targetFolderId).pipe(
      map((response: Response) => {
        return response;
      }));
  }

  saveTargetFolder(targetFolder: TargetFolder): Observable<TargetFolder> {
    return this.http.post<TargetFolder>(ServerUrl.rootUrl + '/rest/admin/saveTargetFolder', targetFolder);
  }

}
