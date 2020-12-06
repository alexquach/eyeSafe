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
            
            console.log("Blink Count", count);

            chrome.storage.local.get("eyeSafe", data=>{
                let eyeSafe = data.eyeSafe;
                if (eyeSafe) {
                    eyeSafe[res_date]["count"].push(count);
                    eyeSafe[res_date]["times"].push(times);

                    chrome.storage.local.set({"eyeSafe" : eyeSafe}, post_data=>{
                        console.log("Appended data!");
                        if (eyeSafe[res_date]["count"].length >= 5) // only make Zoom changes when have enough data (5 min).
                        {
                            check_zoom_update(eyeSafe[res_date]["count"])
                        }

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
                    });
                }
            });
        }
      }
    });
    xhr.open('GET', POLL_URL);
    xhr.send();
}

/*
 * Ensure document is loading properly and content_script can inject message
 * Source: https://stackoverflow.com/questions/23895377/sending-message-from-a-background-script-to-a-content-script-then-to-a-injected 
 */
function ensureSendMessage(tabId, message, callback){
    chrome.tabs.sendMessage(tabId, {ping: true}, function(response){
        if(response && response.pong) { // Content script ready
            console.log("Sent message to content script with zoom:", message.zoom_height);
            chrome.tabs.sendMessage(tabId, message, callback);
      } else { // No listener on the other end
        chrome.tabs.executeScript(tabId, {file: "scripts/root.js"}, function(){
          if(chrome.runtime.lastError) {
            console.error(chrome.runtime.lastError);
            throw Error("Unable to inject script into tab " + tabId);
          }
          // OK, now it's injected and ready
          chrome.tabs.sendMessage(tabId, message, callback);
        });
      }
    });
  }

function zoom(zoom_height){
    chrome.tabs.query({active:true,windowType:"normal", currentWindow: true}, data=>{
        let id = data[0].id;
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            ensureSendMessage(id, {zoom_height: zoom_height});
        });
    });
}



function check_zoom_update(count_arr) {
    const last_five = count_arr.slice(count_arr.length - 5);
    const THRESHOLD = 1/3.6; //zoom constant

    let zoom_in_counter = 0;
    let zoom_out_counter = 0;
    
    for (i = 0; i < last_five.length; i++) {
        console.log(last_five[i]);

        if (last_five[i] < LOWER_THRESHOLD_BLINK_RATE) {
            zoom_in_counter += THRESHOLD;
        }
        else if (last_five[i] > HIGHER_THRESHOLD_BLINK_RATE) {
            zoom_out_counter -= THRESHOLD;
        }
    }

    zoom(0.5 * (zoom_in_counter + zoom_out_counter)); //set average to avoid weird glitch.
}


setInterval(poll_data, 7000);