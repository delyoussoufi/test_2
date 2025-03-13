import {Component, ElementRef, OnInit, TemplateRef, ViewChild} from '@angular/core';
import {ActivatedRoute} from '@angular/router';

import {Observable} from 'rxjs';

import {BsModalService} from 'ngx-bootstrap/modal';
import {BsModalRef} from 'ngx-bootstrap/modal/bs-modal-ref.service';

import {ComponentUtils} from '../../component.utils';
import {ToasterNotificationService} from '../../../services/notification/toaster-notification.service';
import {DigitalisatService} from '../../../services/digitalisat/digitalisat.service';
import {Digitalisat} from '../../../model/model.digitalisat';
import {SearchCategoryService} from '../../../services/search-category/search-category.service';
import {SearchCategory} from '../../../model/model.search-category';
import {DigitalisatImage} from '../../../model/model.digitalisat-image';
import {VorgangService} from '../../../services/vorgang/vorgang.service';
import {ClassificationStatusKeyBind, EnumClassificationStatus} from '../../../enums/enum.digitalisat-working-status';
import {ClassificationStatus} from '../../../model/model.classification-status';
import {DigitalisatClassificationUtils} from '../../../statics/digitalisat-classification-utils';


@Component({
    selector: 'app-digitalisat-edit',
    templateUrl: './digitalisat-edit.component.html',
    styleUrls: ['./digitalisat-edit.component.css'],
    standalone: false
})
export class DigitalisatEditComponent extends ComponentUtils implements OnInit {

  @ViewChild('wrapImages', {static: true}) wrapImagesRef: ElementRef<HTMLCanvasElement>;


  digitalisat: Digitalisat;
  digitalisatImages: Array<DigitalisatImage> = [];
  digitalisatSelectedImages: Array<DigitalisatImage> = [];
  category: SearchCategory;
  categories$: Observable<Array<SearchCategory>>;
  singleImageView = false;
  selectedImageCategory: DigitalisatImage;
  shouldAddImageToCategory = false;
  isSavingVorgang = false;
  isCreatingVorgang = false;
  showAllImages = false;
  fetchingImages = false;
  textSearch = '';
  disableCategoryFunctions = true;
  enumClassificationStatus = EnumClassificationStatus;
  classificationStatusKeyBind = ClassificationStatusKeyBind;
  imageCategoryModalRef: BsModalRef | null;
  modalRef: BsModalRef | null;

  currentScrollTop = 0;
  private imagesToRemoveFromView: Array<DigitalisatImage> = [];

  constructor(private route: ActivatedRoute, private digitalisatService: DigitalisatService, private vorgangService: VorgangService,
              private searchCategoryService: SearchCategoryService,  private modalService: BsModalService,
              private toasterNotificationService: ToasterNotificationService) {
    super(toasterNotificationService);
    this.categories$ = this.searchCategoryService.all();
    this.route.params.subscribe(params => {
      this.textSearch = this.route.snapshot.queryParamMap.get('text_search') || '';
      if (params && params.id) {
        this.digitalisatService.get(params.id).subscribe(
          digitalisat => {
            this.digitalisat = digitalisat;
          },
          error => {
            console.log(error);
            this.toasterNotificationService.showErrorMessage(error.message.error);
          }
        );
      }
      if (params && params.categoryId) {
        this.searchCategoryService.get(params.categoryId).subscribe(
          data => {
            this.category = data;
            this.disableCategoryFunctions = this.category?.name === 'Unclassified';
            this.showAllImages = this.disableCategoryFunctions;
            this.searchImages();
          },
          error => {
            console.log(error);
            this.toasterNotificationService.showErrorMessage(error.message.error);
          }
        );
      } else {
        this.showAllImages = true;
        this.searchImages();
      }
    });
  }

  ngOnInit(): void {}

  searchImages() {
    if (this.showAllImages) {
      this.searchAllImages();
    } else {
      this.searchImagesWithCategory();
    }
  }

