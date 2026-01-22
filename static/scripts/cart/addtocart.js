$('.add-to-cart').click(function(){
    add_to_cart($(this).attr('pid'), $(this).attr('category'))
})
$('.js-counter-plus').click(function(){
    add_to_cart($(this).attr('pid'), $(this).attr('category'))
})
$('.js-counter-minus').click(function(){
    minus_from_cart($(this).attr('pid'), $(this).attr('category'))
})


function add_to_cart(id, category){
    console.log(`adding to cart ${category}: ${id}`)
    socket.emit('add_to_cart', {'category': category, 'id':id})
}
function minus_from_cart(id, category){
    console.log(`minus from cart ${category}: ${id}`)
    socket.emit('minus_from_cart', {'category': category, 'id':id})
}


socket.on('message', function(msg){
    console.log(msg)
})

socket.on('answer_cart', function(msg){
    if(msg['answer'] == '401'){
        window.location.href = String('http://'+location.host+'/login?error=carterror')
    } else if(msg['answer'] == '400') {
        if( window.location.href == String('http://'+location.host+'/cart')){
            location.reload()
        } else {
            console.log('Товар добавлен в корзину')
        }
    }
})