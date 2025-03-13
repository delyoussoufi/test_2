import { Injectable, Injector } from '@angular/core';
import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest, HttpErrorResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { ToasterNotificationService } from './../services/notification/toaster-notification.service';


@Injectable()
export class ErrorInterceptor implements HttpInterceptor {

  constructor(private injector: Injector) { }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const toaster = this.injector.get(ToasterNotificationService);

    return next.handle(req).pipe(
      tap((ev: HttpEvent<any>) => {
        // if (ev instanceof HttpResponse) {
        //   console.log('ev in the do: ', ev);
        // }
      }),
      catchError(err => {
        if (err instanceof HttpErrorResponse) {
          console.log(err);
          toaster.showErrorMessage(err.error?.message);
        }
        return throwError(err);
      }));
  }

}
