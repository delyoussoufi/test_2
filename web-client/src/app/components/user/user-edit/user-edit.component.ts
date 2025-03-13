import {ToasterNotificationService} from '../../../services/notification/toaster-notification.service';
import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from '@angular/router';

import {CloneService} from '../../../services/clone/clone.service';
import {User} from '../../../model/model.user';
import {UserService} from '../../../services/user/user.service';
import {ComponentUtils} from '../../component.utils';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';

@Component({
    selector: 'app-user-edit',
    templateUrl: './user-edit.component.html',
    styleUrls: ['./user-edit.component.css'],
    standalone: false
})
export class UserEditComponent extends ComponentUtils implements OnInit {

  _user: User | undefined;
  user$: Observable<User> | undefined;

  constructor(private route: ActivatedRoute,
    private toasterNotificationService: ToasterNotificationService, private userService: UserService) {
    super(toasterNotificationService);
    this.route.params.subscribe(params => {
      if (params && params.id) {
        this.user$ = this.userService.get(params.id).pipe(
          map( user=> {
            this._user = user;
            if (!this.user) {
              this.toasterNotificationService.showErrorMessage("No user found")
            }
            return user;
          })
        );
      }
    });
  }

  ngOnInit() {
  }

  get user() {
    return this._user;
  }

  set user(user: User) {
    this._user = user;
  }

  updateUser(user: User) {
    this.userService.update(user).subscribe(
      user => {
        this._user = user;
        super.showSuccessMessage('Nutzer aktualisiert.');
      },
      error => {
        console.log(error);
      }
    );
  }

}
