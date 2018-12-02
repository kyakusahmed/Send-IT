
var signup_form = document.getElementById('signup_form')

signin_form.addEventListener('submit', function(event){
    //prevent pager load
    event.preventDefault()

    var first_name = document.getElementById('first_name').value
    var last_name = document.getElementById('last_name').value
    var email = document.getElementById('email').value
    var password = document.getElementById('password').value

    fetch('/api/v1/user/register', {
        method:'POST',
        headers: {'Content-Type' : 'application/json'},
        body:JSON.stringify({
            first_name: first_name,
            last_name: last_name,
            email:email,
            password:password
        })
    })
    .then(function(response){
        return response.json()
    })
    .then(function(response){
        console.log(response)
        if (response.access_token) {
            alert("Login successful " + response.access_token )
        } else if (response.msg) {
            alert(response.msg)
        }
    })
    .catch(function(error){
        console.log(error)
    })

    
})