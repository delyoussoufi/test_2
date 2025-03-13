import {Component, EventEmitter, Input, OnInit, Output, TemplateRef} from '@angular/core';
import {DomSanitizer, SafeUrl} from '@angular/platform-browser';

import {map} from 'rxjs/operators';
import {Observable, of} from 'rxjs';

import {DigitalisatImage} from '../../../model/model.digitalisat-image';
import {ToasterNotificationService} from '../../../services/notification/toaster-notification.service';
import {DigitalisatService} from '../../../services/digitalisat/digitalisat.service';
import {SearchCategory} from '../../../model/model.search-category';
import {ImageGallery} from '../../../model/model.image-gallery';
import {ImageSelectEvent} from '../selectable-image/selectable-image.component';
import {ComponentUtils} from '../../component.utils';
import {BsModalService} from 'ngx-bootstrap/modal';
import {BsModalRef} from 'ngx-bootstrap/modal/bs-modal-ref.service';
import {FoundEntities} from '../../../model/model.found-entities';

@Component({
    selector: 'app-gallery-image-viewer',
    templateUrl: './gallery-image-viewer.component.html',
    styleUrls: ['./gallery-image-viewer.component.css'],
    standalone: false
})
export class GalleryImageViewerComponent extends ComponentUtils implements OnInit {
  @Input()
  set digitalisatImages(dims: DigitalisatImage[]) {
    this._digitalisatImages = dims ? dims : [];
    this.addImagesUrlObservables();
  }
  @Input()
  set selectable(isSelectable: boolean) {
    this._selectable = isSelectable;
    // this._selectedImages = isSelectable ? [...this.digitalisatImages] : []; // copy array
  }
  @Input()
  set selectedImages(img: DigitalisatImage[]) {
    this._selectedImages = img ? [...img] : []; // copy array
  }

  @Input()
  category: SearchCategory;
  @Input()
  disableCategoryFunctions = true;
  @Input()
  textSearch = '';
  @Input()
  singleImageView = false;

  @Output()
  singleImageViewChange = new EventEmitter<boolean>();

  @Output()
  addImageToCategory = new EventEmitter<DigitalisatImage>();
  @Output()
  removeImageFromCategory = new EventEmitter<DigitalisatImage>();
  @Output()
  selectedImagesChange = new EventEmitter<DigitalisatImage[]>();

  foundTermsObservable$: Observable<string[][]>;
  imageNers$: Observable<FoundEntities>;
  imagesUrls$: Array<Observable<SafeUrl>> = [];
  selectedImage: DigitalisatImage;
  selectedImageIdx: number;
  disableLeftArrow = false;
  disableRightArrow = false;
  zoomImage: {'image': DigitalisatImage, 'index': number};
  cleanText = true;

  private _selectable = false;
  private imageGallery: Array<ImageGallery> = [];
  private _digitalisatImages: DigitalisatImage[] = [];
  private _selectedImages: DigitalisatImage[] = [];
  private modalRef: BsModalRef | null;



  constructor(private toasterNotificationService: ToasterNotificationService, private sanitizer: DomSanitizer,
              private digitalisatService: DigitalisatService, private modalService: BsModalService) {
    super(toasterNotificationService);
  }

  ngOnInit(): void {}

  openModal(template: TemplateRef<any>, image: DigitalisatImage, index: number) {
    this.modalRef = this.modalService.show(template, { class: 'modal-lg' });
    this.zoomImage = {'image': image, 'index': index};
    this.setImageNers(image.id);

  }

  closeModal() {
    this.modalRef?.hide();
    this.zoomImage =  {'image': null, 'index': 0};
  }

  get digitalisatImages(): DigitalisatImage[] {
    return this._digitalisatImages;
  }

  get selectable(): boolean {
    return this._selectable;
  }

  private addImagesUrlObservables() {
    this.imagesUrls$ = []; // Cleanup Observables list.
    // We need to add it to a list otherwise calling `getImageFile$(image) | async` direct cause an infinity loop.
    this.digitalisatImages?.forEach(di => this.imagesUrls$.push(this.getImageFile$(di)));
  }

