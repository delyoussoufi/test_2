

function objectToDict(obj) {
  const k: string[] = Object.keys(obj);
  const v = Object.values(obj);

  const dict = {};
  k.map((e, i) => dict[e] = v[i]);

  return dict;
}

export class Search {

  public searchBy: Array<string> | string;
  public searchValue: Array<string>;
  public page: number;
  public perPage: number;
  public orderDesc: boolean;
  public orderBy: string;
  public operator: string;
  public mapColumnAndValue: boolean;
  public use_AND_Operator: boolean;
  public textualQuery: boolean;


  constructor(searchBy: string = '', value: Array<string> = []) {
    this.searchBy = searchBy;
    this.searchValue = value;
    this.page = 1;
    this.perPage = 10;
    this.orderDesc = false;
    this.orderBy = '';
    this.operator = 'CONTAINS';
    this.mapColumnAndValue = true;
    this.use_AND_Operator = true;
    this.textualQuery = null;
  }

  public toDict() {
    const dict = objectToDict(this);
    for (const key in dict) {
      if (dict[key] && typeof(dict[key]) === 'object') {
        dict[key] = JSON.stringify(dict[key]);
      }
    }
    return dict;
  }
}
