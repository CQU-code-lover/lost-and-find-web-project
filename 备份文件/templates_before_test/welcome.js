$(document).ready(function () {
    $("#pic_1,#pic_2,#pic_3").hide();
    $("#pic_1,#pic_2,#pic_3").show("slide",{direction:"up"},1000);
    $("#pic_4,#pic_5,#pic_6").hide();
    $("#pic_4,#pic_5,#pic_6").show("slide",{direction:"down"},1000);
    $("#div_head").hide();
    $("#div_head").show("slide",{direction:"left"},1000);
    $("#word_1,#word_2,#word_3,#word_4").hide();
    setTimeout(function () {
        $("#word_1,#word_2").show("slide",{direction:"up"},1000);
        $("#word_4").fadeIn(1000);
    },1500);
    var animation_word={
        fontSize:"20px",
        top:"+20px"
    };

    setTimeout(function () {
        $("#word_4").animate(animation_word,2000);
    },3000);
    setTimeout(function () {
        $("#word_3").fadeIn(2000);
    },5000);
});
