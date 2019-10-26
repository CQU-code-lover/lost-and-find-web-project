var innerPart=15;
var state='yes';
var length=8;
var infArry=[[87, '0', [2019, 8, 13, 17, 51, 38], '/static/things_inf_pic/1545998900.png', '/user/1209895097', 'title'], [103, '1', [2019, 1, 1, 17, 14, 21], '/static/things_inf_pic/no_pic.png', '/user/1209895097', '丢失一只居儿虫'], [104, '1', [2019, 1, 1, 17, 14, 50], '/static/things_inf_pic/no_pic.png', '/user/1209895097', '丢失一只居儿虫'], [105, '3', [2019, 1, 1, 17, 16, 8], '/static/things_inf_pic/15.jpeg', '/user/1209895097', '丢失一只居儿虫'],[87, '0', [2019, 8, 13, 17, 51, 38], '/static/things_inf_pic/154600365812098.png', '/user/1209895097', 'title'], [103, '1', [2019, 1, 1, 17, 14, 21], '/static/things_inf_pic/no_pic.png', '/user/1209895097', '丢失一只居儿虫'], [104, '1', [2019, 1, 1, 17, 14, 50], '/static/things_inf_pic/no_pic.png', '/user/1', '丢失一只居儿虫'], [105, '3', [2019, 1, 1, 17, 16, 8], '/static/things_inf_pic/1545998900.jpeg', '/user/1209895097', '丢失一只居儿虫'],[87, '0', [2019, 8, 13, 17, 51, 38], '/static/things_inf_pic/15460036581209895097.png', '/user/1209895097', 'title'], [103, '1', [2019, 1, 1, 17, 14, 21], '/static/things_inf_pic/no_pic.png', '/user/1209895097', '丢失一只居儿虫'], [104, '1', [2019, 1, 1, 17, 14, 50], '/static/things_inf_pic/no_pic.png', '/user/1209895097', '丢失一只居儿虫'], [105, '3', [2019, 1, 1, 17, 16, 8], '/static/things_inf_pic/15463341681209895097.jpeg', '/user/1209895097', '丢失一只居儿虫']]
var probe=0;
var heightArry=[];
if (window.screen.width>768) {
    heightArry = [0, 0, 0, 0];
    var boxWidth = (window.screen.width*0.8 - innerPart * 3) / 4;
}
else{
    heightArry = [0, 0];
    var boxWidth = (window.screen.width*0.8 - innerPart) / 2;
}
// 盒子的初始化函数
function box_start(js_object) {
    // 初始化日期显示位置
    setStyleByObject(js_object,'width',boxWidth);
    var box_js_needChange=js_object.children[2].children[2];
    var box_js_leftTwoBox1=js_object.children[2].children[0];
    var box_js_leftTwoBox2=js_object.children[2].children[1];
    setStyleByObject(box_js_needChange,'left',boxWidth-box_js_needChange.offsetWidth-box_js_leftTwoBox1.offsetWidth-box_js_leftTwoBox2.offsetWidth+"px");
    js_object.setAttribute(
        "mouseover","mouseOver(this);",
        "mouseout","mouserOut(this)"
    )
}
function setStyleByObject(object,seted,value) {
    object.style.setProperty(
        seted,value
    )
}




// 节点生成器：1.生成节点2.添加到父节点中3.初始化节点（使用box_start函数）4.调整probe后移
function newBoxNode(){
   var newNode=document.createElement("div");
   newNode.className="inf_box";
   document.getElementById('div_main_inf').appendChild(newNode);
   var newNode1=document.createElement("div");
   newNode.appendChild(newNode1);
   var newNode2=document.createElement("div");
   newNode2.className="title";
   newNode.appendChild(newNode2);
   var newNode3=document.createElement("div");
   newNode3.className="inf_foot";
   newNode.appendChild(newNode3);
   var newNode11=document.createElement("div");
   newNode1.appendChild(newNode11);
   var newNode111=document.createElement("img");
   newNode111.className="box_img";
   newNode11.appendChild(newNode111);
   var newNode21=document.createElement("a");
   newNode2.appendChild(newNode21);
   var newNode31=document.createElement("div");
   newNode31.className="look_times";
   newNode3.appendChild(newNode31);
   var newNode32=document.createElement("div");
   newNode32.className="star";
   newNode3.appendChild(newNode32);
   var newNode33=document.createElement("div");
   newNode33.className="release_time";
   newNode3.appendChild(newNode33);
   var newNode311=document.createElement("span");
   newNode311.className="glyphicon glyphicon-eye-open";
   newNode31.appendChild(newNode311);
   var newNode321=document.createElement("span");
   newNode321.className="glyphicon glyphicon-star";
   newNode32.appendChild(newNode321);
   var newNode331=document.createElement("span");
   newNode331.className="glyphicon glyphicon-calendar";
   newNode33.appendChild(newNode331);

   // 节点信息设置

   newNode111.setAttribute(
       "src",".."+infArry[probe][3]
   );
   newNode21.setAttribute(
       "href","things/"+infArry[probe][0]
   );
   newNode21.innerHTML=infArry[probe][5];
   newNode311.innerHTML=infArry[probe][1];
   newNode321.innerHTML="0";
   var timeArry=infArry[probe][2];
   newNode331.innerHTML=timeArry[0]+"-"+timeArry[1]+"-"+timeArry[2];
   // 后移指针
   probe+=1;
   box_start(newNode);
   return newNode
}

