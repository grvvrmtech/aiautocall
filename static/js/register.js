$(document).ready(function(){
    $("#submit").click(function(){
        if(check_name() && check_age() && check_mailid())
        {
            $("#error").text("Sending");
            send_register_data();    
        }
    });
});

function send_register_data()
{
    var csrftoken = getCookie('csrftoken');
    var xhr=new XMLHttpRequest();
    xhr.onload=function(e) {
        if(this.readyState === 4) {
            console.log("Server returned: ",e.target.responseText);
        }
    };
   
    xhr.open("GET",'register/',true);
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.setRequestHeader("name", $("#name").val());
    xhr.setRequestHeader("age", $("#age").val());
    xhr.setRequestHeader("gender", $("#gender").val());
    xhr.setRequestHeader("mailid", $("#mailid").val());
    xhr.send();

    xhr.onreadystatechange = function() 
    {
        if (this.readyState == 4 && this.status == 200) 
        {
           $("#error").text(xhr.responseText);
        }
        else
        {
            $("#error").text("Something went wrong. Retry after sometime.");
        }
    };
}


function check_name()
{
    var re = new RegExp("^([a-zA-Z ]{3,30})$");

    if($("#name").val()== "")
    {
        $("#error").text("All fields are mandatory");
        return false;
    }
    else if(!re.test($("#name").val()))
    {
        $("#error").text("Enter a valid name");
        return false;
    }
    return true;
}

function check_age()
{
    var re = new RegExp("^[1-9]?[0-9]{1}$|^100$");
    if($("#age").val()== "")
    {
        $("#error").text("All fields are mandatory");
        return false;
    }
    else if(!re.test($("#age").val()))
    {
        $("#error").text("Enter a valid age");
        return false;
    }
    return true;
}

function check_mailid()
{
    var re = new RegExp("^[a-zA-Z0-9](\.?[a-zA-Z0-9]){3,}@cdot\.in$");
    if($("#mailid").val()== "")
    {
        $("#error").text("All fields are mandatory");
        return false;
    }
    else if(!re.test($("#mailid").val()))
    {
        $("#error").text("Enter a valid mailid");
        return false;
    }
    return true;
}

function getCookie(name) 
{
    var cookieValue = null;
    if (document.cookie && document.cookie != '') 
    {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) 
        {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) 
            {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
