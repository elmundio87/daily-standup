setTitleLabel = function(){
  var today = new Date().toLocaleDateString("en-GB");
  $("#title-label").text(SPRINT_NAME + " - " + today)
}
