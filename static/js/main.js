function page() {
    var id_js=document.getElementById("page_input");
    var inner=id_js.innerHTML;
    if inner=='None'{
        alert('请输入页数后尝试')
    }
    else{
        window.location.href='/'+inner
    }
}
