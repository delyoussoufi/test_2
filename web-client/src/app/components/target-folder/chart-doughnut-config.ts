export const doughnutOptions: any = {
  plugins: {
    colors: {
      backgroundColor: ['rgba(228, 58, 58, 0.6)', 'rgba(85, 212, 91, 0.6)']
    }
  },
  tooltips: {
    // Override position of tooltip. Makes tooltip point outside the doughnut instead of inside.
    custom: function(tooltips: any) {
      // console.log(tooltips);
      if (tooltips.xAlign === 'left') {
        tooltips.xAlign = 'right';
        tooltips.x -= (tooltips.width + tooltips.xPadding);
      } else {
        tooltips.xAlign = 'left';
        tooltips.x += tooltips.width + tooltips.xPadding;
      }
    },
    callbacks: {
      label: function(tooltipItem: any, _data: any) {
        // console.log(tooltipItem.index);
        const dataset: Array<any> = _data.datasets[0].data;
        let totalSpace = 0;
        for (const data of dataset) {
          totalSpace += data;
        }
        if (totalSpace === 0) {
          return '%';
        }
        const prefix = tooltipItem.index === 0 ? 'Belegter: ' : 'Freier: ';
        const percentage = dataset[tooltipItem.index] * 100 / totalSpace;
        return prefix + percentage.toPrecision(3) + '%';
      }
    }
  },
  aspectRatio:4,
};

export const doughnutChartColors = ['rgba(228, 58, 58, 0.6)', 'rgba(85, 212, 91, 0.6)'];
