// fetches the registered users from database
document.addEventListener('DOMContentLoaded', function() {
            fetch('http://localhost:5000/user/users')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok ' + response.statusText);
                    }
                    return response.json();
                })
                .then(users => {
                    const userList = document.getElementById('userList');
                    users.forEach(user => {
                        const listItem = document.createElement('li');
                        listItem.textContent = `Username: ${user.username}, Email: ${user.email}, Phone: ${user.phone}`;
                        userList.appendChild(listItem);
                    });
                })
                .catch(error => console.error('There was a problem with the fetch operation:', error));
        });