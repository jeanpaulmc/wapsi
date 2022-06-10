document.getElementById("recharge").onsubmit = function(e){
    e.preventDefault();
    fetch('/recharge/wallet', {
        method : 'PUT',
        body: JSON.stringify({
            'DNI': document.getElementById('DNI').value,
            'price': document.getElementById('price').value
        }),
        headers : {
            'Content-Type' : 'application/json'
        },
    }).then(function(response){
        return response.json()
    }).then(function(jsonResponse){
        console.log(jsonResponse)
        if(jsonResponse['error'] === false){
            document.getElementById("error").className='hidden'
            location.reload(true)
        }else{
            document.getElementById("error").className=''
            document.getElementById("error").innerHTML = jsonResponse['error_message']
        }
    }).catch(function(error) {
        console.log(error)
        document.getElementById("error").className=''
    });
}