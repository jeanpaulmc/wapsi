document.getElementById("register").onsubmit = function (e) {
    e.preventDefault();
    fetch('/users/create', {
        method: 'POST',
        body: JSON.stringify({
            'fecha_nacimiento': document.getElementById('fecha_nacimiento').value,
            'nombre': document.getElementById('nombre').value,
            'apellido': document.getElementById('apellido').value,
            'edad': document.getElementById('edad').value,
            'correo': document.getElementById('correo').value,
            'contrasenia': document.getElementById('contrasenia').value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function (response) {
        return response.json()
    }).then(function (jsonResponse) {
        console.log(jsonResponse)
        if (jsonResponse['error'] === false) {
            window.location.replace('/templates/homepage')
            document.getElementById("error").className = 'hidden'
        } else {
            document.getElementById("error").className = ''
            document.getElementById("error").innerHTML = jsonResponse['error_message']
        }
    }).catch(function (error) {
        console.log(error)
        document.getElementById("error").className = ''
    });
};