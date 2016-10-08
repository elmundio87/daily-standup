getSprintGoals = function(){
    
  $.ajax({
    type: "GET",
    url: API_URL + "/getSprintGoals",
    headers: {
      "Authorization": make_base_auth(localStorage.getItem("username"), localStorage.getItem("password"))
    },
    data: { sprint_name: SPRINT_NAME }
  }).done(function (data){
    $("#sprint-goals").html(data);
    $("#sprint-goals").find("br").remove();
    fitToPanel("sprint-goals");
  });
    
  
};
