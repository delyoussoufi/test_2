import {Directive, ElementRef, Input, OnChanges, SimpleChanges} from '@angular/core';

@Directive({
    selector: '[appOcrTextHighlight]',
    standalone: false
})
export class OcrTextHighlightDirective implements OnChanges {

  @Input() appOcrTextHighlight = '';
  @Input() set ocrText(v: string) {
    this._ocrText = this.cleanText(v);
  }

  private target: HTMLElement;
  private _ocrText: string;

  constructor(private el: ElementRef<HTMLElement>) {
    this.target = el.nativeElement;
  }

  // triggers every time an input property changes.
  ngOnChanges(changes: SimpleChanges) {
    const v = changes?.appOcrTextHighlight?.currentValue ? changes.appOcrTextHighlight.currentValue : this.appOcrTextHighlight;
    this.highlightText(v);
  }

  private cleanText(text: string): string {
    return text?.replace(/<|>/gi, '');
  }

  get ocrText(): string {
    return this._ocrText;
  }

  private highlightText(value: string) {
    if (value && this.ocrText) {
      value = value.replace(/&/gi, '|');  // replace '&' by '|' to be used in regular expression.
      let newText = this.ocrText; // copy ocr text;
      // split values by operator |
      value.split('|').forEach(v => {
        if (v.trim()) {
          const re = new RegExp(v.trim(), 'gi'); // flags: g=global, i=case insensitive.
          newText = newText.replace(re, ` <span class="highlight-text">${v.trim()}</span>`);
        }
      });
      this.text = newText;
    } else {
      if (this.ocrText) {
        this.text = this.ocrText;
      }
    }
  }

  private set text(value: string) {
    this.target.innerHTML = value;
  }

}
