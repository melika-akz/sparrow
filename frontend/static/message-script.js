let currentPage = 1;
let isLoading = false;
let hasNext = true;

window.onload = function () {
    if (window.location.pathname === '/home/') {
        const messageList = document.getElementById('message-list');
        fetchMessages(currentPage);
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

            // Ensure messages are in the correct order (oldest at top, newest at bottom)
            data.results.reverse().forEach(message => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <div class="sender">${message.sender.title}</div>
                    <div class="message">${message.body}</div>
                    <div class="created_at">${new Date(message.created_at).toLocaleString()}</div>
                `;
                messageList.appendChild(li);  // Add messages at the bottom
            });

            // Keep the scroll at the bottom after adding new messages
            messageList.scrollTop = messageList.scrollHeight;

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

            // Add the new message to the bottom of the list
            const messageList = document.getElementById('message-list');
            const li = document.createElement('li');
            li.innerHTML = `
                <div class="sender">${data.sender.title}</div>
                <div class="message">${data.body}</div>
                <div class="created_at">${new Date(data.created_at).toLocaleString()}</div>
            `;
            messageList.appendChild(li);  // Add the sent message at the bottom

            // Ensure the scroll is at the bottom after sending the message
            messageList.scrollTop = messageList.scrollHeight;
        } else {
            alert("Failed to send message!");
        }
    })
    .catch(error => {
        console.error('Error sending message:', error);
    });
}