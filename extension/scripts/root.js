// Content script
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    let zoom = ( window.outerWidth - 10 ) / window.innerWidth;
    zoom /= 3.6;
    /* Set zoom level */
    document.body.style.zoom = `${zoom + request.zoom_height}`;
    console.log("Updated Zoom level", request.zoom_height, zoom + request.zoom_height);    
    if(request.ping) { sendResponse({pong: true}); return; }
    /* Content script action */
  });