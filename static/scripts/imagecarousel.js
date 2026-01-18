$( document ).ready(function(){
    const animation_time = 200;
    $('.main-image-section').children().first().addClass('js-active-image')
    $('.js-active-image').fadeIn(animation_time)
    function imagecarousel(){
        var active_img = $('.js-active-image')
        active_img.fadeOut(animation_time)
        $('img').removeClass('js-active-image')
        if(active_img.is(':last-child')){
            $('.main-image-section').children().first().addClass('js-active-image')
        } else {
            active_img.next().addClass('js-active-image')
        }
        setTimeout(`$('.js-active-image').fadeIn(${animation_time})`, animation_time)
    }
    setInterval(imagecarousel, 3000)
})