function disableButton(button) {

    $(button).css('opacity',0.5);
    $(button).unbind();
};

function enableButton(button) {

    $(button).css('opacity',1);

    $(button).hover(function(){
        $(this).css('opacity',0.85);
    },function(){
        $(this).css('opacity',1);
    });
};