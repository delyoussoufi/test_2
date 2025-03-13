export class VorgangSearch {
  createDateBegin: string;
  createDateEnd: string;
  vorgangsnummer: string;
  searchCategoryId: string;
  firstResult: number;
  maxResults: number;
  orderBy: string;
  orderDirection: string;
  operator = 'CONTAINS';
}
