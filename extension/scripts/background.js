const POLL_URL = "http://127.0.0.1:5000/poll";
const LOWER_THRESHOLD_BLINK_RATE = 10;
const HIGHER_THRESHOLD_BLINK_RATE = 15;

function poll_data() {
    /* Request */
    const xhr = new XMLHttpRequest();
    xhr.addEventListener('readystatechange', function () {
        if (xhr.readyState == 4) {
        if (xhr.status == 200) {

            const count = JSON.parse(xhr.response)["count"];
            const times = JSON.parse(xhr.response)["datetime_array"];
            const res_date = JSON.parse(xhr.response)["sentTime"].substring(0, 10);
            
            console.log("COUNTER", JSON.parse(xhr.response), count);

            chrome.storage.local.get("eyeSafe", data=>{
                let eyeSafe = data.eyeSafe;
                if (eyeSafe) {
                    eyeSafe[res_date]["count"].push(count);
                    eyeSafe[res_date]["times"].push(times);

                    chrome.storage.local.set({"eyeSafe" : eyeSafe}, post_data=>{
                        console.log("Appended data!");
                        console.log(eyeSafe);
                    });
                }
                else {
                    /* Create new object */
                    eyeSafe = {
                        res_date: {}
                    };
                    eyeSafe[res_date] = {
                        "count" : [count],
                        "times" : [times]
                    };
                    chrome.storage.local.set({"eyeSafe" : eyeSafe}, post_data=>{
                        console.log("Saved data!");
                        console.log(eyeSafe);
                    });
                }

                check_zoom_update(eyeSafe[res_date]["count"])
            });
        }
      }
    });
    xhr.open('GET', POLL_URL);
    xhr.send();
}

function receiveText(res){
    console.log(res);
}

function zoom(paramvar){
    console.log('inside zoom')
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.executeScript(
            tabs[0].id,
            {
            code: 'var zoomStr = document.body.style.zoom; currentZoom = parseInt(zoomStr.substring(0, zoomStr.indexOf('%'))); currentZoom += ' + paramvar + '; document.body.style.zoom = currentZoom + "%"; console.log("print inside executeScript")'
            //If you had something somewhat more complex you can use an IIFE:
            //code: '(function (){return document.body.innerText;})();'
            //If your code was complex, you should store it in a
            // separate .js file, which you inject with the file: property.
        },receiveText);
    })

}

function check_zoom_update(count_arr) {
    last_five = count_arr.slice(count_arr.length - 5)

    zoom_in_counter = 0;
    zoom_out_counter = 0;
    for (i = 0; i < last_five.length; i++) {
        if (last_five[i] < LOWER_THRESHOLD_BLINK_RATE) {
            zoom_in_counter ++;
        }
        else if (last_five[i] > HIGHER_THRESHOLD_BLINK_RATE) {
            zoom_out_counter ++;
        }
    }

    if (zoom_in_counter >= 4) {
        zoom(10)
    }
    if (zoom_out_counter >= 3) {
        zoom(-10)
    }
    console.log(zoom_in_counter)
    console.log(zoom_out_counter)

}


setInterval(poll_data, 20000);