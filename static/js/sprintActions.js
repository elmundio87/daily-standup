var sprint_actions = ""
var expiring_certs = ""

updateSprintActions = function(){
    $("#sprint-actions").html(sprint_actions + expiring_certs)
    $("#sprint-actions").find("br").remove()
    fitToPanel("sprint-actions")
}

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
    sprint_actions = data
    updateSprintActions()
  })
    
  $.ajax({
    type: "GET",
    url: API_URL + "/getExpiringCertificates",
    data: { board_name: board_name }
  }).done(function (data){
    $(".message").html("Finding expiring certificates")

    json = JSON.parse(data)
    root = $('<ul>')
  
    for (var item in json){
      host = json[item]
      if( host.days_remaining <= 400){
        listitem = $("<li>")
        listitem.css("font-weight", "bold")
        listitem.text("SSL certificate for " + host.hostname + " will expire in " + host.days_remaining  + " days!")
        root.append(listitem)
      }
    }
    
    expiring_certs = root[0].outerHTML
    updateSprintActions()
  })
  
}
