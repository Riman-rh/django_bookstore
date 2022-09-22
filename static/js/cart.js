var updateBtns = document.getElementsByClassName('update_cart')
for( var i=0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var bookId = this.dataset.book
        var action = this.dataset.action
        console.log('bookId: ', bookId, 'action: ', action)
        if(user === 'AnonymousUser'){
            createCookieItem(bookId,action)
        }else{
            updateUserOrder(bookId, action)
        }
    })
}

function createCookieItem(bookId,action){
     if (action == "add"){
        if (cart[bookId] == undefined ){
                cart[bookId] = {'quantity':1}
            }else{
                cart[bookId]['quantity'] += 1
            }
        }
    else if(action == "remove"){
        cart[bookId]['quantity'] -=1
        if(cart[bookId]['quantity']<=0 ) {
            delete cart[bookId]
        }
    }
    document.cookie = 'cart='+ JSON.stringify(cart) + ';domain=;path=/'
    location.reload()
}

function updateUserOrder(bookId, action){
    var url ='/updatecart/'
    fetch(url,{
          method:'POST',
          headers:{
          'Content-Type':'application/json',
          'X-CSRFToken':csrftoken,
          },

          body: JSON.stringify({'bookId':bookId, 'action':action})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
       location.reload()
    })
}