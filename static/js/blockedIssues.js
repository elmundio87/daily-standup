blockedIssuesHandler = function(data){
  
  html = $("#blocked_issue_cards").empty()

  json = JSON.parse(data)
  for (var entry in json.issues) {
    
    issue = json.issues[entry]
    
    card = $('<div>').attr('class','card')
    id_link = $('<a>')
    id_link.attr('target','_blank')
    id_link.attr('href',json.base_url + "/browse/" + issue.key)
    id_link.text(issue.key)
    
    jira_id = $('<div>').attr('class', 'card_jira_id')
    jira_id.append(id_link)
    
    jira_description = $('<div>')
    jira_description.attr('class','card_jira_description')
    jira_description.html(issue.description.replace("Why","</br>Why"))
    
    jira_status = $('<div>')
    jira_status.attr('class','card_jira_status')
    jira_status.text(issue.status)
    if(issue.flagged){
      jira_status.addClass('flagged')
    }
    
    card.append(jira_id)
    card.append(jira_status)
    card.append(jira_description)
    
    html.append(card)
  }
  
  $("#card-container").html(html)
  
}

getBlockedIssues = function(){

  $.get( "/getBlockedIssues", { sprint_name: SPRINT_NAME } )
    .done(function( data ) {
      blockedIssuesHandler(data)
    })
    
}
