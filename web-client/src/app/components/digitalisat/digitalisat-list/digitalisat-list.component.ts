import {Component, OnInit, TemplateRef} from '@angular/core';
import { HttpParams } from '@angular/common/http';
import {ActivatedRoute, Params, Router} from '@angular/router';

import {BsModalService} from 'ngx-bootstrap/modal';
import {BsModalRef} from 'ngx-bootstrap/modal/bs-modal-ref.service';

import {Observable} from 'rxjs';
import {Digitalisat} from '../../../model/model.digitalisat';
import {DigitalisatService} from '../../../services/digitalisat/digitalisat.service';
import {ToasterNotificationService} from '../../../services/notification/toaster-notification.service';
import {ComponentUtils} from '../../component.utils';
import {SearchCategoryService} from '../../../services/search-category/search-category.service';
import {SearchCategory} from '../../../model/model.search-category';
import {ClassificationStatus} from '../../../model/model.classification-status';
import {DigitalisatSearch} from '../../../model/model.digitalisat-search';
import {
  CassificationStatusStrings,
  ClassificationStatusKeyBind,
  EnumClassificationStatus
} from '../../../enums/enum.digitalisat-working-status';
import {DigitalisatClassificationUtils} from '../../../statics/digitalisat-classification-utils';
import {map} from 'rxjs/operators';
import {DigitalisatQueryExportComponent} from "../digitalisat-query-export/digitalisat-query-export.component";


interface SearchOptions {
  queryParams: HttpParams;
  movePage: boolean;
  orderBy: string;
}

@Component({
    selector: 'app-digitalisat-list',
    templateUrl: './digitalisat-list.component.html',
    styleUrls: ['./digitalisat-list.component.css'],
    standalone: false
})
export class DigitalisatListComponent extends ComponentUtils implements OnInit {

  searchParams: DigitalisatSearch = new DigitalisatSearch();
  enumClassificationStatus = EnumClassificationStatus;
  classificationStatusKeyBind = ClassificationStatusKeyBind;
  searchCategories$: Observable<SearchCategory[]> | undefined;

  searchCategoriesWithoutDefault$: Observable<Array<SearchCategory>>;
  selectedSearchCategory: SearchCategory = null;
  selectedSearchCategoryReclassify: SearchCategory = null;
  selectedWorkingStatus: ClassificationStatusKeyBind = null;
  orderBy = 'title';
  orderDesc = false;
  isCollapsed = true;
  page = 1;
  itemsPerPage = 10;
  totalItems = 0;
  manualPageSelected = 1;

  reclassifyModalRef: BsModalRef | null;
  reclassifyDigitalisat: Digitalisat;

  private blockSearchOnPageChange = false;
  protected searchCategories: SearchCategory[] = [];
  protected digitalisate: Digitalisat[] = [];
  protected isLoading: boolean = true;



  constructor(private digitalisatService: DigitalisatService,
              private modalService: BsModalService, private searchCategoryService: SearchCategoryService,
              private toasterNotificationService: ToasterNotificationService, private _router: Router, private _route: ActivatedRoute) {
    super(toasterNotificationService);
    this.searchCategories$ = this.searchCategoryService.all().pipe(
      map( (data) => {
        this.searchCategories = data;
        this.searchFromUrlParams();
        return this.searchCategories;
      })
    );
    this.searchCategoriesWithoutDefault$ = this.searchCategoryService.all(true);
  }

  ngOnInit() {}

  get maxPage(): number {
    return Math.max(Math.ceil(this.totalItems / this.itemsPerPage), 1);
  }

  bindValuesFromUrlParams(params: Params) {
    this.selectedSearchCategory = this.searchCategories?.find(sc => sc.id === params.classificationStatusId);
    this.selectedWorkingStatus = this.classificationStatusKeyBind.getWorkingStatusKey(params?.classificationStatus);
    if (params?.orderDesc) {
      this.orderDesc = JSON.parse(params?.orderDesc);
    }
    this.itemsPerPage = params?.perPage ? +params.perPage : this.itemsPerPage;
    this.manualPageSelected = params?.page ? +params?.page : this.page;
    // setTimeout(() => this.setPage(params?.page ? +params?.page : this.page), 500);
    this.searchParams.textSearch = params?.textSearch ? params.textSearch : '';
    this.searchParams.orderBy = params?.orderBy ? params.orderBy : this.orderBy;
    this.orderBy = this.searchParams.orderBy;
    // bind scope metadata
    if (params?.metadata) {
      this.searchParams.metadata = JSON.parse(params.metadata);
      this.isCollapsed = this.searchParams.isEmptyMetadata;
    }
  }

  searchFromUrlParams() {
    const params = this._route?.snapshot?.queryParams;
    this.bindValuesFromUrlParams(params);
    const httpParams = new HttpParams({ fromObject: params });
    if (params && Object.keys(params).length > 0) {
      this._search({queryParams: httpParams, movePage: true, orderBy: this.orderBy});
    } else {
      this._search({queryParams: httpParams, movePage: false, orderBy: null});
    }
  }

  addParamToUrl(params: {}) {
    this._router.navigate([], {
      relativeTo: this._route,
      queryParams: params,
      // preserve the existing query params in the route
      queryParamsHandling: 'merge'
    }).then();
  }

  onChangeSearchCategory(selectedSearchCategory: SearchCategory) {
    if (!selectedSearchCategory) {
      this.selectedWorkingStatus = null;  // set selectedWorkingStatus to null since it makes no sense  to search it without category.
    }
    this.search();
  }

