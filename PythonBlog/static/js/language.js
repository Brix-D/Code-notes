// Функция которая проставляет атрибут selected текущему выбранному пользователем языку
$(document).ready(
    function() {
        let language_list = document.getElementById('select_lang').children;
        // Превращение коллекции DOM-детей в массив
        // https://learn.javascript.ru/traversing-dom
        language_list = Array.prototype.slice.call(language_list);
        language_list.forEach(function(value) {
            if (value.getAttribute("value") == getCookie("lang")) {
                // Сравнивает значение варианта языка и куку текущего языка,
                // если равны то ставит варианту атрибут selected
                value.setAttribute('selected', '');
            }
        });
    }
);