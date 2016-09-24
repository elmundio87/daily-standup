getSprintGoals = function(){

  $.get( API_URL + "/getSprintGoals", { sprint_name: SPRINT_NAME } )
    .done(function( data ) {
      $("#sprint-goals").html(data)
    })
  
}
