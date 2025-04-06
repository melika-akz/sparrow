// Fetch members for the direct chat list
const fetchMembers = async () => {
    try {
        const response = await fetch('/sparrow/apiv1/directs/', {
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            },
        });

        const data = await response.json();
        const memberList = document.getElementById('member-list');

        // Clear existing members
        memberList.innerHTML = '';

        // Populate member list
        data.results.forEach(member => {
            const li = document.createElement('li');
            li.textContent = member.name;  // Assuming member has a 'name' field
            li.setAttribute('data-direct-id', member.direct_id);  // Store the direct_id as a data attribute

            // Add the click event listener to call loadMessages with direct_id
            li.addEventListener('click', function() {
                loadMessages(member.direct_id);  // Call loadMessages with the correct direct_id
            });

            memberList.appendChild(li);
        });
    } catch (error) {
        console.error('Error fetching members:', error);
    }
};

// Ensure the member list is fetched on page load
document.addEventListener('DOMContentLoaded', fetchMembers);