setTitleLabel = function(){
  var today = new Date().toLocaleDateString("en-GB");
  var titleLabel = $("#title-label")
  date = $("<small>")
  date.text(today)
  titleLabel.html(SPRINT_NAME + date[0].outerHTML)
  
}
