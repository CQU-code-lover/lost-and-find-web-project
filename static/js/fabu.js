// 主要用于响应操作  注：尺寸位置配置内嵌在html中
$(document).ready(function () {
    // 部署chageDate()函数到日期选择列
    var choiceMonth_js=document.getElementById("choice_the_month").children;
    var choiceDay_js=document.getElementById("choice_the_day").children;
    for(var m=0;m<choiceMonth_js.length-1;m++){
        choiceMonth_js[m].style.setProperty("cursor","pointer");
        choiceMonth_js[m].setAttribute("onclick","changeDate(this)");
    }

    for(var n=0;n<choiceMonth_js.length-1;n++){
        choiceDay_js[n].setAttribute("style","cursor:pointer");
        choiceDay_js[n].setAttribute("onclick","changeDate(this)");
    }
});
function fabu() {
    alert("请在发布后分享")
}
function changeActive(id) {
    var lost_js=document.getElementById("lost");
    var find_js=document.getElementById("find");
    var type_js=document.getElementById("type");
    click_js=lost_js;
    noclick_js=find_js;
    if (id.id=="find"){
        click_js=find_js;
        noclick_js=lost_js
    }
    noclick_js.classList.remove("active");
    if(!click_js.classList.contains("active")){
        click_js.classList.add("active")
    }

    if(find_js.classList.contains("active")){
        type_js.value="find"
    }
    else{
        type_js.value="lost"
    }
}
function changeDate(js) {
    var mydate=new Date();
    var yue=mydate.getMonth()+1; /*Be careful! There must have a bug which return a wrong month value(smaller than the real value,by David)*/
    var ri=mydate.getDate();
    var yue_js=document.getElementById("yue");
    var ri_js=document.getElementById('ri');
    if(js.innerHTML=="本月"){
        yue_js.value=yue;
    }
    if (js.innerHTML=="今日"){
        ri_js.value=ri;
    }
    if (js.tagName=="A"){
        if (js.parentNode.id=="choice_the_month"){
            yue_js.value=js.innerHTML;
        }
        else{
            ri_js.value=js.innerHTML;
        }
    }
}

function cheakForm(js) {
    var state_value=true;
    var alert_str="";
    var k1=document.getElementById("form_title").value,
        k2=document.getElementById("place").value,
        k3=document.getElementById("form_title").value,
        k4=document.getElementById("connect_way").value,
        k5=document.getElementById("yue").value,
        k6=document.getElementById("ri").value,
        k7=document.getElementById("textarea").value;
    if ((!document.getElementById("lost").classList.contains("active"))&&(!document.getElementById("find").classList.contains("active"))){
        state_value=false;
        alert_str+="请选择信息类型\n"
    }
    if(k1==''){
        state_value=false;
        alert_str+="标题不能为空\n"
    }
    if(k2==''){
        state_value=false;
        alert_str+="地点不能为空\n"
    }

    if(k3==''){
        state_value=false;
        alert_str+="标题不能为空\n"
    }
    if(k4==''){
        state_value=false;
        alert_str+="联系方式不能为空\n"
    }
    if((k5=='')||(k6=='')){
        state_value=false;
        alert_str+="请填写完整日期\n"
    }
    if(k7==''){
        state_value=false;
        alert_str+="描述不能为空\n"
    }
    if (!state_value){
        alert(alert_str);
        return false;
    }
    alert(提交成功);
    return true
}