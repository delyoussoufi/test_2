import { NgModule } from '@angular/core';
import { provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import localeDE from '@angular/common/locales/de';
import {NgOptimizedImage, registerLocaleData} from '@angular/common';

import { AlertModule } from 'ngx-bootstrap/alert';
import { CollapseModule } from 'ngx-bootstrap/collapse';
import { BsDatepickerModule } from 'ngx-bootstrap/datepicker';
import { BsDropdownModule } from 'ngx-bootstrap/dropdown';
import { ButtonsModule } from 'ngx-bootstrap/buttons';
import { ModalModule } from 'ngx-bootstrap/modal';
import { PaginationModule } from 'ngx-bootstrap/pagination';
import { PopoverModule } from 'ngx-bootstrap/popover';
import {CarouselModule} from 'ngx-bootstrap/carousel';
import { TabsModule } from 'ngx-bootstrap/tabs';
import { TimepickerModule } from 'ngx-bootstrap/timepicker';
import { TypeaheadModule } from 'ngx-bootstrap/typeahead';
import { defineLocale } from 'ngx-bootstrap/chronos';
import { deLocale } from 'ngx-bootstrap/locale';
import {ProgressbarModule} from 'ngx-bootstrap/progressbar';
import {SortableModule} from 'ngx-bootstrap/sortable';
import {UiSwitchModule} from 'ngx-ui-switch';

import { routing } from './app.routing';

import { AdminComponent } from './components/admin/admin.component';
import { ApplicationParamService } from './services/application-param/application-param.service';
import { AppComponent } from './app.component';
import { AuthService } from './services/auth/auth.service';
import { CloneService } from './services/clone/clone.service';
import { ConversionService } from './services/conversion/conversion.service';
import { ErrorInterceptor } from './interceptors/error.interceptor';
import { ExceptionDetailComponent } from './components/exception/exception-detail/exception-detail.component';
import { ExceptionListComponent } from './components/exception/exception-list/exception-list.component';
import { ExceptionService } from './services/exception/exception.service';
import { LoginComponent } from './components/login/login.component';
import { HomeComponent } from './components/home/home.component';
import { PageNotFoundComponent } from './components/not-found/not-found.component';
import { ProfileComponent } from './components/profile/profile.component';
import { ProfileService } from './services/profile/profile.service';
import { ToasterNotificationService } from './services/notification/toaster-notification.service';
import { TokenInterceptor } from './interceptors/token.interceptor';
import {RightPermission, UrlPermission} from './urlPermission/url.permission';
import { UserEditComponent } from './components/user/user-edit/user-edit.component';
import { UserCreateComponent } from './components/user/user-create/user-create.component';
import { UserListComponent } from './components/user/user-list/user-list.component';
import { ReportingService } from './services/reporting/reporting.service';
import { UserService } from './services/user/user.service';
import { VorgangService } from './services/vorgang/vorgang.service';
import { VorgangListComponent } from './components/vorgang/vorgang-list/vorgang-list.component';
import { VorgangViewComponent } from './components/vorgang/vorgang-view/vorgang-view.component';
import { ApplicationParamListComponent } from './components/application-param/application-param-list/application-param-list.component';
import { ApplicationParamEditComponent } from './components/application-param/application-param-edit/application-param-edit.component';
import {SearchCategoryCreateComponent} from './components/search-category/search-category-create/search-category-create.component';
import {SearchCategoryEditComponent} from './components/search-category/search-category-edit/search-category-edit.component';
import {SearchCategoryListComponent} from './components/search-category/search-category-list/search-category-list.component';
import {SearchCategoryService} from './services/search-category/search-category.service';
import {DigitalisatListComponent} from './components/digitalisat/digitalisat-list/digitalisat-list.component';
import {DigitalisatService} from './services/digitalisat/digitalisat.service';
import {TargetFolderComponent} from './components/target-folder/target-folder.component';
import {SearchBestandListComponent} from './components/search-bestand/search-bestand-list/search-bestand-list.component';
import {SearchBestandCreateComponent} from './components/search-bestand/search-bestand-create/search-bestand-create.component';
import {SearchBestandService} from './services/search-bestand/search-bestand.service';
import {DigiConnectionService} from './services/digi-connection/digi-connection.service';
import { DigitalisatEditComponent } from './components/digitalisat/digitalisat-edit/digitalisat-edit.component';
import { DigitalisatImageViewComponent } from './components/digitalisat/digitalisat-image-view/digitalisat-image-view.component';
import { OcrImageViewerComponent } from './components/reusable/ocr-image-viewer/ocr-image-viewer.component';
import {DownloadFilePipe} from './pipes/download-file-pipe';
import {BlobToSafeUrlPipe} from './pipes/blob-to-safeurl';
import { ReclassifyViewComponent } from './components/reclassify/reclassify-view/reclassify-view.component';
import { ProgressEventComponent } from './components/reusable/progress-event/progress-event.component';
import {InViewDirective} from './directives/inview.directive';
import { GalleryImageViewerComponent } from './components/reusable/gallery-image-viewer/gallery-image-viewer.component';
import { MetadataCommentsViewComponent } from './components/reusable/metadata-comments-view/metadata-comments-view.component';
import { SplitterComponent } from './components/reusable/splitter/splitter.component';
import { OcrTextHighlightDirective } from './directives/ocr-text-highlight.directive';
import { DigitalisatMetadataSearchComponent } from './components/digitalisat/digitalisat-metadata-search/digitalisat-metadata-search.component';
import { OrderBySelectorComponent } from './components/reusable/order-by-selector/order-by-selector.component';
import { CommentViewerComponent } from './components/reusable/comment-viewer/comment-viewer.component';
import { ParseInnerHtmlTextDirective } from './directives/parse-inner-html-text.directive';
import { SelectableImageComponent } from './components/reusable/selectable-image/selectable-image.component';
import { DigitalisatInfoComponent } from './components/digitalisat/digitalisat-info/digitalisat-info.component';
import { ReplaceWhitePipe } from './pipes/replace-white.pipe';
import { UserRoleRightsComponent } from './components/user/user-role-rights/user-role-rights.component';
import {
    DigitalisatQueryExportComponent
} from "./components/digitalisat/digitalisat-query-export/digitalisat-query-export.component";
import {BaseChartDirective, provideCharts, withDefaultRegisterables} from "ng2-charts";

defineLocale('de', deLocale);  // bootstrap
registerLocaleData(localeDE);  // angular

@NgModule({ declarations: [
        AppComponent,
        AdminComponent,
        ApplicationParamListComponent,
        ApplicationParamEditComponent,
        DigitalisatListComponent,
        ExceptionDetailComponent,
        ExceptionListComponent,
        HomeComponent,
        LoginComponent,
        UserEditComponent,
        UserListComponent,
        PageNotFoundComponent,
        ProfileComponent,
        UserCreateComponent,
        SearchBestandCreateComponent,
        SearchBestandListComponent,
        SearchCategoryCreateComponent,
        SearchCategoryEditComponent,
        SearchCategoryListComponent,
        TargetFolderComponent,
        VorgangListComponent,
        VorgangViewComponent,
        AdminComponent,
        DigitalisatEditComponent,
        DigitalisatImageViewComponent,
        OcrImageViewerComponent,
        DownloadFilePipe,
        BlobToSafeUrlPipe,
        ReclassifyViewComponent,
        ProgressEventComponent,
        InViewDirective,
        GalleryImageViewerComponent,
        MetadataCommentsViewComponent,
        SplitterComponent,
        OcrTextHighlightDirective,
        DigitalisatMetadataSearchComponent,
        OrderBySelectorComponent,
        CommentViewerComponent,
        ParseInnerHtmlTextDirective,
        SelectableImageComponent,
        DigitalisatInfoComponent,
        ReplaceWhitePipe,
        UserRoleRightsComponent
    ],
    bootstrap: [AppComponent], imports: [NgOptimizedImage,
        BrowserModule,
        BrowserAnimationsModule,
        FormsModule,
        routing,
        UiSwitchModule,
        AlertModule.forRoot(),
        BsDatepickerModule.forRoot(),
        BsDropdownModule.forRoot(),
        ButtonsModule.forRoot(),
        CollapseModule.forRoot(),
        ModalModule.forRoot(),
        PaginationModule.forRoot(),
        PopoverModule.forRoot(),
        TimepickerModule.forRoot(),
        TabsModule.forRoot(),
        TypeaheadModule.forRoot(),
        ProgressbarModule.forRoot(),
        CarouselModule.forRoot(),
        SortableModule.forRoot(),
        DigitalisatQueryExportComponent,
        BaseChartDirective], providers: [
        ApplicationParamService,
        AuthService,
        CloneService,
        ConversionService,
        DigitalisatService,
        DigiConnectionService,
        ExceptionService,
        ProfileService,
        ReportingService,
        SearchCategoryService,
        SearchBestandService,
        ToasterNotificationService,
        provideCharts(withDefaultRegisterables()),
        UserService,
        {
            provide: HTTP_INTERCEPTORS,
            useClass: TokenInterceptor,
            multi: true
        },
        {
            provide: HTTP_INTERCEPTORS,
            useClass: ErrorInterceptor,
            multi: true
        },
        UrlPermission,
        RightPermission,
        VorgangService,
        provideHttpClient(withInterceptorsFromDi())
    ] })

export class AppModule { }
