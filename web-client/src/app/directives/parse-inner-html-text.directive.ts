import {AfterViewInit, Directive, ElementRef} from '@angular/core';

@Directive({
    selector: '[appParseInnerHtmlText]',
    standalone: false
})
export class ParseInnerHtmlTextDirective implements AfterViewInit {

  constructor(private el: ElementRef<HTMLElement>) {
  }

  private target: HTMLElement;

  /**
   * Parse a string between [] to a html link reference, i.e: [www.example.com] -> <a href="//www.example.com">www.example.com</a>
   * @param v A string to be parsed.
   * @private
   * @return The parsed string.
   */
  private static parseUrlLink(v: string): string {
    const re = new RegExp(/\S*\[(https:\/\/|http:\/\/|www\.)[^\]]+]|\S*(https:\/\/|http:\/\/|www\.)\S+/, 'gi'); // flags: g=global, i=case insensitive.
    const matchOperator = new RegExp(/[\[\]]/, 'g');
    const matchProtocols = new RegExp(/http:\/\/|https:\/\//, 'g');
    const splitTag = new RegExp(/\s+/, 'g');
    v?.match(re)?.forEach(
      s => {
        const values = s.replace(matchOperator, ' ').trim()?.split(splitTag, 2);
        const linkName = values[0];
        const href = values.length > 1 ? values[1].replace(matchProtocols, '') : linkName.replace(matchProtocols, '');
        v = v.replace(s, `<a href="//${href}" target="_blank">${linkName}</a>`);
      }
    );
    return v;
  }

  ngAfterViewInit() {
    this.target = this.el.nativeElement;
    this.parseInnerText();
  }

  parseInnerText() {
    this.target.innerHTML = ParseInnerHtmlTextDirective.parseUrlLink(this.target?.innerText);
  }

}
