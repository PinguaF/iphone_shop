$( document ).ready(function(){
    $('.button-choose').on('click', function(){
        if($('.js-ninja-info-category').text() == 'iphone'){
            var line = $('.js-ninja-info-line').text()
            if($(this).attr('parametr') == 'color' ){
                var memory = $('#current-memory').text()
                var color = $(this).text()
            } else {
                var color = $('#current-color').text()
                var memory = $(this).text()
            }
            socket.emit('get_id_by_paramets', {'category': 'iphone', 'line':line, 'color': color, 'memory': memory})
        }
    })
})

socket.on('id_by_paramets', function(msg){
    var category = $('.js-ninja-info-category').text()
    window.location.href = String('http://'+location.host+'/catalog/'+category+'/'+msg)
})