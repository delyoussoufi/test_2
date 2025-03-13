import {AfterViewInit, Directive, TemplateRef, ViewContainerRef} from '@angular/core';

@Directive({
    selector: '[appInView]',
    standalone: false
})
export class InViewDirective implements AfterViewInit {
  alreadyRendered: boolean; // checking if visible already

  constructor(
    private vcRef: ViewContainerRef,
    private tplRef: TemplateRef<any>
  ) {}

  ngAfterViewInit() {
    const commentEl = this.vcRef.element.nativeElement; // template
    const elToObserve = commentEl.parentElement;
    this.setMinWidthHeight(elToObserve);

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        this.renderContents(entry.isIntersecting);
      });
    }, {threshold: [0, .1, .9, 1]});
    observer.observe(elToObserve);
  }

  renderContents(isInView) {
    if (isInView && !this.alreadyRendered) {
      this.vcRef.clear();
      this.vcRef.createEmbeddedView(this.tplRef);
      this.alreadyRendered = true;
    }
  }

  setMinWidthHeight(el) { // prevent issue being visible all together
    const style = window.getComputedStyle(el);
    // tslint:disable-next-line:radix
    const [width, height] = [parseInt(style.width), parseInt(style.height)];
    // tslint:disable-next-line:no-unused-expression
    !width && (el.style.minWidth = '40px');
    // tslint:disable-next-line:no-unused-expression
    !height && (el.style.minHeight = '40px');
  }
}
