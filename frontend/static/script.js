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



let currentPage = 1;
let isLoading = false;
let hasNext = true;

window.onload = function () {
    if (window.location.pathname === '/home/') {
        const messageList = document.getElementById('message-list');
        fetchMessages(currentPage);

        // وقتی اسکرول به بالا می‌رسه
        messageList.addEventListener('scroll', function () {
            if (messageList.scrollTop === 0 && !isLoading && hasNext) {
                fetchMessages(currentPage);
            }
        });
    }
};

function fetchMessages(page) {
    isLoading = true;

    fetch(`/sparrow/apiv1/rooms/1/messages/?page=${page}`, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
    })
        .then(response => response.json())
        .then(data => {
            const messageList = document.getElementById('message-list');
            const prevScrollHeight = messageList.scrollHeight;

            data.results.reverse().forEach(message => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <div class="sender">${message.sender.title}</div>
                    <div class="message">${message.body}</div>
                    <div class="created_at">${new Date(message.created_at).toLocaleString()}</div>
                `;
                messageList.prepend(li);
            });

            // اگه صفحه اول هست اسکرول کن پایین
            if (page === 1) {
                setTimeout(() => {
                    messageList.scrollTop = messageList.scrollHeight;
                }, 100);
            } else {
                // نگه داشتن موقعیت اسکرول
                messageList.scrollTop = messageList.scrollHeight - prevScrollHeight;
            }

            currentPage++;
            if (!data.next) {
                hasNext = false;
            }

            isLoading = false;
        })
        .catch(error => {
            console.error('Error fetching messages:', error);
            isLoading = false;
        });
}


function sendMessage() {
    event.preventDefault();  // Prevent form submission

    const messageContent = document.getElementById('message-input').value;

    if (messageContent.trim() === '') {
        alert("Message can't be empty!");
        return;
    }

    const messageData = {
        body: messageContent
    };

    fetch('/sparrow/apiv1/rooms/1/messages/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
        body: JSON.stringify(messageData)
    })
    .then(response => response.json())
    .then(data => {
        if (data) {
            document.getElementById('message-input').value = '';
            fetchMessages();
        } else {
            alert("Failed to send message!");
        }
    })
    .catch(error => {
        console.error('Error sending message:', error);
    });
}
