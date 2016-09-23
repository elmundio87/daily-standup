var video = document.querySelector("#videoElement");

function handleVideo(stream) {
	video.src = window.URL.createObjectURL(stream);
}

function videoError(e) {
}

  var videoShouldShow = location.search.split('video=')[1] ? location.search.split('video=')[1] : 'true';

  if(videoShouldShow == "false"){
    $("#videoElement").hide();
  }else{
    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia || navigator.oGetUserMedia;

    if (navigator.getUserMedia) {
    	navigator.getUserMedia({video: true}, handleVideo, videoError);
    }
}
