document.getElementById("public_product").onsubmit = function(e){
    e.preventDefault();
    fetch('/publish/product', {
        method : 'POST',
        body : JSON.stringify({
            'name' : document.getElementById('name').value,
            'price' : document.getElementById('price').value,
            'features' : document.getElementById('features').value,
            'DNI' : document.getElementById('DNI').value,
            'TI' : document.getElementById('TI').value,
            'TF' : document.getElementById('TF').value
        }),
        headers : {
            'Content-type' : 'application/json'
        }
    }).then(function(response){
        return response.json()
    }).then(function(jsonResponse){
        console.log(jsonResponse)
        if(jsonResponse['error'] === false){
            var dni = jsonResponse['dni'].toString()
            window.location.replace('/homepage/'+dni)
            document.getElementById("error").className='hidden'
        }else{
            document.getElementById("error").className=''
            document.getElementById("error").innerHTML = jsonResponse['error_message']
        }
    }).catch(function(error){
        console.log(error)
        document.getElementById("error").className = ''
    })
}

    const items = document.querySelectorAll('.delete-button')
        for (let i = 0; i < items.length; i++) {
            const item = items[i]
            item.onclick = function(e) {
                console.log('click event: ', e)
                const product_id = e.target.dataset['id'];
                fetch('/product/'+product_id+'/delete-product', {
                    method: 'DELETE'
                }).then(function() {
                    const item = e.target.parentElement
                    item.remove()
                });
            }
        }