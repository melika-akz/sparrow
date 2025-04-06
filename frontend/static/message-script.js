let page = 1;
let take = 10;
let isLoading = false;
let hasMoreMessages = true;

window.onload = function () {
    if (window.location.pathname === '/home/') {
        const messageList = document.getElementById('message-list');
        fetchMessages(page);  // Load latest messages

        messageList.addEventListener('scroll', function () {
            if (messageList.scrollTop === 0 && !isLoading && hasMoreMessages) {
                page += 1;  // Load next (older) page
                fetchMessages(page);
            }
        });
    }
};

function fetchMessages(page) {
    isLoading = true;
    const messageList = document.getElementById('message-list');

    // Save current scroll height before new content loads
    const oldScrollHeight = messageList.scrollHeight;

    fetch(`/sparrow/apiv1/rooms/1/messages/?page=${page}&take=${take}`, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('token')
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.results.length === 0) {
                hasMoreMessages = false;
            }

            // Reverse if needed (API returns newest-to-oldest)
            const messages = data.results.reverse();

            messages.forEach(message => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <div class="sender">${message.sender.title}</div>
                    <div class="message">${message.body}</div>
                    <div class="created_at">${new Date(message.created_at).toLocaleString()}</div>
                `;
                messageList.prepend(li);
            });

            // Restore scroll position (prevent jump)
            const newScrollHeight = messageList.scrollHeight;
            messageList.scrollTop = newScrollHeight - oldScrollHeight;

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

            // Add the new message to the bottom
            const messageList = document.getElementById('message-list');
            const li = document.createElement('li');
            li.innerHTML = `
                <div class="sender">${data.sender.title}</div>
                <div class="message">${data.body}</div>
                <div class="created_at">${new Date(data.created_at).toLocaleString()}</div>
            `;
            messageList.appendChild(li);  // Insert at the bottom of the list

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