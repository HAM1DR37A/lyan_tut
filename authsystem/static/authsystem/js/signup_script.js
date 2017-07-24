/**
 * Created by hamid on 7/17/17.
 */

$(document).ready(function() {
    var csrf_token = $('input[name=csrfmiddlewaretoken]').val();
        $("#formbutton").click(function signup_request(e){
            e.preventDefault();
            if($("#myForm input[name=password]").val() == $("#myForm input[name=password2]").val()) {
                $.ajax({
                    type: "POST",
                    data: $("#myForm").serialize(),
                    url: "/auth/signup/",
                    headers: {
                        'X-CSRFToken': csrf_token
                    },
                    success: function (data) {
                        location.href = "/auth/login/";
                    },
                    error: function (err) {
                        alert($("#myForm").serialize());
                    }
                });
            }else{
                alert("password didn't match!");
            }
            });
    });