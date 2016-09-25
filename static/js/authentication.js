function make_base_auth(user, password) {
  var tok = user + ':' + password;
  var hash = btoa(tok);
  return "Basic " + hash;
}

tryLoginFromStoredCredentials = function(){
  if(localStorage.getItem("username") == null || 
    localStorage.getItem("password") == null ||
    localStorage.getItem("username") == "undefined" ||
    localStorage.getItem("password") == "undefined" 
  ){
    window.location.href = 'login.html';
  }
  tryLogin(localStorage.getItem("username"),localStorage.getItem("password"))
}

tryLoginFromSubmitButton = function(){
  tryLogin($("#login_user").val(), $("#login_pass").val(), true)
}

tryLogin = function(username, password, redirect){
  
    redirect = redirect || false;
  
    $.ajax({
      type: "GET",
      url: API_URL + "/",
      headers: {
        "Authorization": make_base_auth(username, password)
      },
    }).done(function(){
      localStorage.setItem("username", username);
      localStorage.setItem("password", password);
      if(redirect){
        window.location.href = 'index.html';
      }
    }).fail(function(){
      window.location.href = 'login.html';
    })
    
}
