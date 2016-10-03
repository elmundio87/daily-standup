try{
  board_name = getUrlParameter("board_name").replace("+"," ")
  $("#loading_image").attr('src','svg/gears.svg')
}
catch(ex){
  $(".message").html(form)
}

$( window ).resize(function() {
  fitToPanel("sprint-actions")
  fitToPanel("sprint-goals")
});

getRapidBoardId(board_name)
