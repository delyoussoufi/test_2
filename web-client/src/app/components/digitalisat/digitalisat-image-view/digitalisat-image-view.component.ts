import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {DomSanitizer, SafeUrl} from '@angular/platform-browser';

import {ComponentUtils} from '../../component.utils';
import {DigitalisatService} from '../../../services/digitalisat/digitalisat.service';
import {SearchCategoryService} from '../../../services/search-category/search-category.service';
import {ToasterNotificationService} from '../../../services/notification/toaster-notification.service';
import {OcrData, SearchTermsFound} from '../../../model/model.ocr-data';
import {SearchCategory} from '../../../model/model.search-category';
import {DigitalisatImage} from '../../../model/model.digitalisat-image';


@Component({
    selector: 'app-digitalisat-image-view',
    templateUrl: './digitalisat-image-view.component.html',
    styleUrls: ['./digitalisat-image-view.component.css'],
    standalone: false
})
export class DigitalisatImageViewComponent extends ComponentUtils implements OnInit  {

  @Input() imageName: string;
  @Input() selectedWord = '';
  @Input() category: SearchCategory;
  @Input() disableLeftArrow = false;
  @Input() disableRightArrow = false;
  @Input() enableCategoryFunction = false;
  @Input() set imageUrl(value: string | SafeUrl) {
    setTimeout(() => this.imageSrc = value, 0);
  }
  @Input() set image (value: DigitalisatImage) {
    this._image = value;
    this._imageId = value?.id;
    if (this._imageId) {
      this.fetchOcrData();
      // this.fetchFoundTerms();
    }
  }

  @Output()
  nextImage = new EventEmitter();

  @Output()
  prevImage = new EventEmitter();

  @Output()
  imageLoaded = new EventEmitter();

  @Output()
  addImageToCategory = new EventEmitter<DigitalisatImage>();

  @Output()
  removeImageFromCategory = new EventEmitter<DigitalisatImage>();

  imageSrc: string | SafeUrl;
  nextArrowLocation = 100;
  private _imageId: string;
  private _image: DigitalisatImage;
  ocrData: OcrData;
  searchTermsFound: Array<SearchTermsFound>;

  constructor(private digitalisatService: DigitalisatService,  private sanitizer: DomSanitizer,
              private searchCategoryService: SearchCategoryService, private toasterNotificationService: ToasterNotificationService) {
    super(toasterNotificationService);
  }

  ngOnInit(): void {}

  get imageId(): string {
    return this._imageId;
  }

  get image(): DigitalisatImage {
    return this._image;
  }

  fetchOcrData() {
    this.digitalisatService.getOcrData(this._imageId).subscribe(
      data => {
        this.ocrData = data;
        this.fetchFoundTerms(); // get found terms only after ocr data
      }, error => {
        console.log(error);
        this.toasterNotificationService.showErrorMessage(error.error.message);
      }
    );
  }

  fetchFoundTerms() {
    if (this.category?.id) {
      this.digitalisatService.getFoundTerms(this._imageId, this.category?.id).subscribe(
        data => {
          this.searchTermsFound = data;
        }, error => {
          console.log(error);
          this.toasterNotificationService.showErrorMessage(error.error.message);
        }
      );
    } else {
      setTimeout(() => this.fetchFoundTerms(), 10);
    }

  }

  onImageLoaded(e) {
    this.nextArrowLocation = e.width + 27;
    this.imageLoaded.emit();
  }

  isImageInCategory(): boolean {
    return this.image.categoriesIds.indexOf(this.category?.id) > -1;
  }
}
