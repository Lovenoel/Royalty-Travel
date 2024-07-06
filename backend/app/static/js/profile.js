// Add an event listener to the file input element for profile picture changes
document.getElementById('profile-picture-input').addEventListener('change', function(event) {
    const file = event.target.files[0]; // Get the selected file

    // Check if a file was selected
    if (file) {
        const formData = new FormData(); // Create a new FormData object
        formData.append('profile_picture', file); // Append the selected file to the FormData object

        // Send the form data to the server using the fetch API
        fetch('/profile/upload_picture', {
            method: 'POST', // HTTP method
            body: formData // Form data to be sent in the request body
        })
        .then(response => response.json()) // Parse the JSON response
        .then(data => {
            // Check if the upload was successful
            if (data.success) {
                // Update the profile picture image source to the newly uploaded file
                document.getElementById('profile-picture').src = URL.createObjectURL(file);
            } else {
                // Alert the user if the upload failed
                alert('Failed to upload profile picture.');
            }
        })
        .catch(error => {
            // Handle any errors that occurred during the upload process
            console.error('Error:', error);
            alert('An error occurred while uploading the profile picture.');
        });
    }
});
