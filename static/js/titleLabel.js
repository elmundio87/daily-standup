setTitleLabel = function(board_id, sprint_id){
  
  $.ajax({
    type: "GET",
    url: API_URL + "/getSprintDaysRemaining",
    headers: {
      "Authorization": make_base_auth(localStorage.getItem("username"), localStorage.getItem("password"))
    },
    data: { board_id: board_id, sprint_id: sprint_id }
  }).done(function (data){
    var today = new Date().toLocaleDateString("en-GB");
    var titleLabel = $("#title-label");
    date = $("<small>");
    
    if(data == "1"){
        date.text(data + " day remaining");
    }
    else{
        date.text(data + " days remaining");
    }
  
    titleLabel.html(SPRINT_NAME + date[0].outerHTML );
  });
  
};
