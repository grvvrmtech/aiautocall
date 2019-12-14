URL = window.URL || window.webkitURL;
 
var gumStream; //stream from getUserMedia()
var rec = null; //Recorder.js object
var input; //MediaStreamAudioSourceNode we'll be recording
 
// shim for AudioContext when it's not avb. 
var AudioContext;
var audioContext;
var screen;
var url;
var timer;
var voice_blob;
var last_text_num = 0;
var id;

$(document).ready(function(){

//var AudioContext = window.AudioContext || window.webkitAudioContext;
//window.AudioContext = window.AudioContext || window.webkitAudioContext;
//var audioContext = new AudioContext(); //new audio context to help us record
    screen = WaveSurfer.create({
        container: '#waveform',
        waveColor: '#5DBCD2',
        progressColor: '#5d96d2'
    });

    //var key = prompt("Please enter your key", "").trim();

    var csrftoken = getCookie('csrftoken');
    new_page(); 

    let socket = new WebSocket("wss://192.168.105.95:8000/client/ws/speech");

    socket.onopen = function(e) {
      alert("[open] Connection established");
        alert("Sending to server");
	  //socket.send("My name is John");
	  };

	  socket.onmessage = function(event) {
	    alert(`[message] Data received from server: ${event.data}`);
	    };

	    socket.onclose = function(event) {
	      if (event.wasClean) {
	          alert(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
		    } else {
		        // e.g. server process killed or network down
			//     // event.code is usually 1006 in this case
			alert('[close] Connection died');
			           }
			           };
			
			           socket.onerror = function(error) {
			             alert(`[error] ${error.message}`);
			             };
    
    
    /*var xhr=new XMLHttpRequest();
    xhr.onload=function(e) {
        if(this.readyState === 4) 
        {
            if(e.target.responseText == "Success")
            {
                id = this.getResponseHeader('id')
                $("#next").click(function(){  
                    new_page();
                });
                new_page();
            }
            else
            {
                alert("Incorrect key, refresh to retry");
            }
        }
    };
    
    xhr.open("GET","check_key/",true);
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
    xhr.setRequestHeader("key", key);
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
    };*/
});

