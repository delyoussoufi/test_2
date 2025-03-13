export class UserDigitalisatComment {
  id: string;
  digitalisatId: string;
  userId: string;
  userName: string;
  reference: string;
  comment: string;
  commentLinkId: string;
  postDate: Date;
  replies: [UserDigitalisatComment];
}
