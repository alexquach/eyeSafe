const POLL_URL = "http://127.0.0.1:5000/poll";

function poll_data() {
    /* Request */
    const xhr = new XMLHttpRequest();
    xhr.addEventListener('readystatechange', function () {
        if (xhr.readyState == 4) {
        if (xhr.status == 200) {

            const count = JSON.parse(xhr.response)["count"];
            const times = JSON.parse(xhr.response)["datetime_array"];
            
            console.log("COUNTER", JSON.parse(xhr.response), count);

            chrome.storage.sync.get("eyeSafe", data=>{
                let eyeSafe = data.eyeSafe;
                if (eyeSafe) {
                    eyeSafe["days"]["get_date"]["count"] += count;
                    eyeSafe["days"]["get_date"]["times"].push(times);

                    chrome.storage.sync.set({"eyeSafe" : eyeSafe}, post_data=>{
                        console.log("Appended data!");
                        console.log(eyeSafe);
                    });
                }
                else {
                    /* Create new object */
                    eyeSafe = {
                        "days": {}
                    };
                    eyeSafe["days"]["get_date"] = {
                        "count" : count,
                        "times" : times
                    };
                    chrome.storage.sync.set({"eyeSafe" : eyeSafe}, post_data=>{
                        console.log("Saved data!");
                        console.log(eyeSafe);
                    });
                }
            });
        }
      }
    });
    xhr.open('GET', POLL_URL);
    xhr.send();
}


setInterval(poll_data, 20000);