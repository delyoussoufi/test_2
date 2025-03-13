import { Routes, RouterModule } from '@angular/router';

import { AdminComponent } from './components/admin/admin.component';
import { ExceptionDetailComponent } from './components/exception/exception-detail/exception-detail.component';
import { ExceptionListComponent } from './components/exception/exception-list/exception-list.component';
import { HomeComponent } from './components/home/home.component';
import { LoginComponent } from './components/login/login.component';
import { ProfileComponent } from './components/profile/profile.component';
import { UserCreateComponent } from './components/user/user-create/user-create.component';
import { UserEditComponent } from './components/user/user-edit/user-edit.component';
import { UserListComponent } from './components/user/user-list/user-list.component';
import {RightPermission, UrlPermission} from './urlPermission/url.permission';
import { VorgangListComponent } from './components/vorgang/vorgang-list/vorgang-list.component';
import { VorgangViewComponent } from './components/vorgang/vorgang-view/vorgang-view.component';
import { ApplicationParamListComponent } from './components/application-param/application-param-list/application-param-list.component';
import { ApplicationParamEditComponent } from './components/application-param/application-param-edit/application-param-edit.component';
import {SearchCategoryListComponent} from './components/search-category/search-category-list/search-category-list.component';
import {SearchCategoryCreateComponent} from './components/search-category/search-category-create/search-category-create.component';
import {SearchCategoryEditComponent} from './components/search-category/search-category-edit/search-category-edit.component';
import {DigitalisatListComponent} from './components/digitalisat/digitalisat-list/digitalisat-list.component';
import {TargetFolderComponent} from './components/target-folder/target-folder.component';
import {SearchBestandListComponent} from './components/search-bestand/search-bestand-list/search-bestand-list.component';
import {SearchBestandCreateComponent} from './components/search-bestand/search-bestand-create/search-bestand-create.component';
import {DigitalisatEditComponent} from './components/digitalisat/digitalisat-edit/digitalisat-edit.component';
import {ReclassifyViewComponent} from './components/reclassify/reclassify-view/reclassify-view.component';
import {DigitalisatInfoComponent} from './components/digitalisat/digitalisat-info/digitalisat-info.component';


const appRoutes: Routes = [
  { path: 'profile', component: ProfileComponent, canActivate: [UrlPermission] },
  { path: 'digitalisate', component: DigitalisatListComponent, canActivate: [RightPermission], data: {rights: ["RIGHT_DIGITALISATE_VIEW"]}},
  { path: 'digitalisate/editDigitalisat/:id', component: DigitalisatEditComponent, canActivate: [RightPermission], data: {rights: ["RIGHT_DIGITALISATE_VIEW"]}},
  { path: 'digitalisate/editDigitalisat/:id/:categoryId', component: DigitalisatEditComponent,  canActivate: [RightPermission], data: {rights: ["RIGHT_DIGITALISATE_VIEW"]}},
  { path: 'vorgaenge', component: VorgangListComponent,  canActivate: [RightPermission], data: {rights: ["RIGHT_VORGANG"]}},
  { path: 'vorgaenge/viewVorgang/:id', component: VorgangViewComponent, canActivate: [RightPermission], data: {rights: ["RIGHT_VORGANG"]} },
  { path: 'reclassify/view', component: ReclassifyViewComponent, canActivate: [RightPermission], data: {rights: ["RIGHT_RECLASSIFY"]} },
  { path: 'searchCategories', component: SearchCategoryListComponent, canActivate: [RightPermission], data: {rights: ["RIGHT_CATEGORY_VIEW"]} },
  { path: 'searchCategories/createSearchCategory', component: SearchCategoryCreateComponent, canActivate: [UrlPermission], data: {rights: ["RIGHT_CATEGORY_EDIT"]}},
  { path: 'searchCategories/editSearchCategory/:id', component: SearchCategoryEditComponent, canActivate: [UrlPermission], data: {rights: ["RIGHT_CATEGORY_EDIT"]} },
  { path: 'admin', component: AdminComponent, canActivate: [UrlPermission], children: [
      // { path: '', redirectTo: 'users', pathMatch: 'prefix'},
      { path: 'users', component: UserListComponent, canActivate: [RightPermission], data: {rights: ["RIGHT_USER_EDIT"]} },
      { path: 'users/createUser', component: UserCreateComponent, canActivate: [RightPermission], data: {rights: ["RIGHT_USER_EDIT"]} },
      { path: 'users/editUser/:id', component: UserEditComponent, canActivate: [RightPermission], data: {rights: ["RIGHT_USER_EDIT"]} },
      { path: 'applicationParams', component: ApplicationParamListComponent, canActivate: [RightPermission], data: {rights: ["RIGHT_APP_SETTINGS"]} },
      { path: 'applicationParams/editApplicationParam/:id', component: ApplicationParamEditComponent, canActivate: [RightPermission], data: {rights: ["RIGHT_APP_SETTINGS"]} },
      { path: 'searchBestaende', component: SearchBestandListComponent, canActivate: [RightPermission], data: {rights: ["RIGHT_BESTANDE_ADD"]} },
      { path: 'searchBestaende/createSearchBestand', component: SearchBestandCreateComponent, canActivate: [RightPermission], data: {rights: ["RIGHT_BESTANDE_ADD"]} },
      { path: 'targetFolders', component: TargetFolderComponent, canActivate: [RightPermission], data: {rights: ["RIGHT_APP_SETTINGS"]} },
      { path: 'exceptions', component: ExceptionListComponent, canActivate: [UrlPermission] },
      { path: 'aktenInfo', component: DigitalisatInfoComponent, canActivate: [UrlPermission]},
      { path: 'exceptions/viewExceptionLog/:id', component: ExceptionDetailComponent, canActivate: [UrlPermission] }
  ]},
  { path: 'login', component: LoginComponent },
  { path: 'home', component: HomeComponent },

  // otherwise redirect to vorgaenge
  { path: '**', redirectTo: '/home' }
];

export const routing = RouterModule.forRoot(
  appRoutes,
  {
    useHash: true,
    scrollPositionRestoration: 'enabled'
});
