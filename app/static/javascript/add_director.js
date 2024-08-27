document.addEventListener('DOMContentLoaded', function() {
    function setupDropdownToggle(buttonId, listId, arrowId) {
      const button = document.getElementById(buttonId);
      const list = document.getElementById(listId); 
      const arrow = document.getElementById(arrowId);

      button.addEventListener('click', function() {
        const isVisible = list.style.display === 'block';
        list.style.display = isVisible ? 'none' : 'block';
        arrow.classList.toggle('up', !isVisible);
        arrow.classList.toggle('down', isVisible);
      });
    }


    setupDropdownToggle('toggleDirectorGames', 'directorgamesList', 'arrowDirectorGames');
    setupDropdownToggle('toggleDirectorCompanies', 'directorcompaniesList', 'arrowDirectorCompanies');



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
    checkFileSize('director_picture_size_limit_1');
    checkFileSize('director_picture_size_limit_2');
  });