document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('submit_form');
    const submitButton = document.getElementById('submitButton');

    form.addEventListener('submit', (event) => {
        // Disable the submit button to prevent multiple submissions
        submitButton.disabled = true;
        submitButton.textContent = 'Submitting...'; // Optional: Change button text
    });
});