  searchImagesWithCategory() {
    if (this.digitalisat?.id && this.category?.id) {
      this.fetchingImages = true;
      this.digitalisatService.getImagesFromDigitalisatAndCategory(this.digitalisat.id, this.category.id, this.textSearch).subscribe(
        data => {
          this.singleImageView = false;
          this.digitalisatImages = data ? data : [];
          this.fetchingImages = false;
        }, error => {
          this.fetchingImages = false;
          console.log(error);
          this.toasterNotificationService.showErrorMessage(error?.error?.message);
        }
      );
    } else {
      setTimeout(() => this.searchImagesWithCategory(), 10);
    }
  }

  searchAllImages() {
    if (this.digitalisat?.id) {
      this.fetchingImages = true;

      this.digitalisatService.getImagesFromDigitalisat(this.digitalisat.id, this.textSearch).subscribe(
        data => {
          if (data) {
            this.singleImageView = false;
            this.digitalisatImages = data;
          }
          this.fetchingImages = false;
          // console.log(data);
        }, error => {
          this.fetchingImages = false;
          console.log(error);
          this.toasterNotificationService.showErrorMessage(error?.error?.message);
        }
      );
    } else {
      setTimeout(() => this.searchAllImages(), 10);
    }
  }

  selectedImagesChange(images: DigitalisatImage[]) {
    this.digitalisatSelectedImages = [...images];
  }

  onCreateVorgangClick() {
    this.isCreatingVorgang = !this.isCreatingVorgang;
    this.digitalisatSelectedImages = this.isCreatingVorgang ? [...this.digitalisatImages] : [];
    if (!this.isCreatingVorgang) {
      this.onChangeImageView(this.singleImageView);
    }
  }

  saveVorgang() {
    if (!this.digitalisatSelectedImages || this.digitalisatSelectedImages?.length === 0) {
      this.toasterNotificationService.showErrorMessage('Sie müssen mindestens ein Bild auswählen, um einen Vorgang zu erstellen');
      return;
    }
    this.isSavingVorgang = true;
    this.vorgangService.create(this.category.id, this.digitalisat.id, this.digitalisatSelectedImages).subscribe(
      data => {
        if (data) {
          this.toasterNotificationService.showSuccessMessage('Gerettet');
        } else {
          this.toasterNotificationService.showErrorMessage('Vorgang konnte nicht erstellt werden');
        }
      }
      ,
      error => {
        this.isSavingVorgang = false;
        console.log(error);
        this.toasterNotificationService.showErrorMessage(error.error?.message);
      },
      () => {
        this.onCreateVorgangClick();
        this.isSavingVorgang = false;
      }
    );
  }

  updateDigitalisate() {
    this.digitalisatService.get(this.digitalisat.id).subscribe(
      digitalist => {
        this.digitalisat = digitalist;
      });
  }

  hasCategory(category: SearchCategory): boolean {
    return this.digitalisat?.classificationStatus.findIndex(cs => cs.searchCategoryId === category?.id) > -1;
  }

  isImageInCategory(image: DigitalisatImage): boolean {
    return image.categoriesIds.indexOf(this.category?.id) > -1;
  }

  hasImagesInCategory(): boolean {
    return this.digitalisatImages?.findIndex(img => this.isImageInCategory(img)) > -1;
  }

  openModal(template: TemplateRef<any>) {
    this.modalRef = this.modalService.show(template);
  }

  closeModal() {
    this.modalRef?.hide();
    this.modalRef = null;
  }

  openImageCategoryModal(template: TemplateRef<any>, image: DigitalisatImage, should_add: boolean) {
    this.shouldAddImageToCategory = should_add;
    this.imageCategoryModalRef = this.modalService.show(template);
    this.selectedImageCategory = image;
  }

  closeImageCategoryModal() {
    this.selectedImageCategory = null;
    this.imageCategoryModalRef?.hide();
  }

  addImageToCategory(image: DigitalisatImage) {
    this.digitalisatService.addFileToClassification(image.id, this.category.id).subscribe(
      (result) => {
        if (result) {
          image.categoriesIds.push(this.category.id);
          this.removeItemFromList(this.imagesToRemoveFromView, image);
        } else {
          this.toasterNotificationService.showErrorMessage('Cant add');
        }
      }
    );
    this.closeImageCategoryModal();
  }

