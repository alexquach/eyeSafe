const POLL_URL = "http://127.0.0.1:5000/poll";

function poll_data() {
    /* Request */
    const xhr = new XMLHttpRequest();
    xhr.addEventListener('readystatechange', function () {
        if (xhr.readyState == 4) {
        if (xhr.status == 200) {
            console.log(JSON.parse(xhr.response));
        }
      }
    });
    xhr.open('GET', POLL_URL);
    xhr.send();
}


setInterval(poll_data, 10000);