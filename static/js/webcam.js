var video = document.querySelector("#videoElement");

function handleVideo(stream) {
	video.src = window.URL.createObjectURL(stream);
}

function videoError(e) {
}

  var videoShouldShow = getUrlParameter('video');

  if(videoShouldShow != "on"){
    $("#videoElement").hide();
  }else{
    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia || navigator.oGetUserMedia;

    if (navigator.getUserMedia) {
    	navigator.getUserMedia({video: true}, handleVideo, videoError);
    }
}
