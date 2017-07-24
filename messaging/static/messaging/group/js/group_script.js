/**
 * Created by hamid on 7/16/17.
 */


$(document).ready(function(){
    var csrf_token = $('input[name=csrfmiddlewaretoken]').val();

    $("#id_text").keypress(function (e) {
        if(e.which == 13 && !e.shiftKey) {
            e.preventDefault();
            var form = new Object();
            form.text = $("#id_text").val();
            form.group_id = $("#g_id").val();
            $.ajax({
                type: "POST",
                data:$("#msgForm").serialize(),
                url:("/messaging/" + $("#g_id").val() + "/group/"),
                dataType: 'json',
                headers:{
                    'X-CSRFToken' : csrf_token
                },
                success:function(data){
                    location.href ="/messaging/" + $("#g_id").val() + "/group/";
                    //alert($("#msgForm").serialize())
                },
                error: function(err){
                    alert(JSON.stringify(form));
                }
            });
            return false;
        }
    });
    $("#sendButtton").click(function send_message(e){
        e.preventDefault();
        var form = new Object();
        form.text = $("#id_text").val();
        form.group_id = $("#g_id").val();
        $.ajax({
            type: "POST",
            data:$("#msgForm").serialize(),
            url:("/messaging/" + $("#g_id").val() + "/group/"),
            headers:{
                'X-CSRFToken' : csrf_token
            },
            success:function(data){
                location.href ="/messaging/" + $("#g_id").val() + "/group/";
            },
            error: function(err){
                alert('error');
            }
        });
    });
});