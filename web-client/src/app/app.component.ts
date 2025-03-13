import { ToasterNotificationService } from './services/notification/toaster-notification.service';
import { Component } from '@angular/core';
import { OnInit } from '@angular/core';
import { debounceTime } from 'rxjs/operators';
import { Subject } from 'rxjs';
import { ComponentUtils } from './components/component.utils';
import { AuthService } from './services/auth/auth.service';
import { User } from './model/model.user';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css'],
    standalone: false
})
export class AppComponent extends ComponentUtils implements OnInit {
  title = 'Registro';
  private _error = new Subject<string>();
  errorMessage: string;
  private _success = new Subject<string>();
  successMessage: string;

  constructor(private authService: AuthService, private toasterNotificationService: ToasterNotificationService) {
    super(toasterNotificationService);
    this.updateUser();
    toasterNotificationService.errorMessage$.subscribe(
      message => {
        this._error.next(message);
      });
    toasterNotificationService.successMessage$.subscribe(
      message => {
        this._success.next(message);
      });
  }

  public ngOnInit() {
    this._success.subscribe((m) => this.successMessage = m);
    this._success.pipe(debounceTime(5000)).subscribe(m => {
      this.successMessage = null;
    });
    this._error.subscribe((m) => this.errorMessage = m);
    this._error.pipe(debounceTime(5000)).subscribe(m => {
      this.errorMessage = null;
    });
  }

  public logout() {
    this.currentUser = undefined;
    this.authService.logOut();
  }

  public updateUser() {
    this.currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (this.currentUser) {
      this.authService.hasToken(this.currentUser.token, this.currentUser.userId).subscribe(
        hasToken => {
          if (!hasToken) {
            this.showErrorMessage('Die bestehende Anmeldung konnte nicht validiert werden.');
            this.logout();
          }
        },
        error => {
          this.showErrorMessage('Die bestehende Anmeldung konnte nicht validiert werden.');
          this.logout();
        }
      );
    } else {
      this.logout();
    }
  }

}
