document.addEventListener('DOMContentLoaded', function() {
    // Function to set up dropdown toggle for buttons
    function setupDropdownToggle(buttonId, listId, arrowId) {
      const button = document.getElementById(buttonId);
      const list = document.getElementById(listId); 
      const arrow = document.getElementById(arrowId);

      // Add click event listener to the button
      button.addEventListener('click', function() {
        const isVisible = list.style.display === 'block';
        list.style.display = isVisible ? 'none' : 'block';
        arrow.classList.toggle('up', !isVisible);
        arrow.classList.toggle('down', isVisible);
      });
    }

    // Setup dropdown toggle for the founder companies section
    setupDropdownToggle('toggleFounderCompanies', 'foundercompaniesList', 'arrowFounderCompanies');


    const MAX_FILE_SIZE = 5 * 1024 * 1024; // Set maximum file size limit to 5 MB

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
    checkFileSize('founder_picture_size_limit_1');
    checkFileSize('founder_picture_size_limit_2');
  });