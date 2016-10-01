try{
  board_name = getUrlParameter("board_name").replace("+"," ")
  $("#loading_image").attr('src','svg/gears.svg')
}
catch(ex){
  $(".message").html(form)
}

getRapidBoardId(board_name)
