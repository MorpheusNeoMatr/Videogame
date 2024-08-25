document.addEventListener('DOMContentLoaded', () => {
    const pictureInput = document.getElementById('user_picture');
    const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB

    pictureInput.addEventListener('change', () => {
        const pictureFile = pictureInput.files[0];

        if (pictureFile && pictureFile.size > MAX_FILE_SIZE) {
            alert('File size exceeds 5 MB limit.');
            pictureInput.value = ''; // Clear the input to allow re-selection
        }
    });
});