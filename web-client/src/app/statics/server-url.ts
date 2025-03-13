export class ServerUrl {
  private static API_URL = 'http://localhost:5001';
  // private static API_URL = 'http://10.175.97.160';
  // private static API_URL = 'http://10.175.97.161';

  static get rootUrl(): string {
    return this.API_URL;
  }

}
