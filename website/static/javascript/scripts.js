 $(document).ready(function () {
	flatpickr('#datepicker', {
		dateFormat: "F j Y",
		time_24hr: false,
		allowInput:false
	});
	flatpickr('#datetimepicker', {
		enableTime: true,
		dateFormat: "F j Y h:i K",
		time_24hr: false,
		allowInput: false
	});
	flatpickr('#datetimepicker2', {
		enableTime: true,
		dateFormat: "F j Y h:i K",
		time_24hr: false,
		allowInput: false
	});
	// Retrieve domain and range data from HTML using jQuery
	var domain = $('#graph-data').data('domain');
	var range = $('#graph-data').data('range');

	// Render chart using domain and range data
	var ctx = document.getElementById('myChart').getContext('2d');
	var myChart = new Chart(ctx, {
	type: 'line',
	data: {
		labels: domain,
		datasets: [{
			label: 'Voltage',
			data: range,
			backgroundColor: 'rgba(255, 99, 132, 0.2)',
			borderColor: 'rgba(255, 99, 132, 1)',
			borderWidth: 1,
			showLine: false
            }]
		},
		options: {
			plugins: {
				legend: {
					display: false
                }
			},
			scales: {
				y: {
					title: {
						display: true,
						text: 'Voltage'
					}
				}
			}
		}
	});
});