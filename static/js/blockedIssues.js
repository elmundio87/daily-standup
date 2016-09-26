blockedIssuesHandler = function(data){
  
  blocked_issue_cards = $("#blocked_issue_cards").clone().empty()
  with_customer_issue_cards = $("#with_customer_issue_cards").clone().empty()

  json = JSON.parse(data)
  
  if(json.hasOwnProperty('error')){
    $("#blocked_issue_cards").text(json['error'])
    return
  }
  
  for (var entry in json.issues) {
    
    issue = json.issues[entry]
    
    
    if(issue.status == "With Customer"){
      card = $('<div>').attr('class','minicard')
      id_link = $('<a>')
      id_link.attr('target','_blank')
      id_link.attr('href',json.base_url + "/browse/" + issue.key)
      id_link.text(issue.key)
      
      jira_id = $('<div>').addClass("jira_id")
      jira_id.append(id_link)
      
      jira_description = $('<div>').addClass("jira_description")
      jira_description.html(issue.description)
      
      with_customer_issue_cards.append(card)
      
      card.append(jira_id)
      card.append(jira_description)
      
      
    }else{
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
      blocked_issue_cards.append(card)
    }
    
  }
  
  if( blocked_issue_cards.html() != $("#blocked_issue_cards").html()){
    $("#blocked_issue_cards").html(blocked_issue_cards.html())
  }
  
  if( with_customer_issue_cards.html() != $("#with_customer_issue_cards").html()){
    $("#with_customer_issue_cards").html(with_customer_issue_cards.html())
  }
  
}

getBlockedIssues = function(){

  $.ajax({
    type: "GET",
    url: API_URL + "/getBlockedIssues",
    headers: {
      "Authorization": make_base_auth(localStorage.getItem("username"), localStorage.getItem("password"))
    },
    data: { sprint_name: SPRINT_NAME }
  }).done(function (data){
    blockedIssuesHandler(data)
    $(".message").html("Rendering Blocked Issues")
    $("#loader").addClass("invisible")
  })
      
}
