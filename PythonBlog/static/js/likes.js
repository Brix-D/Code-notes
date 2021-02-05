function check_liked() {
    let article_id = $("#article-id").text();
    $.ajax({
        headers: { "X-CSRFToken": getCookie('csrftoken') },
        type: "POST",
        dataType: "json",
        url: "/likes/check/"+article_id,
        data: {},
        success: function (result) {
            if (result["status"] == true) {
                $("#like").addClass("error");
                $("#like").attr("href", "/likes/unlike/" + article_id);
                $("#like").html("Дизлайк");
            }
            else {
                $("#like").removeClass("error");
                $("#like").attr("href", "/likes/like/" + article_id);
                $("#like").html("Лайк");
            }
        },
    });
}

$(document).ready(
    function () {
        $("#like").click(function (e) {
            e.preventDefault();
            $.ajax({
                headers: { "X-CSRFToken": getCookie('csrftoken') },
                type: "POST",
                dataType: "json",
                url: $("#like").attr("href"),
                data: {},
                success: check_liked,
            });
        });
    }
);
$(document).ready(
    check_liked()
);