  getImageFile$(digitalisatImage: DigitalisatImage) {
    // check if the url was cached already and return an observable with it.
    const cachedUrl = this.getImageUrl(digitalisatImage);
    if (cachedUrl) {
      return of(cachedUrl);
    }

    // otherwise, make the call to the server.
    return this.digitalisatService.downloadImage(digitalisatImage.id).pipe(
      map(imageData => {
        if (imageData) {
          const url = this.sanitizer.bypassSecurityTrustUrl(URL.createObjectURL(imageData));
          const ig = new ImageGallery();
          ig.imageId = digitalisatImage.id;
          ig.url = url;
          this.imageGallery.push(ig);
          return url;
        }
        console.log('No image');
      })
    );

  }

  onLoadImage(img, idx) {
    const cachedUrl = this.getImageUrl(img);
    if (cachedUrl) {
      // replace call to backend to the cached URL.
      this.imagesUrls$[idx] = of(cachedUrl);
    }
  }

  isImageInCategory(image: DigitalisatImage): boolean {
    return image.categoriesIds.indexOf(this.category?.id) > -1;
  }

  setFoundTermsObservable(imageId: string): boolean {
    this.foundTermsObservable$ = this.digitalisatService.getFoundTerms(imageId, this.category?.id).pipe(
      map((data) => data.map(st => st.found_terms
        .filter((value, index, array) => array.map((ft) => ft.value).indexOf(value.value) === index)
        .map(v => v.value)))
    );
    return false; // necessary to avoid href to jump page.
  }

  getImageUrl(image: DigitalisatImage): SafeUrl {
    if (this.imageGallery) {
      const isFound = this.imageGallery.find(ig => ig.imageId === image?.id);
      if (isFound) {
        return isFound.url;
      }
    }
    return null;
  }

  onSelectImage(image: DigitalisatImage, idx: number) {
    this.selectedImage = image;
    this.selectedImageIdx = idx;
    this.singleImageView = image !== null;
    this.singleImageViewChange.emit(this.singleImageView);
    this.checkImageArrowRoulette(idx);
  }

  nextImage() {
    let index = this.digitalisatImages?.indexOf(this.selectedImage);
    // index = (index + 1 ) % this.digitalisatImages?.length;
    index = (index + 1 );
    this.checkImageArrowRoulette(index);
    if (index < this.digitalisatImages?.length) {
      this.selectedImage = this.digitalisatImages[index];
      this.selectedImageIdx = index;
    }
  }

  prevImage() {
    let index = this.digitalisatImages?.indexOf(this.selectedImage);
    // index = (index - 1 ) % this.digitalisatImages?.length;
    index = (index - 1 );
    this.checkImageArrowRoulette(index);
    if (index >= 0) {
      this.selectedImage = this.digitalisatImages[index];
      this.selectedImageIdx = index;
    }
  }

  checkImageArrowRoulette(index: number) {

    if (this.digitalisatImages?.length === 1) {
      this.disableRightArrow = true;
      this.disableLeftArrow = true;
      return;
    }

    if (index >= this.digitalisatImages?.length) {
      this.disableLeftArrow = false;
      this.disableRightArrow = true;
    } else if (index <= 0) {
      this.disableLeftArrow = true;
      this.disableRightArrow = false;
    } else {
      this.disableRightArrow = false;
      this.disableLeftArrow = false;
    }
  }

  isImageSelected(image: DigitalisatImage): boolean {
    return this._selectedImages.indexOf(image) > -1;
  }

  onSelectImagesChange(e: ImageSelectEvent) {
    const img = this._digitalisatImages.find( im => im.id === e.id);
    if (!img) { return; }

    if (e.selected) {
      this._selectedImages.push(img);
    } else {
      this.removeItemFromList(this._selectedImages, img);
    }
    this.selectedImagesChange.emit(this._selectedImages);
  }

  onCleanTextValueChange(e: boolean) {
    this.cleanText = e;
    this.setImageNers(this.zoomImage?.image.id);
  }

  setImageNers(imageId) {
    this.imageNers$ = this.digitalisatService.getImageNers(imageId, this.cleanText).pipe(
      map( data => {
        data.text = data.text.replace(/<|>/gi, ' ');
        let index = 0;
        let text = '';
        data.entities.forEach(v=> {
          // index += 1;
          const replace = '<span style="background-color: #17a2b8">' + v.value + ' ' + '<b>' + v.label + '</b>' + '</span>';
          text += data.text.substring(index, v.start) + replace;
          index = v.end
        })
        data.safeText = this.sanitizer.bypassSecurityTrustHtml(text);
        return data;

      })
    );
  }

}