  onChangeWorkingStatus(key: CassificationStatusStrings) {
    if (key) {
      this.selectedWorkingStatus = key;
    } else {
      this.selectedWorkingStatus = null;
    }
    this.search();
  }

  collapse() {
    this.isCollapsed = !this.isCollapsed;
  }

  setPage(page: number, delay= 0, blockSearch= false) {
    setTimeout(() => {
      this.blockSearchOnPageChange = blockSearch;
      setTimeout( () => this.blockSearchOnPageChange = false, 5);
      this.page = Math.floor(+page);
      this.manualPageSelected = this.page;
    }, delay);
  }

  pageChanged(event: any) {
    this.page = event.page;
    this.manualPageSelected = this.page;
    if (!this.blockSearchOnPageChange) {
      this._search();
    }
  }

  itemsPerPageChanged(itemsPerPage: number) {
    this.setPage(1, 0, true);
    setTimeout(() => {
      this.itemsPerPage = itemsPerPage;
      this._search();
    }, 2);

  }

  buildQueryParams(page: number, orderBy: string, pageSize?: number): HttpParams {

    if (this.orderBy && this.orderBy === orderBy) {
      this.orderDesc = !this.orderDesc;
    }
    if (orderBy) {
      this.orderBy = orderBy;
    }

    this.searchParams.page = page;
    this.searchParams.perPage = pageSize ? pageSize : this.itemsPerPage;
    this.searchParams.orderBy = this.orderBy;
    this.searchParams.orderDesc = this.orderDesc;
    this.searchParams.searchBy = 'status:==';
    this.searchParams.searchValue = [this.searchParams.status];
    this.searchParams.classificationStatusId = this.selectedSearchCategory?.id ? this.selectedSearchCategory?.id : null;
    this.searchParams.classificationStatus = this.selectedWorkingStatus?.toString() ? this.selectedWorkingStatus?.toString() : null;
    const params = this.searchParams.toDict();
    this.addParamToUrl(params);

    return new HttpParams({ fromObject: params });
  }

  public export_search(exportQueryRef: DigitalisatQueryExportComponent) {
    exportQueryRef.fetchFileService$ = this.digitalisatService.export_search(this.buildQueryParams(this.page, null));
    exportQueryRef.openModal();
  }

  public search(){
    this.setPage(1, 0, true);
    setTimeout(() => {
      this._search();
    }, 2);
  }

  protected _search(options: SearchOptions = {queryParams: null, movePage: false, orderBy: null}) {

    const queryParams = options.queryParams?.has('status') ? options.queryParams : this.buildQueryParams(this.page, options.orderBy);
    this.isLoading=true;

    this.digitalisatService.search(queryParams).subscribe({
      next: data => {
        this.digitalisate = data.resultList;
        this.totalItems = data.totalCount;
        if (options.movePage && queryParams?.has('page')) {
          this.setPage(+queryParams.get('page'), 100, true);
        }
        this.isLoading=false;
      },
      error: error => {
        this.isLoading=false;
        console.log(error);
      }
    });
  }

  sort(orderBy: string, options: SearchOptions = {queryParams: null, movePage: false, orderBy: null}) {
    options.orderBy = orderBy;
    this._search(options);
  }

  getClassificationStatus(digitalisat: Digitalisat): ClassificationStatus {
    return DigitalisatClassificationUtils.getClassificationStatus(digitalisat, this.selectedSearchCategory);
  }

  getClassificationStatusStyle(digitalisat: Digitalisat) {
    return DigitalisatClassificationUtils.getClassificationStatusStyle(digitalisat, this.selectedSearchCategory);
  }

  getClassificationStatusValue(digitalisat: Digitalisat) {
    return DigitalisatClassificationUtils.getClassificationStatusValue(digitalisat, this.selectedSearchCategory);
  }

  openReclassifyModal(template: TemplateRef<any>, digitalisat: Digitalisat) {
    this.reclassifyModalRef = this.modalService.show(template);
    this.reclassifyDigitalisat = digitalisat;

  }

  closeReclassifyModal() {
    this.reclassifyModalRef?.hide();
    this.reclassifyDigitalisat = null;
    this.selectedSearchCategoryReclassify = null;
    this.reclassifyModalRef = null;
  }

  reclassify() {
    if (this.reclassifyDigitalisat) {
      const index = this.digitalisate.indexOf(this.reclassifyDigitalisat);
      this.reclassifyDigitalisat.status = 'CLASSIFYING';
      const categoryId = this.selectedSearchCategoryReclassify?.id;
      this.digitalisatService.reclassifyDigitalisat(this.reclassifyDigitalisat.id, categoryId).subscribe(
        {
          next: digitalisat => {
            if (index > -1 && digitalisat) {
              this.digitalisate[index] = digitalisat;
              this.toasterNotificationService.showSuccessMessage('Reclassification successfully done');
            }
            this.closeReclassifyModal();
          },
          error: error => {
            this.toasterNotificationService.showErrorMessage(error.error?.message);
            this.closeReclassifyModal();
          }
        });
    }
  }

  unlockClassificationFromDigitalisat(digitalisatId: string, searchCategory: SearchCategory) {
    this.digitalisatService.unlockDigitalisatClassification(digitalisatId, searchCategory.id).subscribe(
      digitalisat => {
        if (digitalisat) {
          const index = this.digitalisate.findIndex(d => d.id === digitalisat.id);
          if (index > -1) {
            this.digitalisate[index].lockedCategories = digitalisat.lockedCategories;
          }
          this.showSuccessMessage(searchCategory.name + ' was unlock from ' + digitalisat?.signature);
        } else {
          this.showErrorMessage('Fail to unlock ' + searchCategory.name);
        }
      }
    );
  }

}
