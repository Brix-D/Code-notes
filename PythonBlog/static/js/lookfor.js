function FuncSuccess(result) {
    let result_block = document.getElementById("res");
    while(result_block.firstChild) {
        result_block.removeChild(result_block.firstChild);
    }
    if(typeof result !== "object") { //Если реузльтат не пустой JSON-объект
    result = JSON.parse(result) //то парсить его в JSON

    if (result != null) {
        result.forEach(function(value) {
            let p = document.createElement("p");
            let a = document.createElement("a");
            result_block.append(p);
            p.append(a);
            a.innerHTML = value["fields"]["title"];
            a.href = "/note/view/"+value["pk"];
        });
        }
    }
    if (result_block.firstChild == null) {
        result_block.classList.add("invisible");
    } else {
        result_block.classList.remove("invisible");
    }
}

//function FailFunc(result) {
//    let result_block = document.getElementById("res");
//    while(result_block.firstChild) {
//        result_block.removeChild(result_block.firstChild);
//    }
//    if (result_block.firstChild == null) {
//        result_block.classList.add("invisible");
//    } else {
//        result_block.classList.remove("invisible");
//    }
//}


//Получить куки по указанному имени
//https://stackoverflow.com/questions/6506897/csrf-token-missing-or-incorrect-while-post-parameter-via-ajax-in-django
function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

//AJAX-для поиска по одному слову
//$(document).ready(
//    function(){
//        $("#oneword").bind("input", function()
//        {
//            var value = document.getElementById("oneword").value;
////            $.ajaxSetup({
////
////            });
//            $.ajax ({
//                headers: { "X-CSRFToken": getCookie('csrftoken') }, //Отправка CSRF-токена заголовком
//                url: "searchone",
//                type: "post",
//                data: {one: value},
//                dataType: "json",
//                success: FuncSuccess,
//                //error: FailFunc
//            });
//        });
//    });

$(document).ready(
    function(){
        $("#multyword").bind("input", function()
        {
            var value = document.getElementById("multyword").value;
            $.ajax ({
                headers: { "X-CSRFToken": getCookie('csrftoken') },
                url: $('#search').attr('action'),
                type: "post",
                data: ({multy: value}),
                dataType: "json",
                success: FuncSuccess,
                //error: FailFunc
            });
        });
    });