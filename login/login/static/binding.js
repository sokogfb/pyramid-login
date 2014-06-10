$("#submit").click(function(){

  var bcrypt = new bCrypt();
  var salt = $("#salt").val();

  if($("#username").val().length < 4){
    return $(".error").html('<div class="alert alert-danger">Username must be at least 4 charcters</div>');
  }

  if($("#password").val().length < 8){
    return $(".error").html('<div class="alert alert-danger">Password must be at least 8 charcters</div>');
  }
  bcrypt.hashpw($("#password").val(), $("#salt").val(), function(hash){
    $("#password").val(hash);
    $("#form_register").submit();
  });

});