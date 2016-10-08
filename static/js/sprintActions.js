var sprint_actions = "Loading Sprint Actions...";
var expiring_certs = "Loading SSL certs...";
var report_link = $("<a>");
    
report_link.text("View all SSL Certs");
report_link.attr('target',"_blank");
report_link.attr('href',"ssl_certs.html?board_name=" + getUrlParameter("board_name") );
expiring_certs += report_link[0].outerHTML;


updateSprintActions = function(){
    $("#sprint-actions").html(sprint_actions + expiring_certs);
    $("#sprint-actions").find("br").remove();
    fitToPanel("sprint-actions");
};

getSprintActions = function(){
    
  getLastSprintName = function(sprint_name){
    sprint_name = sprint_name.replace("#","");
    sprint_name_words = sprint_name.split(" ");
    
    sprint_name_prefix = sprint_name_words.slice(0, sprint_name_words.length - 1).join(" ");
    
    sprint_number = sprint_name_words[sprint_name_words.length - 1];
    last_sprint_number = sprint_number - 1;
    
    return sprint_name_prefix + " " + last_sprint_number;
  };
  
  $.ajax({
    type: "GET",
    url: API_URL + "/getSprintActions",
    headers: {
      "Authorization": make_base_auth(localStorage.getItem("username"), localStorage.getItem("password"))
    },
    data: { sprint_name: getLastSprintName(SPRINT_NAME) }
  }).done(function (data){
    sprint_actions = data;
    updateSprintActions();
  });
    
  $.ajax({
    type: "GET",
    url: API_URL + "/getExpiringCertificates",
    data: { board_name: board_name }
  }).done(function (data){

    json = JSON.parse(data);
    root = $('<ul>');
  
    for (var item in json){
      host = json[item];
      
      listitem = $("<li>");
      listitem.css("font-weight", "bold");
      listitem.append("SSL cert for ");
      link = $("<a>");
      link.text(host.hostname);
      link.attr('href',"https://" + host.hostname);
      link.attr('target',"_blank");
      listitem.append(link);
      
      if( host.error !== ""){
        listitem.attr('title',host.error);
        listitem.addClass("ssl_error");
        listitem.text("");
        listitem.append(link);
        if(host.error.indexOf("Connection refused") !== -1){
          listitem.append(" IS OFFLINE");
        }else{
          listitem.append(" HAS AN INVALID SSL CERTIFICATE!");
        }
        root.append(listitem);
      }
      else if(host.days_remaining <= 0){
          listitem.append(" HAS EXPIRED!!!");
          root.append(listitem);
      }
      else if( host.days_remaining <= 30){
        listitem.append(" will expire in " + host.days_remaining  + " days!");
        root.append(listitem);
      }
      
    }
    
    expiring_certs = root[0].outerHTML + report_link[0].outerHTML;
    updateSprintActions();
  });
  
};
