import {Router} from '@angular/router';
import {Component, OnInit, ViewEncapsulation} from '@angular/core';

import {User} from '../../model/model.user';
import {AuthService} from '../../services/auth/auth.service';
import {AppComponent} from '../../app.component';


@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.css'],
    encapsulation: ViewEncapsulation.None,
    standalone: false
})
export class LoginComponent implements OnInit {
  user: User = new User();
  errorMessage: string;
  constructor(private authService: AuthService, private router: Router,
    private appComponent: AppComponent) { }

  ngOnInit() {
  }

  login() {
    this.authService.logIn(this.user).subscribe({
      next: data => {
        if (data) {
          this.router.navigate(['/digitalisate']);
          this.appComponent.updateUser();
        } else {
          this.errorMessage = 'Fehler :  Anmeldung konnte nicht erfolgen';
        }
      },
      error: err => {
        console.log(err);
        this.errorMessage = 'Fehler :  Anmeldung konnte nicht erfolgen';
      }
    });
  }

}
