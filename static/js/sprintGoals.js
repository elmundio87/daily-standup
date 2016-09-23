$.ajax({
  url: "/getSprintGoals"
}).done(function(data) { 
  $(".sprint-goals").html(data)
});
