import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {ActivatedRoute} from '@angular/router';

import {map} from 'rxjs/operators';
import {forkJoin, Observable} from 'rxjs';

import {User} from '../../../model/model.user';
import {UserService} from '../../../services/user/user.service';
import {ToasterNotificationService} from '../../../services/notification/toaster-notification.service';
import {ComponentUtils} from '../../component.utils';
import {Right} from '../../../model/model.right';
import {Role} from '../../../model/model.role';
import {CloneService} from '../../../services/clone/clone.service';

@Component({
    selector: 'app-user-role-rights',
    templateUrl: './user-role-rights.component.html',
    styleUrls: ['./user-role-rights.component.css'],
    standalone: false
})
export class UserRoleRightsComponent extends ComponentUtils implements OnInit {
  @Input()
  set user(user: User | null) {
    if (user) {
      this._user = user;
    } else {
      this._user = new User();
    }
    this.userRoleRight$ = forkJoin([this.roles$, this.rights$]).pipe(
      map( data => {
        const roles:Role[] = data[0];
        const rights: Right[] = data[1];
        this.buildUserRolesAndRights(roles, rights);
        return true;
      })
    );
  }


  @Output()
  userChange = new EventEmitter<User>();

  @Output()
  userSave = new EventEmitter<User>();


  userRoleRight$: Observable<boolean> | undefined
  rights: Right[] = [];
  roles: Role[] = [];

  protected roles$: Observable<Role[]> = this.userService.getRoles().pipe(
    map( roles => {
      this.roles = roles;
      return roles;
    })
  );
  protected rights$: Observable<Right[]> = this.userService.getRights().pipe(
    map( rights => {
      this.rights = rights;
      return rights;
    })
  );

  protected defaultRightsFromRole: string[] = [];
  private _user: User;


  constructor(private route: ActivatedRoute, private cloneService: CloneService,
              private toasterNotificationService: ToasterNotificationService, private userService: UserService) {
    super(toasterNotificationService);
  }

  ngOnInit() {
  }

  get user(){
    return this._user;
  }

  protected fetchRolesRights() {

  }

  onSelectRole(role: Role) {
    if (!role) {
      return;
    }

    // Deselect all
    this.clearRights();
    this.roles.forEach(v => v.selected = false);
    role.selected = true;
    this.userService.getRightsByRole(role.authority).subscribe(
      rightIds => {
        this.defaultRightsFromRole = rightIds;
        this.setDefaultRights();
      }
    );

  }

  protected clearRights() {
    this.rights.forEach( right => {
        right.required = false;
        right.selected = false;
      }
    );
  }

  protected setDefaultRights() {
    this.rights.forEach(right => {
        if (this.defaultRightsFromRole.includes(right.right_id)) {
          right.selected = true;
          right.required = true;
        }
      }
    );

  }

  protected setUserRole(roles: Role[]) {
    let hasRole = false;
    roles.forEach(role => {
      role.selected = this.userHasRole(this.user, role.authority);
      if (role.selected) {
        this.onSelectRole(role);
        hasRole = true;
      }
    });

    if (!hasRole) {
      const defaultRole = roles.filter(v => v.authority === 'ROLE_USER')[0]
      this.onSelectRole(defaultRole);
    }

  }

  protected setUserRights(rights: Right[]) {
    rights.forEach( right=> {
      right.selected = this.userHasRight(this.user, right.right_id);
    });

  }

  protected buildUserRolesAndRights(iRoles: Role[], iRights: Right[]) {
    this.setUserRole(iRoles);
    this.setUserRights(iRights);
  }

  onSaveClick() {
    let updateUser = this.cloneService.clone(this.user);
    const userRoles: string[] = [];
    const userRights: string[] = [];
    this.roles.forEach(role => {
      if (role.selected) {
        userRoles.push(role.authority);
      }
    });
    this.rights.forEach( right => {
      if (right.selected) {
        userRights.push(right.right_id);
      }
    });
    updateUser.roles = userRoles;
    updateUser.rights = userRights;
    this.userChange.emit(updateUser);
    this.userSave.emit(updateUser);
  }

}
