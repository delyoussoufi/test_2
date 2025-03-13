import {Component, OnInit} from '@angular/core';
import { HttpParams } from '@angular/common/http';

import {Observable} from 'rxjs';
import {map, mergeMap} from 'rxjs/operators';

import {TypeaheadMatch} from 'ngx-bootstrap/typeahead';
import {BsModalService} from 'ngx-bootstrap/modal';
import {BsModalRef} from 'ngx-bootstrap/modal/bs-modal-ref.service';

import {ConversionService} from '../../../services/conversion/conversion.service';
import {ToasterNotificationService} from '../../../services/notification/toaster-notification.service';
import {SearchBestand} from '../../../model/model.search-bestand';
import {SearchBestandComponent} from '../search-bestand.component';
import {SearchBestandService} from '../../../services/search-bestand/search-bestand.service';
import {DigiConnectionService} from '../../../services/digi-connection/digi-connection.service';

@Component({
    selector: 'app-search-bestand-create',
    templateUrl: './search-bestand-create.component.html',
    styleUrls: ['./search-bestand-create.component.css'],
    standalone: false
})
export class SearchBestandCreateComponent extends SearchBestandComponent implements OnInit {

  addSearchTermError = '';
  addSearchTermModalRef: BsModalRef;
  bestandDataSource: Observable<any>;
  bestandTypeaheadLoading = true;
  selectedBestand: SearchBestand = new SearchBestand();

  constructor(private conversionService: ConversionService, private digiConnectionService: DigiConnectionService,
              private searchBestandService: SearchBestandService, private modalService: BsModalService,
              private toasterNotificationService: ToasterNotificationService) {
    super(modalService, toasterNotificationService);
    // Serach for Bestände
    this.bestandDataSource = Observable.create((observer: any) => {
      // Runs on every search
      observer.next(this.selectedBestand.name);
    }).pipe(
      mergeMap((term: string) => digiConnectionService.searchBestaende(this.buildQueryParams(term)).pipe(
        // Map search result observable to result list.
        map((data: any) => {
          // console.log(data);
          return data.resultList;
        }))
      )
    );
  }

  private buildQueryParams(name: string, operator: string = 'CONTAINS'): HttpParams {
    const params = {};
    params['orderBy'] = 'name';
    params['orderDirection'] = 'ASC';
    if (name) {
      params['name'] = name.trim();
    }
    params['operator'] = operator;
    params['firstResult'] = 0;
    params['maxResults'] = 10;
    return new HttpParams({ fromObject: params });
  }

  ngOnInit() {
  }

  createSearchBestand() {

    this.searchBestandService.create(this.selectedBestand).subscribe(
      data => {
        this.selectedBestand = new SearchBestand();
        super.showSuccessMessage('Suchbestand wurde erstellt.');
      },
      error => {
        if (error.error && error.error.message) {
          super.showErrorMessage(error.error.message);
        } else {
          super.showErrorMessage('Suchbestand konnte nicht erstellt werden.');
        }
        console.log(error);
      }
    );
  }

  changeTypeaheadLoading(e: boolean): void {
    this.bestandTypeaheadLoading = e;
  }

  typeaheadOnSelect(e: TypeaheadMatch): void {
    // console.log('Selected value: ', e.value);
    this.findBestand(e.value);
  }

  // TODO Change it to get Bestand using Id
  private findBestand(name: string) {
    this.digiConnectionService.searchBestaende(this.buildQueryParams(name, 'EQUAL')).subscribe(
      data => {
        if (data.resultList && data.resultList.length === 1) {
          this.selectedBestand = data.resultList[0];
        } else {
          this.toasterNotificationService.showErrorMessage('Bestand konnte nicht ausgewählt werden.');
        }
      }
    );
  }

}
