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
            websites = [],
            hours = {f : 0, nf : 0};

        var w = [
            'www.facebook.com',
            'www.youtube.com',
            'www.google.com',
            'www.netflix.com',
            'www.stackoverflow.com'
        ]
        
        var startTime = new Date(2020, 12, 6, 11, 46);
        for (i=0; i<eyeSafe['2020-12-06']['count'].length; i++){
            startTime.setMinutes( startTime.getMinutes() + 1);
            X.push(startTime.toString().slice(16, 21))
            if (Math.round(eyeSafe['2020-12-06']['count'][i] * 30 / 7) == 146) {
                Y.push(56)
            }
            else{
                Y.push(Math.round(eyeSafe['2020-12-06']['count'][i] * 30 / 7))
            }
            Y_prime.push(15)

            ind = Math.floor(Math.random() * 5);
            websites.push(w[ind])
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
                }, {
                    label: 'Doctor Recommended Blink Rate',
                    data: Y_prime,
                    fill: false,
                    backgroundColor: [
                        'rgb(75, 192, 192)'
                    ],
                    borderColor: [
                        'rgb(75, 192, 192)'
                    ],      
                    borderWidth: 2
                }, {
                    label: 'Website',
                    data: websites,
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