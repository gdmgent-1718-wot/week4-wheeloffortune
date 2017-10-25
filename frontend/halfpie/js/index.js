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
        20]
};

var settings = {
  total: 200, // 2x total for half-pie chart
  startAngle: 270, // or 90
  showLabel: true,
  labelDirection: 'center',
  labelOffset: 0
};

new Chartist.Pie('.ct-pie', data, settings);