getRapidBoardId = function(board_name){
$.get( API_URL + "/getRapidBoardId", { board_name: board_name } )
  .done(function( data ) {

      board_id = JSON.parse(data)['board_id']
      getSprintName(board_id, board_name)

  })
}

getSprintName = function(board_id,board_name){
$.get( API_URL + "/getSprintName", { board_id: board_id, board_name: board_name } )
  .done(function( data ) {
    SPRINT_NAME = JSON.parse(data)['sprint_name']
    getSprintGoals()
    getBlockedIssues()
    setTitleLabel()
    setInterval(getBlockedIssues, 30000)
  })
}

try{
  board_name = getUrlParameter("board_name").replace("+"," ")
}
catch(ex){
  form = $('<form>')
  form.attr("action","index.html")
  textbox = $('<input>')
  textbox.attr('type','text')
  textbox.attr('name','board_name')
  textbox.attr('placeholder',"Board Name")
  submit = $('<input>')
  submit.attr('type', 'submit')
  submit.attr('value','Submit')
  
  form.append(textbox)
  form.append(submit)
  
  $(".message").html(form)
}

getRapidBoardId(board_name)
