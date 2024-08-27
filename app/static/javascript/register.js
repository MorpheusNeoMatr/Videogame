document.addEventListener('DOMContentLoaded', () => {
    const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB

    // Function to check file size
    function checkFileSize(inputId) {
        const pictureInput = document.getElementById(inputId);
        pictureInput.addEventListener('change', () => {
            const pictureFile = pictureInput.files[0];

            if (pictureFile && pictureFile.size > MAX_FILE_SIZE) {
                alert('File size exceeds 5 MB limit.');
                pictureInput.value = ''; // Clear the input to allow re-selection
            }
        });
    }

    // Check file sizes for each input
    checkFileSize('register_picture_size_limit');
});
