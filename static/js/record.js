function startUserMedia(stream) {
    var input = audio_context.createMediaStreamSource(stream);
    recorder = new Recorder(input);
};

function startRecording() {
    var constraints = { audio: true, video:false };
    
    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
 	window.AudioContext = window.AudioContext || window.webkitAudioContext;
	var audioContext = new AudioContext();        
        gumStream = stream;
        input = audioContext.createMediaStreamSource(stream);
        rec = new Recorder(input,{numChannels:1});
 
        //start the recording process
        rec.record()
    }).catch(function(err) {
        initialize();
        alert(err);
    });
};

function stopRecording() {
        rec.stop();
        //stop microphone access
        gumStream.getAudioTracks()[0].stop();
        rec.exportWAV(createDownloadLink);
};

function preemptRecording()
{
    if(rec != null)
    {
        rec.stop();
        //stop microphone access
        gumStream.getAudioTracks()[0].stop();
    }
}

function createDownloadLink(blob) {
let socket = new WebSocket("wss://192.168.105.95:2700");

    socket.onopen = function(e) {
      alert("[open] Connection established");
        alert("Sending to server");
          //socket.send("My name is John");
          
	socket.send(blob)
};

    screen.loadBlob(blob);
    url = URL.createObjectURL(blob);
    voice_blob=blob;
};
