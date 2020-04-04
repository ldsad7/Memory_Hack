$(document).ready(function(){
    $('button.prev_btn').click(function(){
        $('.prev_wrapper').fadeOut(600, function () {
            document.location.reload();//Здесь надо будет написать ссылку на внутренню страницу
        });
    });
});