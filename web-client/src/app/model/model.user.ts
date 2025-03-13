export class User {
  userId: string;
  token: string;
  username  = '';
  surname = '';
  forename = '';
  password = '';
  enabled = true;
  accountNonExpired = true;
  accountNonLocked = true;
  credentialsNonExpired = true;
  roles: string[];
  rights: string[];
  settings: string[];
}
