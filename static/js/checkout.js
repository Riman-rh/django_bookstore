    from = document.getElementById('form')
    form.addEventListener('submit', function(e){
        e.preventDefault()
        var id = this.dataset.orderId
        var formData = {
            'firstname':null,
            'lastname':null,
            'email':null,
            'address':null,
            'zipcode':null,
            'phone':null,
            'orderId':id
        }
       formData.firstname = form.firstname.value
       formData.lastname = form.lastname.value
       formData.email = form.email.value
       formData.address = form.address.value
       formData.zipcode = form.zipcode.value
       formData.phone = form.phone.value
       shippinginf(formData)
    })
    function shippinginf(formData){
        url = '/orderprocess/'
        fetch(url,{
              method:'POST',
              headers:{
                'Content-Type':'application/json',
                'X-CSRFToken': csrftoken,
              },
              body: JSON.stringify({formData})
        })
        .then((response)=>{
            window.location.assign("/success")
        })

    }