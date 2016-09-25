getSprintGoals = function(){
    
  $.ajax({
    type: "GET",
    url: API_URL + "/getSprintGoals",
    headers: {
      "Authorization": make_base_auth(username, password)
    },
    data: { sprint_name: SPRINT_NAME }
  }).done(function (data){
    $("#sprint-goals").html(data)
  })
    
  
}
