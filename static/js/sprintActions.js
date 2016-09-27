getSprintActions = function(){
    
  getLastSprintName = function(sprint_name){
    sprint_name = sprint_name.replace("#","")
    sprint_name_words = sprint_name.split(" ")  
    
    sprint_name_prefix = sprint_name_words.slice(0, sprint_name_words.length - 1).join(" ")
    
    sprint_number = sprint_name_words[sprint_name_words.length - 1]  
    last_sprint_number = sprint_number - 1
    
    return sprint_name_prefix + " " + last_sprint_number 
  }  
  
  $.ajax({
    type: "GET",
    url: API_URL + "/getSprintActions",
    headers: {
      "Authorization": make_base_auth(localStorage.getItem("username"), localStorage.getItem("password"))
    },
    data: { sprint_name: getLastSprintName(SPRINT_NAME) }
  }).done(function (data){
    $(".message").html("Rendering Sprint Actions")
    $("#sprint-actions").html(data)
  })
    
  
}
