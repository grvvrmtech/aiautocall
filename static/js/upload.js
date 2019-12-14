function upload_file()
{
    //upload the blob
    var csrftoken = getCookie('csrftoken');
    var xhr=new XMLHttpRequest();
    xhr.onload=function(e) {
        if(this.readyState === 4) {
            console.log("Server returned: ",e.target.responseText);
        }
    };
    
    xhr.open("POST","upload/",true);
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.setRequestHeader("text", encodeURI($("#keyword").val()));
    //xhr.setRequestHeader("id", id);
    xhr.send(voice_blob);

    xhr.onreadystatechange = function() 
    {
        if (this.readyState == 4 && this.status == 200) 
        {
           $("#random_text").text("Voice Uploaded Successfully...Press Next to Continue");
        }
        else
        {
            $("#random_text").text("Something went wrong. Retry after sometime");
        }
    };
};

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
