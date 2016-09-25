getSprintGoals = function(){
    
  $.ajax({
    type: "GET",
    url: API_URL + "/getSprintGoals",
    headers: {
      "Authorization": make_base_auth(localStorage.getItem("username"), localStorage.getItem("password"))
    },
    data: { sprint_name: SPRINT_NAME }
  }).done(function (data){
    $(".message").html("Rendering Sprint Goals")
    $("#sprint-goals").html(data)
  })
    
  
}