  removeDigitalisateFilesFromClassification() {
    if (!this.digitalisat && !this.category) { return; }
    this.digitalisatService.removeDigitalisateFilesFromClassification(this.digitalisat.id, this.category.id).subscribe(
      (result) => {
        if (result) {
          this.updateDigitalisate();
          this.searchImages();
        } else {
          this.toasterNotificationService.showErrorMessage('Cant delete');
        }
      }
    );
    this.closeModal();
  }

  removeImageFromCategory(image: DigitalisatImage) {
    this.digitalisatService.removeImageFromCategory(image.id, this.category.id).subscribe(
      (result) => {
        if (result) {
          if (this.showAllImages) {
            // if showAllImages is true then remove the category from image category list
            this.removeItemFromList(image.categoriesIds, this.category.id);
          } else {
            if (this.singleImageView) {
              // remove from category.
              this.removeItemFromList(image.categoriesIds, this.category.id);
              // cache images to be removed when view changes.
              this.imagesToRemoveFromView.push(image);
            } else {
              // otherwise, remove it from list of images.
              this.removeItemFromList(this.digitalisatImages, image);
            }
          }
          if (this.digitalisatImages.filter(img => this.isImageInCategory(img)).length === 0) {
            this.updateDigitalisate();
          }
        } else {
          this.toasterNotificationService.showErrorMessage('Cant delete');
        }
      }
    );
    this.closeImageCategoryModal();
  }

  getClassificationStatus(digitalisat: Digitalisat): ClassificationStatus {
    return DigitalisatClassificationUtils.getClassificationStatus(digitalisat, this.category);
  }

  onChangeWorkingStatus(e) {
    this.digitalisatService.changeClassificationStatus(this.digitalisat.id, this.category.id, e).subscribe(
      (saved) => {
        if (!saved) {
          this.toasterNotificationService.showErrorMessage('Fail to change working status');
        }
      }
    );
  }

  onOwnerSwitchValueChange(status: boolean) {
    this.digitalisatService.changeClassificationOwnership(this.digitalisat.id, this.category.id, status).subscribe();
  }

  onLocationSwitchValueChange(status: boolean) {
    this.digitalisatService.changeClassificationLocation(this.digitalisat.id, this.category.id, status).subscribe();
  }

  isLocked() {
    const index = this.digitalisat?.lockedCategories.findIndex(l => l.id === this.category?.id);
    // If an index is found then digitalisat is locked for this category
    return index > -1;
  }

  unlockClassificationFromDigitalisat() {
    this.digitalisatService.unlockDigitalisatClassification(this.digitalisat.id, this.category.id).subscribe(
      digitalisat => {
        if (digitalisat) {
          this.digitalisat.lockedCategories = digitalisat.lockedCategories;
          this.showSuccessMessage(this.category.name + ' was unlock from ' + digitalisat?.signature);
        } else {
          this.showErrorMessage('Fail to unlock ' + this.category.name);
        }
      }
    );
  }

  onScroll(e) {
    if (!this.singleImageView && !this.isCreatingVorgang) {
      this.currentScrollTop = e.target.scrollTop;
    }
  }

  onChangeImageView(isSingleImageView) {
    if (!isSingleImageView) {
      this.imagesToRemoveFromView.forEach( i =>  this.removeItemFromList(this.digitalisatImages, i));
      this.imagesToRemoveFromView = [];
      //  must wait until images are repopulated to set scroll position.
      this.moveScroll(this.currentScrollTop, 2);
    }
  }

  moveScroll(target: number, bounce: number, timeout = 1000 ) {
    const startedAt = Date.now();
    const timerId = setInterval(() => {
      this.wrapImagesRef.nativeElement.scrollTo( {
        top: target,
        behavior: 'auto'
      });
      const resultantScrollTop = this.wrapImagesRef.nativeElement.scrollTop;

      if (Date.now() - startedAt > timeout) {
        clearInterval(timerId);
      }

      if (resultantScrollTop === target) {
        clearInterval(timerId);
        // reinforce the position. Check again to see if scroll didn't move.
        setTimeout(() => {
          if (this.wrapImagesRef.nativeElement.scrollTop !== target) {
            this.moveScroll(target, 5, 100);
          }
        }, 200);
      }
    }, bounce);
  }
}
