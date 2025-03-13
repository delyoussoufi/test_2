import {Search} from './model.search';

export class SearchCategorySearch extends Search {
  name = ' ';
  description = ' ';

  constructor() {
    super();
  }

  public toDict() {
    const params = super.toDict();
    // remove keys from dict
    delete params['name'];
    delete params['description'];
    return params;
  }
}
