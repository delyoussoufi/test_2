import {Component, Input, OnInit, TemplateRef} from '@angular/core';
import {Digitalisat} from '../../../model/model.digitalisat';
import {UserDigitalisatComment} from '../../../model/model.user-digitalisat-comment';
import {ComponentUtils} from '../../component.utils';
import {ToasterNotificationService} from '../../../services/notification/toaster-notification.service';
import {DigitalisatService} from '../../../services/digitalisat/digitalisat.service';
import {BsModalService} from 'ngx-bootstrap/modal';
import {BsModalRef} from 'ngx-bootstrap/modal/bs-modal-ref.service';
import {CommentEvent} from '../comment-viewer/comment-viewer.component';
import {DatePipe} from '@angular/common';

@Component({
    selector: 'app-metadata-comments-view',
    templateUrl: './metadata-comments-view.component.html',
    styleUrls: ['./metadata-comments-view.component.css'],
    standalone: false
})
export class MetadataCommentsViewComponent  extends ComponentUtils implements OnInit {

  @Input()
  set digitalisat(d: Digitalisat) {
    this._digitalisat = d;
    this.fetchComments(d?.id);
  }
  @Input()
  reference: string;

  userComment: string;
  userComments: Array<UserDigitalisatComment> = [];
  deleteComment: UserDigitalisatComment;
  dataPipe = new DatePipe('de');

  private _digitalisat: Digitalisat;
  private modalRef: BsModalRef | null;


  constructor(private toasterNotificationService: ToasterNotificationService,  private digitalisatService: DigitalisatService,
              private modalService: BsModalService) {
    super(toasterNotificationService);
  }

  ngOnInit(): void {
  }

  openUserCommentDeleteModal(template: TemplateRef<any>, uc: UserDigitalisatComment) {
    this.modalRef = this.modalService.show(template);
    this.deleteComment = uc;
  }

  closeUserCommentDeleteModal() {
    this.modalRef?.hide();
    this.modalRef = null;
    this.deleteComment = null;
  }

  onDeleteCommentFromModal() {
    this.onDeleteComment(this.deleteComment);
    this.closeUserCommentDeleteModal();
  }

  get digitalisat(): Digitalisat {
    return this._digitalisat;
  }

  fetchComments(digitalisat_id) {
    if (!digitalisat_id) { return; }
    this.digitalisatService.getComments(digitalisat_id).subscribe(
      data => {
        this.userComments = data;
      },
      error => {
        console.log(error);
      }
    );
  }

  isCommentOwner(uc: UserDigitalisatComment): boolean {
    return this.hasRole('ROLE_ADMIN') || uc.userId === this.currentUser.userId;
  }

  onClickSaveCommentEdit(e: CommentEvent) {
    const uc: UserDigitalisatComment = e.id;
    uc.comment = e.value;
    this.digitalisatService.updateComment(uc).subscribe();
  }

  onClickSaveCommentReply(e: CommentEvent) {
    if (!e.value ) { return; }
    this.addComment(e.value, null, e.id);
  }

  onDeleteComment(uc: UserDigitalisatComment) {
    if (uc) {
      if (uc.commentLinkId) {
        this.removeItemFromList(this.userComments.find(el => el.id === uc.commentLinkId)?.replies, uc);
      } else {
        this.removeItemFromList(this.userComments, uc);
      }
      this.digitalisatService.deleteComment(uc).subscribe();
    }
  }

  addComment(comment: string, reference: string, parentComment: UserDigitalisatComment = null) {
    const uc = new UserDigitalisatComment();
    uc.userName = this.currentUser.username; // just a placeholder for the frontend. This should be filled by the backend.
    uc.userId = this.currentUser.userId; // just a placeholder for the frontend. This should be filled by the backend.
    uc.postDate = new Date(); // just a placeholder for the frontend. This should be filled by the backend.
    uc.digitalisatId = this.digitalisat.id;
    uc.reference = reference;
    uc.comment = comment;
    uc.commentLinkId = parentComment ? parentComment.id : null;
    this.digitalisatService.addComment(uc).subscribe(
      data => {
        if (data) {
          if (!parentComment) {
            // add element to the beginning of the list
            this.userComments.unshift(data);
          } else {
            parentComment.replies.push(data);
          }
        }
      },
      error => {
        console.log(error);
        this.toasterNotificationService.showErrorMessage(error.message.error);
      }
    );
  }

  onAddComment() {
    this.addComment(this.userComment, this.reference);
    this.userComment = null;
  }
}
