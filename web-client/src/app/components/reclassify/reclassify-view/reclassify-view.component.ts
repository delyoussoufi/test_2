import {AfterViewInit, Component, OnDestroy, TemplateRef} from '@angular/core';

import {Observable} from 'rxjs';

import {BsModalService} from 'ngx-bootstrap/modal';
import {BsModalRef} from 'ngx-bootstrap/modal/bs-modal-ref.service';

import {ComponentUtils} from '../../component.utils';
import {ToasterNotificationService} from '../../../services/notification/toaster-notification.service';
import {DigitalisatService} from '../../../services/digitalisat/digitalisat.service';
import {SearchCategory} from '../../../model/model.search-category';
import {SearchCategoryService} from '../../../services/search-category/search-category.service';
import {ProgressEventComponent} from '../../reusable/progress-event/progress-event.component';


@Component({
    selector: 'app-reclassify-view',
    templateUrl: './reclassify-view.component.html',
    styleUrls: ['./reclassify-view.component.css'],
    standalone: false
})
export class ReclassifyViewComponent extends ComponentUtils implements AfterViewInit, OnDestroy {

  progressEvent: ProgressEventComponent;

  searchCategoriesWithoutDefault$: Observable<Array<SearchCategory>>;
  selectedSearchCategoryReclassify: SearchCategory = null;
  isClassifying = false;
  reclassifyModalRef: BsModalRef | null;
  reClassifyTotal = 0;



  constructor(private toasterNotificationService: ToasterNotificationService, private digitalisatService: DigitalisatService,
              private searchCategoryService: SearchCategoryService, private modalService: BsModalService) {
    super(toasterNotificationService);
    this.searchCategoriesWithoutDefault$ = this.searchCategoryService.all(true);
  }

  ngAfterViewInit(): void {
    this.digitalisatService.isClassificationRunning().subscribe(
      isClassifying => {
        this.isClassifying = isClassifying;
        if (isClassifying) {
          this.progressEvent.startListenProgress('reclassify_digitalisate');
        }
      }
    );
  }

  ngOnDestroy(): void {}

  onProgressEventLoad(e) {
    this.progressEvent = e;
  }

  onCompleteReclassify() {
    this.isClassifying = false;
    this.toasterNotificationService.showSuccessMessage('Reclassification done');
  }

  openReclassifyModal(template: TemplateRef<any>) {
    this.reclassifyModalRef = this.modalService.show(template);
  }

  closeReclassifyModal() {
    this.reclassifyModalRef?.hide();
    this.reclassifyModalRef = null;
    this.selectedSearchCategoryReclassify = null;
  }

  reclassify(progressEvent: ProgressEventComponent) {
    this.digitalisatService.totalOpenDigitalisateInCategory(this.selectedSearchCategoryReclassify?.id).subscribe(
      data => this.reClassifyTotal = data
    );
    this.digitalisatService.addToReclassifyJob(this.selectedSearchCategoryReclassify?.id).subscribe(
      pId => {
        this.isClassifying = true;
        this.toasterNotificationService.showSuccessMessage('Reclassification started');
        this.progressEvent.startListenProgress(pId);
      },
      error => {
        console.log(error);
        this.isClassifying = false;
        this.toasterNotificationService.showErrorMessage('Error when trying reclassification.');
      }
    );
    this.closeReclassifyModal();
  }

}
