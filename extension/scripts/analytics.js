/**
 * Define Canvas
 */
var ctx = document.getElementById('analytics').getContext('2d');

/**
 * Retrieve data from shared local session (Chrome)
 */
chrome.storage.local.get("eyeSafe", data => {
    let eyeSafe = data.eyeSafe;
    console.log(eyeSafe)
    if (eyeSafe['2020-12-06']) {
        var X = [],
            Y = [],
            Y_prime = [],
            hours = {f : 0, nf : 0};
        
        var startTime = new Date(2020, 12, 6, 11, 46);
        for (i=0; i<eyeSafe['2020-12-06']['count'].length; i++){
            startTime.setMinutes( startTime.getMinutes() + 1);
            X.push(startTime.toString().slice(16, 21))
            Y.push(Math.round(eyeSafe['2020-12-06']['count'][i] * 60 / 7))
        }

        console.log(X)
        console.log(Y)
        
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: X,
                datasets: [{
                    label: 'Number of blinks per minute',
                    data: Y,
                    fill: false,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                title: {
                    display: true,
                    text: 'Blink Rate (per Min) vs. Time (Min)'
                },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                },
                hover: {
                    mode: 'nearest',
                    intersect: true
                },
                scales: {
                    xAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Time (HH:MM)'
                        }
                    }],
                    yAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Blinks (per minute)'
                        }
                    }]
                }
            }
        });

    }
});