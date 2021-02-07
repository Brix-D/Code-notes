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