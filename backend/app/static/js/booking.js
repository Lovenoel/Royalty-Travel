document.getElementById('booking-form').addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(event.target);
            const data = Object.fromEntries(formData.entries());

            fetch('/booking/api/bookings', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                loadBookings();
            });
        });

        function loadBookings() {
            fetch('/booking/book')
                .then(response => response.json())
                .then(data => {
                    const bookingsList = document.getElementById('bookings-list');
                    bookingsList.innerHTML = '';
                    data.forEach(booking => {
                        const li = document.createElement('li');
                        li.textContent = `Booking ID: ${booking.id}, Passenger ID: ${booking.passenger_id}, Departure: ${booking.departure_place}, Destination: ${booking.destination}, Date & Time: ${booking.date_time}, Fare: ${booking.fare}`;
                        bookingsList.appendChild(li);
                    });
                });
        }

        document.addEventListener('DOMContentLoaded', loadBookings);