// 调整尾部div的位置 内嵌到节点定位中 在每次生成新节点后调用 调整body的高度
function changePositionFoot() {
    var maxHeight= minAndMax()[3]+document.getElementById("div_head").offsetHeight+document.getElementById("div_main_head").offsetHeight;
    var body_js=document.getElementsByTagName("body")[0];
    // 这是两个head的高度和
    var headHeight=document.getElementById("div_head").offsetHeight+document.getElementById("div_main_head").offsetHeight;
    setStyleByObject(document.getElementById("div_foot"),"top",maxHeight+"px");
    setStyleByObject(body_js,"height",headHeight+minAndMax()[3]+"px")
}



// 返回结构：Arry    [最短的列序号，最短的列数据，最长的列序号，最长的列数据]
function minAndMax(){
    if (heightArry.length==4){
        var minColumn=0;
        var minData=0;
        var maxColumn=0;
        var maxData=0;
        for(var i=1;i<=4;i++) {
            if (heightArry[minColumn] > heightArry[i]) {
                minColumn = i
            }
        }
        for(var j=1;j<=4;j++){
            if (heightArry[maxColumn]<heightArry[j])
            {
                maxColumn=j
            }
        }
        return [minColumn+1,heightArry[minColumn],maxColumn+1,heightArry[maxColumn]]
    }


    else{
        if (heightArry[0]<heightArry[1]){
            return [1,heightArry[0],2,heightArry[1]]
        }
        else{
            return [2,heightArry[1],1,heightArry[0]]
        }
    }
}
// 1.固定位置 2.更新heightArry数组   3.调用方法来设置div_foot的位置

function setElementPosition(objElement,column) {
    var positionY=heightArry[column-1];
    var positionX=(column-1)*boxWidth+innerPart;
    setStyleByObject(objElement,"top",positionY+"px");
    setStyleByObject(objElement,"left",positionX+"px");
    heightArry[column-1]+=objElement.offsetHeight+innerPart;
    changePositionFoot()
}

function IfloadNewNodes() {
    if (probe!=infArry.length-1){
        if (window.scrollTop+window.body.clientHeight>=minAndMax()[3]+50){
            return true
        }

    }
    else{
        document.getElementById("div_foot").innerHTML="暂无更多内容";
        return false
    }
}
$(document).ready(
    function () {
        if (window.screen.width>768){
            if (state=='yes'){
                if (length>=5){
                    var onloadValue=true;
                    for (var i=0;i<=3;i++){
                        setElementPosition(newBoxNode(),minAndMax()[0]);
                    }
                    while(IfloadNewNodes){
                        if(probe==infArry.length-1){
                            document.getElementById("div_foot").innerHTML="暂无更多内容";
                            onloadValue=false;
                            break
                        }
                        setElementPosition(newBoxNode(),minAndMax()[0])
                    }
                    window.onscroll=function () {
                        if (onloadValue&&IfloadNewNodes){
                            // 进行批量加载
                            for(var k=0;k<=9;k++){
                                if (probe==infArry.length-1){
                                    document.getElementById("div_foot").innerHTML="暂无更多内容";
                                    onloadValue=false;
                                    break
                                }
                                setElementPosition(newBoxNode(),minAndMax()[0])
                            }
                        }
                    }
                }
                else{
                    for(var j=0;j<=infArry.length-1;j++){
                        setElementPosition(newBoxNode(),minAndMax()[0]);
                        document.getElementById("div_foot").innerHTML="暂无更多内容"
                    }
                }
            }
            else{
                document.getElementById("div_foot").innerHTML="没有搜索到结果 请输入其他关键词重试"
            }
        }
        else{
            heightArry=[0,0]
        }
    }
);
// hover变换的函数 test版本不使用
function mouserOver(objElement) {

}
function mouserOut(objElement) {

}

function showBackgroundDiv(){
    setStyleByObject(document.getElementById("back_helper_div"),"display","block")
}
function unshowBackgroundDiv() {
    setStyleByObject(document.getElementById("back_helper_div"),"display","none")
}