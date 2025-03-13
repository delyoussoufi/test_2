import {AfterViewInit, Component, ElementRef, EventEmitter, HostListener, Input, Output, ViewChild} from '@angular/core';

import {SafeUrl} from '@angular/platform-browser';

import {Box, FoundTerm, OcrData, SearchTermsFound, Word} from '../../../model/model.ocr-data';

@Component({
    selector: 'app-ocr-image-viewer',
    templateUrl: './ocr-image-viewer.component.html',
    styleUrls: ['./ocr-image-viewer.component.css'],
    standalone: false
})
export class OcrImageViewerComponent implements AfterViewInit {

  @ViewChild('canvasOverlay', {static: false}) canvasRef: ElementRef<HTMLCanvasElement>;
  @ViewChild('canvasReference', {static: false}) canvasReferenceRef: ElementRef<HTMLCanvasElement>;
  @ViewChild('image', {static: false}) imgRef: ElementRef<HTMLImageElement>;
  @ViewChild('popButton', {static: false}) popRef: ElementRef<HTMLButtonElement>;

  @Input() imageId: string;
  @Input() src: string | SafeUrl;
  @Input() selectedWord = '';
  @Input() showOcrData = false;
  @Input() showCarousel = true;
  @Input() hasSearch = true;
  @Input() size: number;
  @Input() imageName: string;
  @Input() disableLeftArrow = false;
  @Input() disableRightArrow = false;
  @Input() enableCategoryFunction = false;
  @Input() isImageInCategory = false;
  @Input() set ocrData (data: OcrData) {
    // This is called before highlightData.
    this.ocrDataSet = data;
    this.clearHighlightText();
    setTimeout(() => this.onChangeOcrData(), 1);
  }
  @Input() set highlightData (data: Array<SearchTermsFound>) {
    this._highlightData = data;
    // wait 100 ms to run highlightFoundTerms and possible select word.
    setTimeout(() => {
      this.clearHighlightText();
      this.onChangeSearch(this.selectedWord);
    }, 100);
  }

  @Output()
  imageLoaded = new EventEmitter<any>();
  @Output()
  nextImage = new EventEmitter();
  @Output()
  prevImage = new EventEmitter();
  @Output()
  removeImageFromCategory = new EventEmitter<string>();
  @Output()
  addImageToCategory = new EventEmitter<string>();

  public context: CanvasRenderingContext2D;
  public canvasElement: HTMLCanvasElement;
  public canvasReferenceElement: HTMLCanvasElement;

  public imageElement: HTMLImageElement;
  public popElement: HTMLButtonElement;

  public ocrDataSet: OcrData;
  public arrowKeyFocus = true;
  public _highlightData: Array<SearchTermsFound>;
  imageWidth = 100;
  imageHeight = 100;
  zoomX = 0;
  zoomY = 0;
  scale = 1;
  rotation = 0;
  isPanning = false;
  start = { x: 0, y: 0 };
  allWords: Array<Word> = [];
  // selectedWord: string;
  foundTermPosInfo = {x: -100, y: 0, w: 0, h: 0};
  searchInfo = {text: '', score: 0, term: ''};

  constructor() {}

  ngAfterViewInit(): void {
    this.setupOverlay();
  }

  getResize(): number {
    if (this.size) {
      return this.size;
    }
    return  this.showOcrData ? 600 : 1000;
  }

  onImageLoaded() {
    this.rescaleImage(this.getResize());
    this.imageLoaded.emit({'width': this.imageWidth, 'height': this.imageHeight});
    // if (this.selectedWord) {
    //   setTimeout(() => this.onChangeSearch(this.selectedWord), 1000);
    // }
  }

