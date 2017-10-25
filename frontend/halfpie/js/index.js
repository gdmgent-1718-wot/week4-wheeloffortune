var data = {
  labels:       [
        "€100",
        "€0",
        "€20",
        "€10",
        "€50"
      ],
  series:       [
        20,
        20,
        20,
        20,
        20],
  moreInfo: [
      {
          index: 0,
          class: '.ct-series-a',
          dutyCycle: 11
      },
      {
          index: 1,
          class: '.ct-series-b',
          dutyCycle: 9
      },
      {
          index: 2,
          class: '.ct-series-c',
          dutyCycle: 7.5
      },
      {
          index: 3,
          class: '.ct-series-d',
          dutyCycle: 5
      },
      {
          index: 4,
          class: '.ct-series-e',
          dutyCycle: 3.5
      },
  ]};


var settings = {
  total: 200, // 2x total for half-pie chart
  startAngle: 270, // or 90
  showLabel: true,
  labelDirection: 'center',
  labelOffset: 0
};

new Chartist.Pie('.ct-pie', data, settings);