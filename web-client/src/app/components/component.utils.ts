import { ToasterNotificationService } from '../services/notification/toaster-notification.service';
import { User } from '../model/model.user';

export abstract class ComponentUtils {

  bsConfig = Object.assign(
    {},
    {locale: 'de', containerClass: 'theme-dark-blue', dateInputFormat: 'DD.MM.YYYY', selectFromOtherMonth: true}
  );
  currentUser: User;

  protected constructor(private __toasterNotificationService: ToasterNotificationService) {
    this.currentUser = JSON.parse(localStorage.getItem('currentUser'));
  }

  public showSuccessMessage(message: string) {
    this.__toasterNotificationService.showSuccessMessage(message);
    window.scrollTo(0, 0);
  }

  public showErrorMessage(message: string) {
    this.__toasterNotificationService.showErrorMessage(message);
    window.scrollTo(0, 0);
  }

  public userHasRole(user: User, role: string) {
    if (user == null) {
      return false;
    }
    return !(user.roles == null || !user.roles.includes(role));
  }

  public userHasRight(user: User, right: string) {
    if (user == null) {
      return false;
    }
    return !(user.rights == null || !user.rights.includes(right));
  }

  // public userHasSetting(user: User, setting: string) {
  //   if (user == null) {
  //     return false;
  //   }
  //   if (user.settings == null || !user.settings.includes(setting)) {
  //     return false;
  //   }
  //   return true;
  // }

  public hasAdminRights(): boolean {
    const adminRights: string[] = [
      'RIGHT_USER_EDIT',
      'RIGHT_APP_SETTINGS',
      'RIGHT_BESTANDE_ADD',
    ];
    const rights: string[] = adminRights.filter( value => this.userHasRight(this.currentUser, value));

    return rights.length > 0;
  }

  public hasRole(role: string) {
    // this.currentUser = JSON.parse(localStorage.getItem('currentUser'));
    return this.userHasRole(this.currentUser, role);
  }

  public hasRight(right: string) {
    // this.currentUser = JSON.parse(localStorage.getItem('currentUser'));
    return this.userHasRight(this.currentUser, right);
  }

  /**
   * Remove item from list if found.
   * @param list The list where the item must be removed.
   * @param obj The item to remove.
   */
  public removeItemFromList(list: Array<any>, obj: any) {
    const index = list.indexOf(obj, 0);
    if (index > -1) {
      list.splice(index, 1);
    }
  }

  // public hasSetting(setting: string) {
  //   this.currentUser = JSON.parse(localStorage.getItem('currentUser'));
  //   return this.userHasSetting(this.currentUser, setting);
  // }

}
