import {Search} from './model.search';

export interface IScopeMetadataSearch {
  title: string;
  geburtsname: string;
  wohnort: string;
  registrySignature: string;
  associates: string;
  laufzeit: string;
  startSignature: number;
  endSignature: number;
  comments: string,
}

export class DigitalisatSearch extends Search {
  classificationStatusId: string;
  status = 'FINISHED';
  classificationStatus: string;
  textSearch: string;
  metadata: IScopeMetadataSearch = { title: '', geburtsname: '', wohnort: '', registrySignature: '', associates: '', laufzeit: '',
   startSignature: 0,  endSignature: 0, comments: ''};

  get isEmptyMetadata(): boolean {
    const emptyValues: Array<Object> = Object.keys(this.metadata).map(key => !this.metadata[key]);
    return emptyValues.every(v => v === true);
  }
}
