getRapidBoardId = function(board_name){
$.ajax({
  type: "GET",
  url: API_URL + "/getRapidBoardId",
  headers: {
    "Authorization": make_base_auth(localStorage.getItem("username"), localStorage.getItem("password"))
  },
  data: { board_name: board_name },
}).done(function (data){
  board_id = JSON.parse(data)['board_id']
  getSprintName(board_id, board_name)
}).fail(function(){
  window.location.href = 'index.html'
})
    
}

getSprintName = function(board_id, board_name){

  $.ajax({
    type: "GET",
    url: API_URL + "/getSprintName",
    headers: {
      "Authorization": make_base_auth(localStorage.getItem("username"), localStorage.getItem("password"))
    },
    data: { board_id: board_id, board_name: board_name }
  }).done(function (data){
    SPRINT_NAME = JSON.parse(data)['sprint_name']
    getSprintGoals()
    getBlockedIssues()
    setTitleLabel()
    setInterval(getSprintGoals, 30000)
    setInterval(getBlockedIssues, 30000)
  })
  
}

tryLoginFromStoredCredentials()

try{
  board_name = getUrlParameter("board_name").replace("+"," ")
  $("#loading_image").attr('src','svg/gears.svg')
}
catch(ex){
  form = $('<form>')
  form.attr("action","index.html")
  textbox = $('<input>')
  textbox.attr('list','boards')
  textbox.attr('name','board_name')
  textbox.attr('placeholder',"Board Name")
  submit = $('<input>')
  submit.attr('type', 'submit')
  submit.attr('value','Submit')
  
  legend = $('<legend>')
  legend.text('Choose Sprint Board')
  
  videoLabel = $('<label>')
  videoCheckbox = $('<input>')
  videoCheckbox.attr("type","checkbox")
  videoCheckbox.attr("name","video")
  videoCheckbox.attr("checked","checked")
  
  videoLabel.append(videoCheckbox)
  videoLabel.append("Mirror Webcam")
  
  datalist = $('<datalist>')
  datalist.attr('id','boards')
  option1 = $('<option>')
  option1.attr('value','Pack 1')
  option2 = $('<option>')
  option2.attr('value','Pack 2')
  
  datalist.append(option1)
  datalist.append(option2)
  
  form.append(legend)
  form.append(videoLabel)
  form.append($('<br>'))
  form.append(textbox)
  form.append(datalist)
  form.append(submit)
  
  $(".message").html(form)
}

getRapidBoardId(board_name)
