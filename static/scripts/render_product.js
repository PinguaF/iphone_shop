console.log($('.js-ninja-info').text())
//render product
$( document ).ready(function(){

    var plist = JSON.parse(String($('.js-ninja-info').text()).replaceAll(`'`,'"')) || {}
    console.log(plist)
    var category_list = []

    function render_grid(category = null){
        if (!category) {
            for(var product in plist){
                if (!category_list.includes(plist[product][2])){
                    category_list.push(plist[product][2])
                }
                $('.category-count').text(plist.length)
                $('.catalog-grid').append(
                    `<div class="product" pid="${plist[product][0]}">
                    <img src="/static/images/products/${plist[product][6]}.png">
                    <div class="price">
                        <p>${plist[product][5]} BYN</p>
                    </div>
                    <div class="availability">
                    <svg class="icon-in-availability" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M15.142 9.98299L10.875 14.25L9.42049 12.7955M12 3C7.02944 3 3 7.02944 3 12C3 16.9706 7.02944 21 12 21C16.9706 21 21 16.9706 21 12C21 7.02944 16.9706 3 12 3Z" stroke="#48dc6c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <p>В наличии</p>
                    </div>
                    <div class="name">
                    <p>${plist[product][2]}, ${plist[product][4]}, ${plist[product][3]}</p>
                    </div>
                    <button class="add-to-cart">В корзину</button>
                    </div>`)}
        } else {
            var counter = 0
            $('.catalog-grid').empty()
            for(var product in plist){
            if(plist[product][2]==category){
                counter ++;
                $('.catalog-grid').append(
                    `<div class="product" pid="${plist[product][0]}">
                    <img src="/static/images/products/${plist[product][6]}.png">
                    <div class="price">
                    <p>${plist[product][5]} BYN</p>
                    </div>
                    <div class="availability">
                    <svg class="icon-in-availability" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M15.142 9.98299L10.875 14.25L9.42049 12.7955M12 3C7.02944 3 3 7.02944 3 12C3 16.9706 7.02944 21 12 21C16.9706 21 21 16.9706 21 12C21 7.02944 16.9706 3 12 3Z" stroke="#48dc6c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <p>В наличии</p>
                    </div>
                    <div class="name">
                    <p>${plist[product][2]}, ${plist[product][4]}, ${plist[product][3]}</p>
                    </div>
                    <button class="add-to-cart">В корзину</button>
                    </div>`)
                $('.category-count').text(counter)
            }
        }}

        $('img').on('error', function() {
            console.log('Ошибка при загрузке изображения:', $(this).attr('src'));
            $(this).attr('src', '/static/images/icons/image-placeholder.svg');
        })

        $('.product').on('click', function(){
            window.location.href = String(location.href+'/'+$(this).attr('pid'))
        })
    }
    render_grid()
    for (var cat in category_list){
        $('.category-choose').append(`<p class='js-category'>${category_list[cat]}</p>`)
    }


    $('.js-category').on('click', function() {
        $('p').removeClass('active-category')
        $(this).addClass('active-category');
        render_grid($(this).text())
    })
    $('.js-all-category').on('click', function() {
        $('p').removeClass('active-category')
        $(this).addClass('active-category');
        render_grid()
    })
})
