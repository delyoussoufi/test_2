import { Injectable } from '@angular/core';
import { Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';

import {User} from '../model/model.user';

@Injectable()
export class UrlPermission  {

  constructor(private router: Router) { }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {
    if (localStorage.getItem('currentUser')) {
      // logged in so return true
      return true;
    }

    // not logged in so redirect to login page with the return url
    this.router.navigate(['/login'], { queryParams: { returnUrl: state.url }});
    return false;
  }
}


@Injectable()
export class RightPermission  {

  constructor(private router: Router) { }

  get currentUser(): User | null{
    return JSON.parse(localStorage.getItem('currentUser'));
  }

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot) {

    if (!route.data["rights"]) {
      console.error("You must provide a data['rights'] to use RightPermission. i.e: data: {rights: ['RIGHT_USER_CREATE']}");
      return false;
    }
    const rights: string[] = route.data["rights"]

    for (const right of rights ) {
      if (this.currentUser && this.currentUser.rights.includes(right)) {
        return true;
      }
    }
    // Don't have rights.
    console.log("You don't have permission to access this page.");
    this.router.navigate(['/'], { queryParams: { returnUrl: state.url }});
    return false;
  }
}