  setupOverlay() {
    this.imageElement = this.imgRef?.nativeElement;
    this.canvasElement = this.canvasRef?.nativeElement;
    this.canvasReferenceElement = this.canvasReferenceRef?.nativeElement;

    this.popElement = this.popRef?.nativeElement;
    if (this.imageElement && this.canvasElement && this.imageElement?.naturalHeight > 0) {
      // console.log('Setting', this.imageElement);
      this.context = this.canvasElement.getContext('2d');
      this.context.lineWidth = 1;
      this.context.strokeStyle = 'red';
      this.context.font = '50pt Arial';
      this.context.globalCompositeOperation = 'multiply';
      this.rescaleImage(this.getResize());

      // rescale image on image load event.
      this.imageElement.onload = (e) => this.onImageLoaded();

      // add event listener to canvas.
      this.canvasElement.addEventListener('mousewheel', (e) => this.onMouseWheel(e),  { passive: false });
      // this.canvasElement.addEventListener('mouseenter', (e) => console.log(e),  { passive: false });
      // this.canvasElement.addEventListener('mouseleave', (e) => console.log(e),  { passive: false });

      this.imageLoaded.emit({'width': this.imageWidth, 'height': this.imageHeight});
    } else {
      setTimeout(() => {  this.setupOverlay(); }, 10);
    }

  }

  rescaleImage(resize: number): void {
    if (this.imageElement) {
      const scale = resize / this.imageElement.naturalWidth; // uses width to rescale
      this.imageElement.width = this.imageElement.naturalWidth * scale;
      this.imageElement.height = this.imageElement.naturalHeight * scale;
      this.imageWidth =  this.imageElement.width;
      this.imageHeight = this.imageElement.height;
      // set canvas to the size of the resized image.
      this.canvasElement.width =  this.imageElement.width;
      this.canvasElement.height = this.imageElement.height;

      this.canvasReferenceElement.width =  this.imageElement.width;
      this.canvasReferenceElement.height = this.imageElement.height;

      // set the 2d context to the same scale as the image
      this.context?.scale(scale, scale);
      this.canvasReferenceElement?.getContext('2d').scale(scale, scale);
    }

  }

  drawBoxes(ocrData: OcrData) {
    if (this.context) {
      ocrData.words.forEach((w) => {
        const bbox = w.box;
        const x0 = bbox.x0; const xf = bbox.xf; const y0 = bbox.y0; const yf = bbox.yf;
        this.context.strokeRect(x0, y0, xf - x0, yf - y0);
        // this.context.fillText(w.text, x0, y0, xf - x0);
      });
    } else {
      setTimeout(() => {  this.drawBoxes(ocrData); }, 10);
    }
  }

  clearHighlightText() {
    this.context?.clearRect(0, 0, this.imageElement?.naturalWidth, this.imageElement?.naturalHeight);
  }

  clearSearchOnChangeImage() {
    // this.clearHighlightText();
    // this.selectedWord = null;
  }


  highlightText(word: string) {
    if (!word) {
      return;
    }
    const searchingTerm = word.toLowerCase().trim();
    const regex = new RegExp(searchingTerm);
    this.ocrDataSet?.words.forEach((w) => {
      if (w.text.toLowerCase().match(regex)) {
        const bbox = w.box;
        const x0 = bbox.x0; const xf = bbox.xf; const y0 = bbox.y0; const yf = bbox.yf;
        const index = w.text.toLowerCase().indexOf(searchingTerm);
        const width = xf - x0;
        const pxs = width /  Math.max(1, w.text.length); // pixel per word.
        this.context.fillStyle = 'rgba(100, 255, 50, 0.2)';
        this.context.beginPath();
        this.context.fillRect(x0 + index * pxs, y0, searchingTerm.length * pxs, yf - y0);
        this.context.closePath();
      }
    });
  }

