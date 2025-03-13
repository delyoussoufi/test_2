import {Component, HostListener, Input, OnInit, Renderer2} from '@angular/core';

@Component({
    selector: 'app-splitter',
    templateUrl: './splitter.component.html',
    styleUrls: ['./splitter.component.css'],
    standalone: false
})
export class SplitterComponent implements OnInit {

  @Input()
  parent: HTMLElement;

  isDraggable = false;

  constructor(private renderer: Renderer2) { }

  ngOnInit(): void {}

  @HostListener('document:mousemove', ['$event'])
  drag(e) {
    if (!this.isDraggable) {
      return;
    }
    this.renderer.setStyle(this.parent, 'width', `${e.clientX}px`);
  }

  mouseDown(e) {
    e.preventDefault();
    this.isDraggable = true;
  }

  @HostListener('document:mouseup', ['$event'])
  onMouseUp(event: MouseEvent) {
    this.isDraggable = false;
  }

}
