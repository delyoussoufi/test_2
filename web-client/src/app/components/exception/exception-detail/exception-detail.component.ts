import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ExceptionLog } from './../../../model/model.exception-log';
import { ExceptionService } from './../../../services/exception/exception.service';

@Component({
    selector: 'app-exception-detail',
    templateUrl: './exception-detail.component.html',
    styleUrls: ['./exception-detail.component.css'],
    standalone: false
})
export class ExceptionDetailComponent implements OnInit {

  exceptionLog: ExceptionLog = new ExceptionLog();

  constructor(private route: ActivatedRoute, private exceptionService: ExceptionService) {
    this.route.params.subscribe(params => {
      if (params && params.id) {
        this.exceptionService.get(params.id).subscribe(
          data => {
            this.exceptionLog = data;
          }
        );
      }
    });
  }

  ngOnInit() {
  }

}
