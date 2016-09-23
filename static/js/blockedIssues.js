blockedIssuesHandler = function(data){
  
  html = $('<div>')
  debugger
  json = JSON.parse(data)
  for (var entry in json) {
    
    issue = json[entry]
    
    card = $('<div>').attr('class','card')
    id_link = $('<a>')
    id_link.attr('target','_blank')
    id_link.attr('href',issue.key)
    id_link.text(issue.key)
    
    jira_id = $('<div>').attr('class', 'card_jira_id')
    jira_id.append(id_link)
    
    jira_description = $('<div>')
    jira_description.attr('class','card_jira_description')
    jira_description.html(issue.description.replace("Why","</br>Why"))
    
    jira_status = $('<div>')
    jira_status.attr('class','card_jira_status')
    jira_status.text(issue.status)
    
    card.append(jira_id)
    card.append(jira_status)
    card.append(jira_description)
    
    html.append(card)
  }
  $(".card-container").html(html)
}

$.ajax({
  url: "/getBlockedIssues"
}).done(function(data) { 
  blockedIssuesHandler(data)
});
