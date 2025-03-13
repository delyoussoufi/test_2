// This class should be equal to SearchCategory at the Python side.
import {SearchTerm} from './model.search-term';
import {SearchBlacklist} from './model.search-blacklist';
import {SearchIgnoreList} from './model.search-ignore-list';

export class SearchCategory {

  id: string;
  name: string;
  description: string;
  order: number;
  searchTerms: Array<SearchTerm>;
  blacklist: Array<SearchBlacklist>;
  ignoreList: Array<SearchIgnoreList>;
}
