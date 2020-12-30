// функция галочки при загрузке файла
// https://obninsksite.ru/blog/html-and-css/input-file-style


(function() {

  'use strict';

  $('#upload-file').each(function() {
    var $input = $(this),
        $label = $input.next('.label-file'),
        labelVal = $label.html();

   $input.on('change', function(element) {
      var fileName = '';
      if (element.target.value) fileName = element.target.value.split('\\').pop();
      fileName ? $label.addClass('has-file').find('.js-fileName').html(fileName) : $label.removeClass('has-file').html(labelVal);
   });
  });

})();