function set_text()
{
    var csrftoken = getCookie('csrftoken');
    var xhr=new XMLHttpRequest();
    xhr.onload=function(e) {
        if(this.readyState === 4) {
            console.log("Server returned: ",e.target.responseText);
        }
    };
    
    xhr.open("GET","get_text/",true);
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.setRequestHeader("num", last_text_num);
    xhr.send();

    xhr.onreadystatechange = function() 
    {
        if (this.readyState == 4 && this.status == 200) 
        {
           $("#random_text").text(xhr.responseText);
           last_text_num = this.getResponseHeader('num')
        }
        else
        {
            $("#random_text").text("Something went wrong. Retry after sometime.");
        }
    };
}