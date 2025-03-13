// This class should be equal to DigitalisatModel at the Python side.
import {ScopeData} from './model.scope-data';
import {ClassificationStatus} from './model.classification-status';
import {SearchCategory} from './model.search-category';

export class Digitalisat {

  id: string;
  scopeId: string;
  folderName: string;
  signature: string;
  targetFolderId: string;
  subFolder: number;
  expectedImages: number;
  numberOfImages: number;
  status: string; // DigitalisatStatus
  statusValue: string;
  createDate: string;
  deleteDate: string;
  scopeData: ScopeData; // ScopeDataModel
  classificationStatus: Array<ClassificationStatus>; //
  lockedCategories: Array<SearchCategory>; //
}
