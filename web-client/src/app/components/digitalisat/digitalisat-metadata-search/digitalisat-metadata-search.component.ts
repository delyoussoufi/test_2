import {Component, EventEmitter, Input, OnInit, Output, SecurityContext} from '@angular/core';
import {DomSanitizer} from '@angular/platform-browser';

import {IScopeMetadataSearch} from '../../../model/model.digitalisat-search';
import {ToasterNotificationService} from '../../../services/notification/toaster-notification.service';

class FilterAlias {
  aliasName: string;
  mapName: string;
  valueType: string;
  shouldDisplay: boolean;
  operationSymbol: string;
  helpText: string;

  constructor(aliasName: string, mapName: string, valueType: string, shouldDisplay= true, operationSymbol= ':',
              helpText= '') {
    this.aliasName = aliasName;
    this.mapName = mapName;
    this.valueType = valueType;
    this.shouldDisplay = shouldDisplay;
    this.operationSymbol = operationSymbol;
    this.helpText = helpText;
  }
}
@Component({
    selector: 'app-digitalisat-metadata-search',
    templateUrl: './digitalisat-metadata-search.component.html',
    styleUrls: ['./digitalisat-metadata-search.component.css'],
    standalone: false
})
export class DigitalisatMetadataSearchComponent implements OnInit {

  @Input()
  metaFilter: IScopeMetadataSearch = { title: '', geburtsname: '', wohnort: '', registrySignature: '',
    associates: '', laufzeit: '', startSignature: 0, endSignature: 0, comments: ''};
  @Output()
  metaFilterChange = new EventEmitter<IScopeMetadataSearch>();

  @Output()
  search = new EventEmitter();

  // A list of tuple. The first value is a display value the second should match an IScopeMetadataSearch key.
  private filtersAlias: FilterAlias[] = [];

  filtersAliasDisplay: FilterAlias[] = [];

  value: string;

  filterPlaceholder = new FilterAlias('Filter', 'Filter', 'text');

  selectedFilter: FilterAlias = this.filterPlaceholder;  // start value as placeholder.

  constructor(private toasterNotificationService: ToasterNotificationService,  private sanitizer: DomSanitizer ) {
    this.construct_filters();
    this.filtersAliasDisplay = this.filtersAlias.filter(alias => alias.shouldDisplay);
  }

  ngOnInit(): void {}

  private construct_filters() {
    const full_text_helper = this.sanitize(
      '<span>Fulltext search examples: Han<b>*</b>, Hans <b>&</b> Feist, Hans <b><-></b> Feist, Ha<b>* <-></b> Fe<b>*</b></span>');
    this.filtersAlias = [
      new FilterAlias('Signature', 'endSignature', 'number', false, ' <='),
      new FilterAlias('Signature', 'startSignature', 'number', false, ' >='),
      new FilterAlias('Aktensignatur', 'mapSignature', 'text', true,
        ':', this.sanitize('<span>Zulässige Suchmuster: Einzelsignatur bspw. <b>12</b> (sucht nur Signatur 12), ' +
          'Signaturbereich bspw. <b>10:500</b> (sucht von Signatur 10 bis Signatur 500)</span>')),
      new FilterAlias('Name', 'title', 'text', true,  ':', full_text_helper),
      new FilterAlias('Registratursignatur', 'registrySignature', 'text', true),
      new FilterAlias('Geburtsname', 'geburtsname', 'text', true),
      new FilterAlias('Wohnort', 'wohnort', 'text', true),
      new FilterAlias('Laufzeit', 'laufzeit', 'text', true),
      new FilterAlias('in Akte genannt', 'associates', 'text', true, ':',
        full_text_helper),
      new FilterAlias('Kommentare', 'comments', 'text', true),
    ];
  }

  private hasFilters(): boolean {
    const values = Object.keys(this.metaFilter).map(key => this.metaFilter[key]);
    for (const value of values) {
      if (value) {
        return true;
      }
    }
    return false;
  }

  onFilterChange(filter: FilterAlias) {
    this.value = null;
  }

  private getAliasFilter(key: string): FilterAlias {
    const _alias = this.filtersAlias.filter(alias => alias.mapName === key);
    return _alias[0];
  }

  getAliasFilterName(key: string): string {
    const f = this.getAliasFilter(key);
    return `${f?.aliasName}${f?.operationSymbol}`;
  }

  private castToNumber(v: string): number {
    const number = +v;
    if (number >= 0) {
      return number;
    } else {
      this.toasterNotificationService.showErrorMessage(`Value ${v} must be a number >= 0`);
      return 0;
    }
  }

  addFilter(key: string, value: string) {
    if (!this.value) {
      return;
    }

    if (key in this.metaFilter) {
      this.metaFilter[key] = value;
      this.metaFilterChange.emit(this.metaFilter);
    } else if (key === 'mapSignature') {
      const values = this.value.toString().trim().split(':');
      if (values.length > 1) {
        if (+values[0] > +values[1] && +values[1] > 0) {
          this.toasterNotificationService.showErrorMessage(`${values[0]} must be <= than ${values[1]}`);
          return;
        }
        this.metaFilter.startSignature = this.castToNumber(values[0]);
        this.metaFilter.endSignature = this.castToNumber(values[1]);
      } else {
        this.metaFilter.startSignature = this.castToNumber(values[0]);
        this.metaFilter.endSignature = this.metaFilter.startSignature;
      }
      this.metaFilterChange.emit(this.metaFilter);
    }
  }

  removeFilter(key: string, emitSearchOnEmpty= true) {
    if (key in this.metaFilter) {
      this.metaFilter[key] = null;
      this.value = null;
      this.metaFilterChange.emit(this.metaFilter);
    }
    if (!this.hasFilters() && emitSearchOnEmpty) {
      this.search.emit();
    }
  }

  onSearch() {
    this.addFilter(this.selectedFilter.mapName, this.value);
    this.search.emit();
  }

  cleanFilters() {
    this.filtersAlias.forEach((alias) => this.removeFilter(alias.mapName, false));
    this.value = '';
    this.selectedFilter = this.filterPlaceholder;
    this.search.emit();
  }

  sanitize(str: string) {
    return this.sanitizer.sanitize(SecurityContext.HTML, str);
  }

}
