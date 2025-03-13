import {Digitalisat} from './model.digitalisat';
import {SearchCategory} from './model.search-category';

export class Vorgang {

  id: string;
  name: string;
  createDate: string;
  digitalisat: Digitalisat;
  searchCategory: SearchCategory;
}
