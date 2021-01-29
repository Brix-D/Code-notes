// Функция которая проставляет атрибут selected текущему выбранному пользователем языку
$(document).ready(
    function() {
        let language_list = document.getElementById('select_lang').children;
        // Превращение коллекции DOM-детей в массив
        // https://learn.javascript.ru/traversing-dom
        language_list = Array.prototype.slice.call(language_list);
        language_list.forEach(function(value) {
            console.log(value);
            if (value.getAttribute("value") == getCookie("lang")) {
                console.log("язык - " + value.getAttribute("value"));
                value.setAttribute('selected', '');
            }
        });
    }
);