  highlightFoundTerms(found_terms: Array<SearchTermsFound>) {
    if (!found_terms) {
      return;
    }
    if (this.context) {
      // this.clearHighlightText();
      const selectBoxes: Box[] = [];
      for (const stf of found_terms) {
        stf.found_terms.forEach((ft) => {
          const bbox = new Box(ft.box);
          const x0 = bbox.x0; const xf = bbox.xf; const y0 = bbox.y0; const yf = bbox.yf;
          const width = xf - x0;
          const height = yf - y0;
          // check for collision. I overlap is more than 50% then turn off alpha.
          const overlapBoxes = selectBoxes.filter(b => b.percentOverlappingArea(bbox) > 0.5);
          let alpha = 0;
          if (overlapBoxes.length === 0) {
            alpha =  Math.max(0.1, 0.6 - 1.5 * ft.score);
          }
          selectBoxes.push(bbox);
          // this.context.fillStyle = `rgba(200,60,185, ${alpha})`;  // purple
          this.context.fillStyle = `rgba(60,200,30, ${alpha})`;  // green

          this.context.beginPath();
          this.context.fillRect(x0, y0, width, height);
          // this.context.fillStyle = `rgba(200,60,185, 0.6)`;
          // this.context.fillText(`${ft.value} - error: ${ft.score}`, x0, y0, width + 50);
          this.context.closePath();
        });
      }
      // searchTerms.forEach((term) => this.highlightText(term));
    } else {
      setTimeout(() => this.highlightFoundTerms(found_terms), 100);
    }
  }

  highlightSearchText(searchTerm: string) {
    if (this.context) {
      const searchTerms = searchTerm.split(/&|<->|\s+/);
      this.clearHighlightText();
      searchTerms.forEach((term) => this.highlightText(term));
    }
  }

  onClickViewOcr() {
    this.showOcrData = !this.showOcrData;
    this.rescaleImage(this.getResize());
    // highlight classification again to keep it.
    this.onChangeSearch(this.selectedWord);
  }

  onChangeOcrData() {
    // creates a unique set of words. Remove words that repeat.
    this.allWords = this.ocrDataSet?.words.filter(
      (value, index, array) => array.map((w) => w.text).indexOf(value.text) === index);
    // call onChangeSearch to highlight selected word
    if (this.selectedWord) {
      this.highlightSearchText(this.selectedWord);
    }
  }

  onChangeSearch(e) {
    // this.highlightSearchText(e?.replace('<->', '&'));
    this.highlightSearchText(e);
    // highlight classification again to keep it.
    this.highlightFoundTerms(this._highlightData);
  }

  imageReset() {
    this.zoomY = 0;
    this.zoomX = 0;
    this.scale = 1;
  }

  rotateImage(rotationAngle: number) {
    this.rotation += rotationAngle;
  }



  onMouseWheel(event) {
    // const offX  = (event.offsetX + this.zoomX * this.scale || event.pageX - (event.target).offset().left) + this.zoomX;
    // console.log(this.popElement.offsetLeft, event.layerX);
    const wheelDelta = Math.max(-1, Math.min(1, (event.wheelDelta || -event.detail)));

    const xOrigin = this.imageWidth / 2;
    const yOrigin = this.imageHeight / 2;

    const xs = (event.layerX - this.zoomX - xOrigin) / this.scale;
    const ys = (event.layerY - this.zoomY - yOrigin) / this.scale;

    // const xs = (event.movementX - this.zoomX) / this.scale;
    // const ys = (event.movementY - this.zoomY) / this.scale;

    if (wheelDelta > 0) {
      this.mouseWheelUp();
    } else {
      this.mouseWheelDown();
    }

    if (event.preventDefault) {
      event.preventDefault();
    }

    // keep zoom at center
    // this.zoomX = event.layerX - xs * this.scale;
    // this.zoomY = event.layerY - ys * this.scale;

    this.zoomX = event.layerX - xOrigin - xs * this.scale;
    this.zoomY = event.layerY - yOrigin - ys * this.scale;

  }

  onFoundTermOver(box, ft: FoundTerm, search_term: string) {
    this.foundTermPosInfo.x = box.x + this.zoomX;
    this.foundTermPosInfo.y = box.y + this.zoomY;
    this.foundTermPosInfo.w = box.w;
    this.foundTermPosInfo.h = box.h;
    this.searchInfo = {text: ft.value, score: ft.score, term: search_term};
  }

  onFoundTermOut() {
    // remove button from view
    this.foundTermPosInfo.x = -1000;
    this.foundTermPosInfo.y = -1000;
  }

  rotatePoint(x, y, xc, yc, angle) {
    const x0Rot = (x - xc) * Math.cos(angle) - (y - yc) * Math.sin(angle) + xc;
    const y0Rot = (x - xc) * Math.sin(angle) + (y - yc) * Math.cos(angle) + yc;
    return {'x': x0Rot, 'y': y0Rot};
  }

