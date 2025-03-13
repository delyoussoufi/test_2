import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';

@Component({
    selector: 'app-order-by-selector',
    templateUrl: './order-by-selector.component.html',
    styleUrls: ['./order-by-selector.component.css'],
    standalone: false
})
export class OrderBySelectorComponent implements OnInit {

  @Input()
  isDesc: boolean;

  @Input()
  isActive: boolean;

  @Input()
  title = 'sortieren';

  @Output()
  sort = new EventEmitter();

  constructor() { }

  ngOnInit(): void {
  }

}
