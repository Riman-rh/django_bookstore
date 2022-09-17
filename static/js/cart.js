var updateBtns = document.getElementsByClassName('update_cart')
for( var i=0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var bookId = this.dataset.book
        var action = this.dataset.action
        console.log('bookId: ', bookId, 'action: ', action)
        if(user === 'AnonymousUser'){
            console.log('you are not logged in')
        }else{
            updateUserOrder(bookId, action)
        }
    })
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
        console.log('data', data)
    })
}