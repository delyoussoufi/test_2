import {Component, OnInit, TemplateRef} from '@angular/core';
import {ComponentUtils} from '../component.utils';
import {ToasterNotificationService} from '../../services/notification/toaster-notification.service';
import {BsModalRef} from 'ngx-bootstrap/modal/bs-modal-ref.service';
import {BsModalService} from 'ngx-bootstrap/modal';
import {TargetFolder} from '../../model/model.target-folder';
import {ApplicationParamService} from '../../services/application-param/application-param.service';
import { doughnutOptions, doughnutChartColors } from './chart-doughnut-config';
import {SystemInfo} from "../../model/model.system-info";
import {map} from "rxjs/operators";
import {Observable} from "rxjs";

@Component({
    selector: 'app-target-folder',
    templateUrl: './target-folder.component.html',
    styleUrls: ['./target-folder.component.css'],
    standalone: false
})
export class TargetFolderComponent extends ComponentUtils implements OnInit {

  activateTargetFolderId: string;
  addTargetFolderPath: string;
  targetFolders: Array<TargetFolder>;
  activateTargetFolderModalRef: BsModalRef;
  deleteTargetFolder: TargetFolder;
  deleteTargetFolderModalRef: BsModalRef;
  addTargetFolderModalRef: BsModalRef;

  totalDiskSpace = 0;
  unit = 'GB';

  // Doughnut
  public doughnutChartColors = doughnutChartColors;
  public doughnutOptions = doughnutOptions;
  // public doughnutChartData = [{data: [100, 0], label: 'Test'}];
  public diskInfo$: Observable<any>;
  public doughnutChartLabels: string[] = [0 + ' GB Belegter Speicher', 0 + ' GB Freier Speicher'];
  public doughnutChartType = 'doughnut';

  constructor(private modalService: BsModalService, private applicationParamService: ApplicationParamService,
              private toasterNotificationService: ToasterNotificationService) {
    super(toasterNotificationService);
  }

  ngOnInit() {
    this.applicationParamService.getTargetFolders().subscribe(
      data => {
        this.targetFolders = data;
      },
      error => console.log(error)
    );

    this.diskInfo$ = this.applicationParamService.getSystemInfo().pipe(
      map(systemInfo => {
        return {
          datasets: [{
            data: this.setupDiskInfo(systemInfo),
            label: " size",
            backgroundColor: this.doughnutChartColors,
          }],
          // These labels appear in the legend and in the tooltips when hovering different arcs
          labels: this.doughnutChartLabels

        }
      })
    );
  }

  saveTargetFolder(targetFolder: TargetFolder) {
    if (targetFolder.editPath) {
      targetFolder.path = targetFolder.editPath;
    }

    this.applicationParamService.saveTargetFolder(targetFolder).subscribe(
      returnTargetFolder => {
        this.showSuccessMessage('Saved');
      },
      error => {
        console.log(error);
        this.showErrorMessage(error.message);
      }
    );

  }

  openActivateTargetFolderModal(template: TemplateRef<any>, targetFolderId: string) {
    this.activateTargetFolderId = targetFolderId;
    this.activateTargetFolderModalRef = this.modalService.show(template);
  }

  activateTargetFolderFromModal() {
    if (this.activateTargetFolderId) {
      this.applicationParamService.activateTargetFolder(this.activateTargetFolderId).subscribe(
        data => {
          this.targetFolders = data;
          this.closeActivateTargetFolderModal();
          this.showSuccessMessage('Zielverzeichnis aktiviert');
        },
        error => {
          console.log(error);
          this.closeActivateTargetFolderModal();
          this.showErrorMessage('Zielverzeichnis konnte nicht aktiviert werden.');
        }
      );
    }
  }

  closeActivateTargetFolderModal() {
    this.activateTargetFolderId = null;
    this.activateTargetFolderModalRef.hide();
    this.activateTargetFolderModalRef = null;
  }

  openDeleteTargetFolderModal(template: TemplateRef<any>, targetFolder: TargetFolder) {
    this.deleteTargetFolder = targetFolder;
    this.deleteTargetFolderModalRef = this.modalService.show(template);
  }

  deleteTargetFolderFromModal() {
    if (this.deleteTargetFolder) {
      this.applicationParamService.deleteTargetFolder(this.deleteTargetFolder.id).subscribe(
        () => {
          if (this.targetFolders.includes(this.deleteTargetFolder)) {
            this.targetFolders.splice(this.targetFolders.indexOf(this.deleteTargetFolder), 1);
            this.showSuccessMessage('Zielverzeichnis gelöscht');
          }
          this.closeDeleteTargetFolderModal();
        },
        error => {
          console.log(error);
          this.closeDeleteTargetFolderModal();
          if (error && error.error && error.error) {
            this.showErrorMessage(error.error);
          } else {
            this.showErrorMessage('Zielverzeichnis konnte nicht gelöscht werden.');
          }
        }
      );
    }
  }

  closeDeleteTargetFolderModal() {
    this.deleteTargetFolder = null;
    this.deleteTargetFolderModalRef.hide();
    this.deleteTargetFolderModalRef = null;
  }

  openAddTargetFolderModal(template: TemplateRef<any>) {
    this.addTargetFolderModalRef = this.modalService.show(template);
  }

  addTargetFolderFromModal() {
    if (this.addTargetFolderPath) {
      const targetFolder = new TargetFolder();
      targetFolder.path = this.addTargetFolderPath;
      this.applicationParamService.createTargetFolder(targetFolder).subscribe(
        data => {
          this.targetFolders.push(data);
          this.closeAddTargetFolderModal();
          this.showSuccessMessage('Zielverzeichnis hinzugefügt');
        },
        error => {
          console.log(error);
          this.closeAddTargetFolderModal();
          this.showErrorMessage('Zielverzeichnis konnte nicht hinzugefügt werden.');
        }
      );
    }
  }

  changePathValue(targetFolder: TargetFolder, event: any) {
    targetFolder.editPath = event.target.textContent.trim();
    console.log(targetFolder.editPath);
  }

  closeAddTargetFolderModal() {
    this.addTargetFolderPath = null;
    this.addTargetFolderModalRef.hide();
    this.addTargetFolderModalRef = null;
  }
  private setupDiskInfo(systemInfo: SystemInfo): number[] {
    this.totalDiskSpace = systemInfo.totalDiskSpace;
    let availableSpace = systemInfo.availableDiskSpace;
    let usedSpace = systemInfo.usedDiskSpace;
    // Change scale to TB if necessary
    if (this.totalDiskSpace > 999) {
      availableSpace = availableSpace * 0.000976563;
      usedSpace = usedSpace * 0.000976563;
      this.totalDiskSpace = this.totalDiskSpace * 0.000976563;
      this.unit = 'TB';
    }
    // Clean labels and set new values.
    this.doughnutChartLabels.length = 0;
    this.doughnutChartLabels.push(usedSpace.toPrecision(4) + ' ' + this.unit + ' Belegter Speicher');
    this.doughnutChartLabels.push(availableSpace.toPrecision(4) + ' ' + this.unit + ' Freier Speicher');
    // Set new data.
    return [usedSpace , availableSpace];
  }


}
