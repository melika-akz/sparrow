// Login function
function login(event) {
    event.preventDefault();  // Prevent the default form submission

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const loginData = {
        email: email,
        password: password
    };

    fetch('/apiv1/tokens/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(loginData),
    })
    .then(response => response.json())
    .then(data => {
        if (data.access) {
            localStorage.setItem('token', data.access);  // Store the token
            window.location.href = '/home/';  // Redirect to the home page after successful login
        } else {
            alert('Login failed! Please check your credentials.');
        }
    })
    .catch(error => {
        console.error('Error logging in:', error);
    });
}


// Signup function
function signup() {
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const signupData = {
        username: username,
        email: email,
        password: password
    };

    fetch('/api/signup/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(signupData),
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            localStorage.setItem('jwt_token', data.token);  // Store the token
            window.location.href = '';  // Redirect to home page after successful signup
        } else {
            alert('Sign up failed! Please check your input.');
        }
    })
    .catch(error => {
        console.error('Error signing up:', error);
    });
}

