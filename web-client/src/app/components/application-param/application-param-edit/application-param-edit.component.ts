import { ActivatedRoute } from '@angular/router';
import { Component, OnInit } from '@angular/core';
import { ApplicationParam } from '../../../model/model.application-param';
import { ComponentUtils } from '../../component.utils';
import { ApplicationParamService } from '../../../services/application-param/application-param.service';
import { ServerUrl } from '../../../statics/server-url';
import { ToasterNotificationService } from '../../../services/notification/toaster-notification.service';

@Component({
    selector: 'app-application-param-edit',
    templateUrl: './application-param-edit.component.html',
    styleUrls: ['./application-param-edit.component.css'],
    standalone: false
})
export class ApplicationParamEditComponent extends ComponentUtils implements OnInit {

  param: ApplicationParam = new ApplicationParam();
  tipMessage = '';
  currentAppUrl: String;

  constructor(private route: ActivatedRoute,
    private applicationParamService: ApplicationParamService, private toasterNotificationService: ToasterNotificationService) {
    super(toasterNotificationService);
    this.currentAppUrl = ServerUrl.rootUrl.split('/Provenance')[0];
    this.route.params.subscribe(params => {
      if (params && params.id) {
        this.applicationParamService.get(params.id).subscribe(
          data => {
            this.param = data;
            this.setTipMessage(this.param.id);
          },
          error => {
            console.log(error);
          }
        );
      }
    });
  }

  ngOnInit() {
  }

  updateApplicationParam() {
    if (this.param != null && this.param.value.length > 0) {
      this.param.value = this.param.value.trim();
      this.applicationParamService.update(this.param).subscribe(
        data => {
          this.param = data;
          super.showSuccessMessage('Anwendungsparameter aktualisiert.');
        },
        error => {
          if (error && error.error && error.error.message) {
            super.showErrorMessage(error.error.message);
          }
        }
      );
    } else {
      super.showErrorMessage('Der Anwendungsparameter konnte nicht aktualisiert werden.');
    }
  }

  setTipMessage(paramId: string) {
    switch (paramId) {
      case 'appUrl':
        this.tipMessage = 'Die aktuelle URL-Domäne der Anwendung.';
        break;
      case 'uploadFolder':
        this.tipMessage = 'Der vollständige Pfad für den Upload-Ordner auf dem Server.';
        break;
      default:
        break;
    }

  }

}
