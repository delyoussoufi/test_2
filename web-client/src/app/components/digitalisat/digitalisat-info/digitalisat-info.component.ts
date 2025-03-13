import {Component, OnInit} from '@angular/core';

import {DigitalisatService} from '../../../services/digitalisat/digitalisat.service';
import {map} from "rxjs/operators";
import {Observable} from "rxjs";
import {ChartType} from "chart.js";


@Component({
    selector: 'app-digitalisat-info',
    templateUrl: './digitalisat-info.component.html',
    styleUrls: ['./digitalisat-info.component.css'],
    standalone: false
})
export class DigitalisatInfoComponent implements OnInit {

  public doughnutOptions = {
    plugins: {},
    tooltips: {
      // Override position of tooltip. Makes tooltip point outside the doughnut instead of inside.
      custom: function(tooltips: any) {},
      callbacks: {}
    },
    aspectRatio:4,
  };

  public doughnutChartData: number[] = [];
  public doughnutChartLabels: string[] = [];
  public total = 0;
  isLoading = true;
  digitalisatInfo$: Observable<any>;
  public doughnutType: ChartType = 'doughnut';

  private doughnutChartColors = [
    'rgba(85, 212, 91, 0.6)',
    'rgba(229,145,145,0.63)',
    'rgba(255,238,21,0.44)',
    'rgb(138,44,100)',
  ];

  constructor(private digitalisatService: DigitalisatService) {
    this.fetch_info();
  }

  ngOnInit(): void {
  }

  private resetDoughnut() {
    this.total = 0;
    this.doughnutChartData = [];
    this.doughnutChartLabels = [];
  }

  private fetch_info() {
    this.isLoading = true;
    this.resetDoughnut();
    this.digitalisatInfo$ = this.digitalisatService.getInfo().pipe(
      map((data) => {
        data?.forEach(info => {
          this.total += info.total;
          this.doughnutChartData.push(info.total);
          this.doughnutChartLabels.push(info.status);
        });
        return {
          datasets: [{
            data: this.doughnutChartData,
            backgroundColor: this.doughnutChartColors,
          }],
          // These labels appear in the legend and in the tooltips when hovering different arcs
          labels: this.doughnutChartLabels

        }
      })
    );
    // this.digitalisatService.getInfo().subscribe(
    //   data => {
    //     data?.forEach(info => {
    //       this.total += info.total;
    //       this.doughnutChartData.push(info.total);
    //       this.doughnutChartLabels.push(info.status);
    //     });
    //     this.isLoading = false;
    //   }
    // );
  }

}
