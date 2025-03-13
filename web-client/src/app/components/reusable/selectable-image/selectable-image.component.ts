import {AfterViewInit, Component, ElementRef, EventEmitter, Input, OnInit, Output, ViewChild} from '@angular/core';
import {SafeUrl} from '@angular/platform-browser';

export interface ImageSelectEvent {
  id: string;
  selected: boolean;
}

@Component({
    selector: 'app-selectable-image',
    templateUrl: './selectable-image.component.html',
    styleUrls: ['./selectable-image.component.css'],
    standalone: false
})
export class SelectableImageComponent implements AfterViewInit  {

  @ViewChild('canvas', {static: false}) canvasRef: ElementRef<HTMLCanvasElement>;

  @Input() itemId: string;
  @Input() src: string | SafeUrl;
  @Input() name: string;
  @Input() title: string;
  @Input() highlightTitle = false;
  @Input() isSelect = false;

  @Output()
  selectChanged = new EventEmitter<ImageSelectEvent>();

  private canvas: HTMLCanvasElement;
  private context: CanvasRenderingContext2D;

  private selectImage = new Image();
  private selectedImage = new Image();

  constructor() {
    this.selectImage.src = './assets/images/select.png';
    this.selectedImage.src = './assets/images/selected.png';
  }

  ngAfterViewInit(): void {
    this.canvas = this.canvasRef.nativeElement;
    this.context = this.canvas?.getContext('2d');

    // call draw method after load images.
    this.selectImage.onload = () => this.drawImageSelectLayer();
    this.selectedImage.onload = () => this.drawImageSelectLayer();
  }

  drawImageSelectLayer() {
    this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
    if (this.isSelect) {
      this.context.drawImage(this.selectedImage, 0, 0, this.canvas.width, this.canvas.height);
    } else {
      this.context.drawImage(this.selectImage, 0, 0, this.canvas.width, this.canvas.height);
    }
  }

  onSelectClick() {
    this.isSelect = !this.isSelect;
    this.drawImageSelectLayer();
    this.selectChanged.emit( {id: this.itemId, selected: this.isSelect} );
  }

}
