export class VorgangSessionSearch {
  createDateBegin: string;
  createDateEnd: string;
  vorgangsnummer: string;
  searchCategoryId: string;

  orderBy: string;
  orderDirection: string;
  operator = 'CONTAINS';

  page: number;
  itemsPerPage: number;
  totalItems: number;
}
