import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';

export interface CommentEvent {
  id: any;
  value: string;
}

@Component({
    selector: 'app-comment-viewer',
    templateUrl: './comment-viewer.component.html',
    styleUrls: ['./comment-viewer.component.css'],
    standalone: false
})
export class CommentViewerComponent implements OnInit {

  @Input()
  id: any;

  @Input()
  title = '';

  @Input()
  comment = '';

  @Input()
  isOwner = false;

  @Input()
  editable = true;

  @Input()
  canReply = true;

  @Output() commentChange = new EventEmitter<string>();

  @Output()
  save = new EventEmitter<any | CommentEvent>();

  @Output()
  saveReply = new EventEmitter<any | CommentEvent>();

  @Output()
  delete = new EventEmitter<any>();

  editing = false;
  replying = false;
  commentReply = '';

  private cacheEditingString: string;

  constructor() {
  }

  ngOnInit(): void {}

  onEditComment() {
    this.editing = true;
    this.cacheEditingString = this.comment;
  }

  onCommentEditCancel() {
    this.editing = false;
    this.comment = this.cacheEditingString;
    this.cacheEditingString = '';
  }

  onClickSaveCommentEdit() {
    this.save.emit({id: this.id, value: this.comment});
    this.editing = false;

  }

  onReplyCancel() {
    this.replying = false;
    this.commentReply = '';
  }

  onClickSaveCommentReply() {
    this.saveReply.emit({id: this.id, value: this.commentReply});
    this.onReplyCancel();
  }

  onDelete() {
    this.delete.emit(this.id);
  }
}