  isOverFoundTerm(e) {
    if (!this._highlightData) {
      return;
    }
    const rect = this.canvasReferenceElement.getBoundingClientRect();
    const scaleX = this.imageElement.naturalWidth / rect.width;
    const scaleY = this.imageElement.naturalHeight / rect.height;
    let isOverBoxes = false;
    const angle = this.rotation * Math.PI / 180;
    const xc = this.imageElement.naturalWidth / 2; const yc = this.imageElement.naturalHeight / 2;

    const mouseX = (e.clientX - rect.left) * scaleX;
    const mouseY = (e.clientY - rect.top) * scaleY;

    for (const stf of this._highlightData) {
      stf.found_terms.forEach((ft) => {
        const bbox = ft.box;
        let x0 = bbox.x0; let xf = bbox.xf; let y0 = bbox.y0; let yf = bbox.yf;
        const p0 = this.rotatePoint(x0, y0, xc, yc, angle);
        const pf = this.rotatePoint(xf, yf, xc, yc, angle);
        x0 = p0.x; xf = pf.x; y0 = p0.y; yf = pf.y;
        // invert points if necessary.
        if (x0 > xf) {
          x0 = pf.x; xf = p0.x;
        }
        if (y0 > yf) {
          y0 = pf.y; yf = p0.y;
        }
        // console.log(-x0Rot, y0Rot);
        // this.context.strokeRect(10, 10, 100, 100);
        // this.context.strokeRect(x0, y0, xf - x0, yf - y0);

        // console.log('mouse:', x, y);
        // console.log('retc:', x0, xf, y0, yf);


        if (mouseX >= x0 && mouseX <= xf && mouseY >= y0 && mouseY <= yf) {
          const xCenter = (1 - this.scale) * this.imageWidth / 2;
          const yCenter = (1 - this.scale) * this.imageHeight / 2;

          // adjust for when transform-origin of the image is the center.
          const rescaledBox =  {x: x0 / scaleX + xCenter, y : y0 / scaleY + yCenter, w: (xf - x0) / scaleX, h: (yf - y0) / scaleY};
          this.onFoundTermOver(rescaledBox, ft, stf.value);
          isOverBoxes = true;
        }
      });
      if (!isOverBoxes) {
        this.onFoundTermOut();
      }
    }
  }

  mouseWheelUp() {
    this.scale *= 1.2;
  }

  mouseWheelDown() {
    this.scale /= 1.2;
  }

  moveImage(e) {
    e.preventDefault();
    if (!this.isPanning) {
      this.isOverFoundTerm(e);
      return;
    }
    this.zoomX = (e.clientX - this.start.x);
    this.zoomY = (e.clientY - this.start.y);
  }

  mouseDown(e) {
    this.start = { x: e.clientX - this.zoomX, y: e.clientY - this.zoomY};
    this.isPanning = true;
  }

  onMouseOver(e) {}

  @HostListener('document:mousedown', ['$event'])
  mouseDownDocument(e) {
    // If click inside a textarea or input remove focus from arrows.
    const nodeName: string = e.target.nodeName.toLowerCase();
    this.arrowKeyFocus = !(nodeName === 'textarea' || nodeName === 'input');
  }

  @HostListener('document:mouseup', ['$event'])
  onMouseUp(e: MouseEvent) {
    this.isPanning = false;
  }

  @HostListener('document:keydown', ['$event'])
  onKeyPress(e: KeyboardEvent, ) {
    // if not in focus do nothing.
    if (!this.arrowKeyFocus) { return; }

    if (e.code === 'ArrowLeft' || e.code === 'ArrowRight') {
      e.preventDefault();
      this.clearSearchOnChangeImage();
      if (e.code === 'ArrowLeft' && !this.disableLeftArrow) {
        this.prevImage.emit();
      } else if (e.code === 'ArrowRight' && !this.disableRightArrow) {
        this.nextImage.emit();
      }
    }
  }

}
