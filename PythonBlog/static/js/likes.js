function update_like_status() {
    let article_id = $("#article-id").text();
    $.ajax({
        headers: { "X-CSRFToken": getCookie('csrftoken') },
        type: "POST",
        dataType: "json",
        url: "/likes/check/"+article_id,
        data: {},
        success: function (result) {
            if (result["status"] == true) {
                $("#like-link").attr("href", "/likes/unlike/" + article_id);
                $("#like-img").css("-webkit-mask-image", "url(/static/img/like_fill.svg)");
                $("#like-img").css("background-color", "#f44336");
            }
            else {
                $("#like-link").attr("href", "/likes/like/" + article_id);
                // $("#like").html("Лайк " + result["count"]);
                $("#like-img").css("-webkit-mask-image", "url(/static/img/like.svg)");
                $("#like-img").css("background-color", "#b2adcc");
            }
            $("#like-count").html(result["count"])
        },
    });
}

$(document).ready(
    function () {
        $("#like-link").click(function (e) {
            e.preventDefault();
            $.ajax({
                headers: { "X-CSRFToken": getCookie('csrftoken') },
                type: "POST",
                dataType: "json",
                url: $("#like-link").attr("href"),
                data: {},
                success: update_like_status,
            });
        });
    }
);
$(document).ready(
    update_like_status()
);