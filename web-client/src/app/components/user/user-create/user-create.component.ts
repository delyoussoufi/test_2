import {Component, OnInit} from '@angular/core';

import {ToasterNotificationService} from '../../../services/notification/toaster-notification.service';
import {UserService} from '../../../services/user/user.service';
import {Role} from '../../../model/model.role';
import {User} from '../../../model/model.user';
import {ComponentUtils} from '../../component.utils';

@Component({
    selector: 'app-user-create',
    templateUrl: './user-create.component.html',
    styleUrls: ['./user-create.component.css'],
    standalone: false
})
export class UserCreateComponent extends ComponentUtils implements OnInit {

  user: User = new User();
  // roles: Role[] = [];

  constructor(private toasterNotificationService: ToasterNotificationService, private userService: UserService) {
    super(toasterNotificationService);
    // this.userService.getRoles().subscribe(
    //   data => {
    //     this.buildUserAndRoles(data, this.user);
    //   },
    //   error => console.log(error)
    // );
  }

  ngOnInit() {
  }

  // buildUserAndRoles(iRoles: Role[], iUser: User) {
  //   for (const role of iRoles) {
  //     role.selected = this.userHasRole(iUser, role.authority);
  //   }
  //   this.user = iUser;
  //   this.roles = iRoles;
  // }

  createUser(user: User) {

    this.userService.create(user).subscribe(
      data => {
        // this.user = new User();
        // this.buildUserAndRoles(this.roles, this.user);
        super.showSuccessMessage('Nutzer erstellt.');
      },
      error => {
        if(error.error && error.error.errorMessage) {
          super.showErrorMessage(error.error.errorMessage);
        } else {
          super.showErrorMessage('Nutzer konnte nicht erstellt werden.');
        }
        console.log(error);
      }
    );
  }

}
