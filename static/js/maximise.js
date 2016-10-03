$(".panel-heading").click(function(){
  $(this).parent().toggleClass("maximise")
  fitToPanel("sprint-actions")
  fitToPanel("sprint-goals")
})
