var video = document.querySelector("#webcam");

function handleVideo(stream) {
	video.src = window.URL.createObjectURL(stream);
}

function videoError(e) {
}

  var videoShouldShow = getUrlParameter('video');

  if(videoShouldShow != "on"){
    $("#webcam").hide();
  }else{
    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia || navigator.oGetUserMedia;

    if (navigator.getUserMedia) {
    	navigator.getUserMedia({video: true}, handleVideo, videoError);
    }
}
