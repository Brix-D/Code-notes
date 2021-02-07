$(document).ready(function(){
    // установка ид коммента в скрытый инпут по клику на ссылку "ответить", также установка имени адресата
    $(".reply-link").on("click", function (event){
        event.preventDefault();
        let id_comment = event.target.parentElement.parentElement.getAttribute("data-comment-id");
        let name_author = event.target.parentElement.previousElementSibling.previousElementSibling.firstElementChild.firstElementChild.innerHTML;
        name_author = name_author.slice(0, -1);
        $("#id_parent").attr("value", String(id_comment));
        $("#reply_to_name").html("Ответить " + name_author);
        $("#reply_name_block").show();
    })

    // Удаление ид коммента и подписи имени из формы по клику на крестик
    $("#cancel_reply").on("click", function (event){
        event.preventDefault();
        $("#id_parent").removeAttr("value");
        $("#reply_to_name").html("");
        $("#reply_name_block").hide();
    })

    $("#reply_name_block").hide();
});