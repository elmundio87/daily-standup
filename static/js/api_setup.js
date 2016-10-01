getSprintName = function(board_id, board_name){

  $.ajax({
    type: "GET",
    url: API_URL + "/getSprintName",
    headers: {
      "Authorization": make_base_auth(localStorage.getItem("username"), localStorage.getItem("password"))
    },
    data: { board_id: board_id, board_name: board_name }
  }).done(function (data){
    SPRINT_NAME = JSON.parse(data)['sprint_name']
    getSprintGoals()
    getBlockedIssues()
    getSprintActions()
    setTitleLabel()
    setInterval(getSprintGoals, 30000)
    setInterval(getBlockedIssues, 30000)
    setInterval(getSprintActions, 30000)
  })

}

getRapidBoardId = function(board_name){

  $.ajax({
    type: "GET",
    url: API_URL + "/getRapidBoardId",
    headers: {
      "Authorization": make_base_auth(localStorage.getItem("username"), localStorage.getItem("password"))
    },
    data: { board_name: board_name },
  }).done(function (data){
    board_id = JSON.parse(data)['board_id']
    getSprintName(board_id, board_name)
  }).fail(function(){
    window.location.href = 'index.html'
  })

}
