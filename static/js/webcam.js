var video = document.querySelector("#webcam");
var videoShouldShow = getUrlParameter('video');

if(videoShouldShow != "on"){
  $("#webcam").hide();
  $("#panel-sprint-goals").addClass("no-webcam");
  $("#panel-sprint-actions").addClass("no-webcam");
}else{
  navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia || navigator.oGetUserMedia;

  if (navigator.getUserMedia) {
  	navigator.getUserMedia({video: true}, handleVideo, videoError);
  }else{
    $("#webcam").hide();
    $("#panel-sprint-goals").addClass("no-webcam");
    $("#panel-sprint-actions").addClass("no-webcam");
  }
	
}

function handleVideo(stream) {
	video.src = window.URL.createObjectURL(stream);
}

function videoError(e) {
}

$("#webcam").click(function(){
	if (navigator.getUserMedia) {
		navigator.getUserMedia({video: true}, handleVideo, videoError);
	}
});
