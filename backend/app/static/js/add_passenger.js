function getCsrfToken() {
    return document.querySelector('input[name="csrf_token"]').value;
}

function addPassenger() {
    const form = document.getElementById('passengerForm');
    const data = {
        username: form.username.value,
        email: form.email.value,
        phone: form.phone.value
    };

    console.log('Sending data:', data); // Log data to verify structure

    fetch('http://localhost:5000/passenger/passengers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken() // Include the CSRF token in the headers
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                throw new Error(text || 'Unknown error');
            });
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        alert('Passenger added successfully!');
        closeAddPassengerForm(); // Close the modal after adding passenger
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Failed to add passenger: ' + error.message);
    });
}

function alertCheck() {
    alert('Alert button clicked!');
}
