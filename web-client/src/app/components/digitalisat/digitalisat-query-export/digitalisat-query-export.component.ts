import {AfterContentInit, Component, inject, Input, TemplateRef, ViewChild} from '@angular/core';
import {BsModalService, ModalDirective, ModalModule} from "ngx-bootstrap/modal";
import {BsModalRef} from "ngx-bootstrap/modal/bs-modal-ref.service";
import {Observable} from "rxjs";
import {DownloadFilePipe} from "../../../pipes/download-file-pipe";

@Component({
    selector: 'app-digitalisat-query-export',
    imports: [ModalModule],
    providers: [DownloadFilePipe],
    templateUrl: './digitalisat-query-export.component.html',
    styleUrl: './digitalisat-query-export.component.css'
})
export class DigitalisatQueryExportComponent implements AfterContentInit {

  @ViewChild('queryExportTemplate') public template: TemplateRef<any>;

  @Input()
  fileName = "query-export.xlsx";

  @Input()
  modalTitle = 'Query Exportieren';

  public fetchFileService$: Observable<Blob>;
  private modalService = inject(BsModalService);
  private downloadFilePipe = inject(DownloadFilePipe);
  protected modalRef: BsModalRef | null;

  constructor() {}

  ngAfterContentInit(): void {}

  openModal() {
    this.modalRef = this.modalService.show(this.template);
  }

  close() {
    this.modalRef?.hide();
  }

  protected exportQuery(loadingDirective: ModalDirective) {
    loadingDirective.show();
    this.close();

    this.fetchFileService$?.subscribe({
      next: data => {
        loadingDirective.hide();
        this.downloadFilePipe.transform(data, this.fileName);
      },
      error: error => {
        console.log(error);
        loadingDirective.hide();
      }
    });
  }

}
