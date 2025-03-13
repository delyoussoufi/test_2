import { CloneService } from '../../services/clone/clone.service';
import { Component, OnInit } from '@angular/core';
import {forkJoin} from 'rxjs';
import { ProfileService } from '../../services/profile/profile.service';
import { ToasterNotificationService } from '../../services/notification/toaster-notification.service';
import { ProfileUser } from '../../model/model.profile-user';
import { ComponentUtils } from '../component.utils';

@Component({
    selector: 'app-profile-form',
    templateUrl: './profile.component.html',
    styleUrls: ['./profile.component.css'],
    standalone: false
})
export class ProfileComponent extends ComponentUtils implements OnInit {

  profileUser: ProfileUser = new ProfileUser();

  constructor(private profileService: ProfileService,
    private cloneService: CloneService, private toasterNotificationService: ToasterNotificationService) {
    super(toasterNotificationService);
    this.profileService.get().subscribe(
      user => {
        this.profileUser.updateFromUser(user);
      }
    );
  }

  ngOnInit() {}

  updateProfile() {
    this.profileService.update(this.profileUser).subscribe({
        next: user => {
          this.profileUser.updateFromUser(user);
          super.showSuccessMessage('Profil aktualisiert.');
        },
        error: error => {
          console.log(error);
        }
    });
  }

}
