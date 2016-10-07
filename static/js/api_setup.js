getSprintName = function(board_id, board_name){

  $.ajax({
    type: "GET",
    url: API_URL + "/getSprintName",
    headers: {
      "Authorization": make_base_auth(localStorage.getItem("username"), localStorage.getItem("password"))
    },
    data: { board_id: board_id, board_name: board_name }
  }).done(function (data){
    SPRINT_NAME = JSON.parse(data).sprint_name;
    SPRINT_ID = JSON.parse(data).sprint_id;
    getSprintGoals();
    getBlockedIssues();
    getSprintActions();
    setTitleLabel(board_id, SPRINT_ID);
  });

};

getRapidBoardId = function(board_name){

  $.ajax({
    type: "GET",
    url: API_URL + "/getRapidBoardId",
    headers: {
      "Authorization": make_base_auth(localStorage.getItem("username"), localStorage.getItem("password"))
    },
    data: { board_name: board_name },
  }).done(function (data){
    board_id = JSON.parse(data).board_id;
    getSprintName(board_id, board_name);
  }).fail(function(){
    window.location.href = 'index.html';
  });

};
