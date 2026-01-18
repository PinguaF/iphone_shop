const socket = io();

$( document ).ready(function(){
    $('.logo').click(function(){
        window.location.href = "/";
    })
    $('.js-button-to-page').click(function(){
        window.location.href = String('http://'+location.host+$(this).attr('jslink'))
    })
    $('img').on('error', function() {
        console.log('Ошибка при загрузке изображения:', $(this).attr('src'));
        $(this).attr('src', '/static/images/icons/image-placeholder.svg');
    })
    
    $('.side-menu').hide()
    $('#burger-menu').click(function(){
        document.body.style.overflow = 'hidden';
        $('.side-menu').fadeIn(500)
    })
    $('.js-close-sm').click(function(){
        document.body.style.overflow = 'scroll';
        $('.side-menu').fadeOut(500)
    })
})