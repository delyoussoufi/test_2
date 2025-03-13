import {User} from "./model.user";

export class ProfileUser {
    userId: string;
    username: string;
    surname: string;
    forename: string;
    password: string;
    repeatedPassword: string;

    updateFromUser(user: User) {
      this.userId = user.userId;
      this.username = user.username;
      this.surname = user.surname;
    }
}
