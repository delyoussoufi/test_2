import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable()
export class ToasterNotificationService {

  private successMessageSource = new Subject<string>();
  successMessage$ = this.successMessageSource.asObservable();
  private errorMessageSource = new Subject<string>();
  errorMessage$ = this.errorMessageSource.asObservable();

  constructor() { }

  showSuccessMessage(message: string) {
    this.successMessageSource.next(message);
  }

  showErrorMessage(message: string) {
    this.errorMessageSource.next(message);
  }

}
