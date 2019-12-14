function initialize()
{   
    clearInterval(timer);
    preemptRecording();
    rec = null;

    enableButton($("#record"));
    disableButton($("#play"));
    disableButton($("#pause"));
    disableButton($("#stop"));
    disableButton($("#upload"));
    disableButton($("#refresh"));

    $("#record").unbind('click');
    $("#record").click(function(){  
        disableButton($("#record"));
        disableButton($("#play"));
        disableButton($("#pause"));
        enableButton($("#stop"));
        disableButton($("#upload"));
        disableButton($("#refresh"));
        record();
    });
    screen.empty();
};

function record()
{
    startRecording();
    blink(1000);

    $("#stop").unbind('click');
    $("#stop").click(function(){  
        disableButton($("#record"));
        enableButton($("#play"));
        disableButton($("#pause"));
        disableButton($("#stop"));
        enableButton($("#upload"));
        enableButton($("#refresh"));
        stop_record();
    });
};

function stop_record()
{
    clearInterval(timer);
    stopRecording();
    rec = null;

    $("#play").unbind('click');
    $("#play").click(function(){  
        disableButton($("#record"));
        disableButton($("#play"));
        enableButton($("#pause"));
        enableButton($("#stop"));
        start_playing();
    });

    $("#refresh").unbind('click');
    $("#refresh").click(function(){  
        initialize();
    });

    $("#upload").unbind('click');
    $("#upload").click(function(){
        disableButton($("#record"));
        disableButton($("#upload"));
        disableButton($("#refresh"));  
        upload_file();
    });
};

function start_playing()
{
    screen.play();
    screen.on('finish',function(){
        disableButton($("#record"));
        enableButton($("#play"));
        disableButton($("#pause"));
        disableButton($("#stop"));
        stop_playing();
    });
    $("#pause").unbind('click');
    $("#pause").click(function(){  
        disableButton($("#record"));
        enableButton($("#play"));
        disableButton($("#pause"));
        enableButton($("#stop"));
        pause_playing();
    });

    $("#stop").unbind('click');
    $("#stop").click(function(){  
        disableButton($("#record"));
        enableButton($("#play"));
        disableButton($("#pause"));
        disableButton($("#stop"));
        stop_playing();
    });
};

function pause_playing()
{
    screen.pause();
    $("#play").unbind('click');
    $("#play").click(function(){  
        disableButton($("#record"));
        disableButton($("#play"));
        enableButton($("#pause"));
        enableButton($("#stop"));
        start_playing();
    });
};

function stop_playing()
{
    screen.stop();
    $("#play").unbind('click');
    $("#play").click(function(){  
        disableButton($("#record"));
        disableButton($("#play"));
        enableButton($("#pause"));
        enableButton($("#stop"));
        start_playing();
    });
};

function new_page()
{
    initialize();
    //set_text();
};

function blink(interval){
    timer = window.setInterval(function(){
        $("#record").css("opacity", "0");
        window.setTimeout(function(){
            $("#record").css("opacity", "0.5");
        }, 150);
    }, interval);
}
