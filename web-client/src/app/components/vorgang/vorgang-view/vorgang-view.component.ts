import {Component, ElementRef, OnInit, TemplateRef, ViewChild} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {BsModalService, ModalOptions} from 'ngx-bootstrap/modal';

import {ToasterNotificationService} from '../../../services/notification/toaster-notification.service';
import {Vorgang} from '../../../model/model.vorgang';
import {VorgangService} from '../../../services/vorgang/vorgang.service';
import {ComponentUtils} from '../../component.utils';
import {DigitalisatImage} from '../../../model/model.digitalisat-image';
import {DownloadFilePipe} from '../../../pipes/download-file-pipe';
import {MetadataCommentsViewComponent} from '../../reusable/metadata-comments-view/metadata-comments-view.component';

@Component({
    selector: 'app-vorgang-view',
    templateUrl: './vorgang-view.component.html',
    styleUrls: ['./vorgang-view.component.css'],
    providers: [DownloadFilePipe],
    standalone: false
})
export class VorgangViewComponent extends ComponentUtils implements OnInit {

  @ViewChild('wrapImages', {static: true}) wrapImagesRef: ElementRef<HTMLCanvasElement>;



  vorgang: Vorgang;
  digitalisatImages: Array<DigitalisatImage> = [];
  singleImageView = false;

  private currentScrollTop = 0;

  constructor(private route: ActivatedRoute, private vorgangService: VorgangService,  private modalService: BsModalService,
              private toasterNotificationService: ToasterNotificationService, private downloadFilePipe: DownloadFilePipe) {
    super(toasterNotificationService);
    this.route.params.subscribe(params => {
      if (params && params.id) {
        this.vorgangService.get(params.id).subscribe({
          next: vorgang => {
            this.vorgang = vorgang;
            this.fetchVorgangImages(this.vorgang);
          },
          error: error => {
            console.log(error);
            this.toasterNotificationService.showErrorMessage(error.message.error);
          }
        });
      }
    });
  }

  ngOnInit(): void {}

  private create_pdf_name(): string {
    const name = this.vorgang?.name + '_' + this.digitalisatImages[0]?.name.toLowerCase().split('_image')[0];
    return name?.toLowerCase().replace(' ', '_');
  }

  sendEmail() {
    const subject = 'Vorgang ' + this.vorgang.name;
    window.open(`mailto:?subject=${subject}`);
  }

  fetchVorgangImages(vorgang: Vorgang) {
    if (vorgang) {
      this.vorgangService.getImages(vorgang.id).subscribe({
        next: data => {
          if (data) {
            this.digitalisatImages = data;
          }
        },
        error: error => {
          console.log(error);
          this.toasterNotificationService.showErrorMessage(error?.error?.message);
        }
      });
    }
  }

  downloadPdf(loadingModal: TemplateRef<any>, comment: MetadataCommentsViewComponent) {
    const modalOptions: ModalOptions = {
      backdrop : 'static',
      keyboard : false
    };
    const loadingPanel = this.modalService.show(loadingModal, modalOptions);
    this.vorgangService.downloadPdf(this.vorgang).subscribe({
      next: data => {
        const autoComment = `PDF download by ${this.currentUser?.username}`;
        const reference = `PDF ${this.vorgang.name}`;
        this.downloadFilePipe.transform(data, this.create_pdf_name());
        setTimeout(() => comment.addComment(autoComment, reference), 10);
      },
      error: error => {
        console.log(error);
        setTimeout(() => loadingPanel.hide(), 500)
      },
      complete: () => {setTimeout(() => loadingPanel.hide(), 500)}
    });
  }

  onScroll(e: any) {
    if (!this.singleImageView) {
      this.currentScrollTop = e.target.scrollTop;
    }
  }

  onChangeImageView(isSingleImageView: boolean) {
    if (!isSingleImageView) {
      //  must wait until images are repopulated to set scroll position.
      setTimeout(() => this.wrapImagesRef.nativeElement.scrollTop = this.currentScrollTop, 200);
    }
  }

}
