import { ActivatedRoute } from '@angular/router';
import { Component, OnInit } from '@angular/core';
import { ApplicationParam } from '../../../model/model.application-param';
import { ComponentUtils } from '../../component.utils';
import { ApplicationParamService } from '../../../services/application-param/application-param.service';
import { ServerUrl } from '../../../statics/server-url';
import { ToasterNotificationService } from '../../../services/notification/toaster-notification.service';

@Component({
    selector: 'app-application-param-list',
    templateUrl: './application-param-list.component.html',
    styleUrls: ['./application-param-list.component.css'],
    standalone: false
})
export class ApplicationParamListComponent extends ComponentUtils implements OnInit {

  applicationParams: Array<ApplicationParam>;
  currentAppUrl: String;

  constructor(private applicationParamService: ApplicationParamService,
    private toasterNotificationService: ToasterNotificationService) {
    super(toasterNotificationService);
    this.currentAppUrl = ServerUrl.rootUrl.split('/Provenance')[0];
  }

  ngOnInit() {
    this.applicationParamService.getAll().subscribe(
      data => {
        this.applicationParams = data;
        this.reorderParamList();
      },
      error => console.log(error)
    );
  }

  private reorderParamList() {
    this.applicationParams.sort((param1 , param2) => {
      if (param1.id < param2.id) {
        return -1;
      } else if (param1.id > param2.id) {
        return 1;
      } else {
        return 0;
      }
    });
  }

}
