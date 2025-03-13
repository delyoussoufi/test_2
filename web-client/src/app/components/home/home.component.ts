import { AfterContentChecked, ChangeDetectorRef, Component, OnInit, ViewEncapsulation } from '@angular/core';
import { User } from '../../model/model.user';
import { AuthService } from '../../services/auth/auth.service';
import { AppComponent } from '../../app.component';
import { Router } from '@angular/router';
import { ToasterNotificationService } from '../../services/notification/toaster-notification.service';
import { ComponentUtils } from '../component.utils';


@Component({
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.css'],
    encapsulation: ViewEncapsulation.None,
    standalone: false
})
export class HomeComponent extends ComponentUtils implements OnInit, AfterContentChecked {
  user: User = new User();
  errorMessage: string;
  constructor(private authService: AuthService,
    private cdref: ChangeDetectorRef,
    private router: Router,
    private appComponent: AppComponent,
    private toasterNotificationService: ToasterNotificationService) {
      super(toasterNotificationService);
    }

  ngOnInit() {
  }

  ngAfterContentChecked() {
    this.cdref.detectChanges();
  }

}
