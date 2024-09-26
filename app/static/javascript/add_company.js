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

    // Setup dropdown toggles for different sections
    setupDropdownToggle('toggleCompanyGames', 'companygamesList', 'arrowCompanyGames');
    setupDropdownToggle('toggleCompanyDirectors', 'companydirectorsList', 'arrowCompanyDirectors');
    setupDropdownToggle('toggleCompanyFounders', 'companyfoundersList', 'arrowCompanyFounders');
    setupDropdownToggle('toggleCompanySeries', 'companyseriesList', 'arrowCompanySeries');

    // Popup functionality for series in company
    var popupCompanySeries = document.getElementById("popup-company-series");
    var openPopupCompanySeriesBtn = document.getElementById("openPopupCompanySeriesBtn");
    var closePopupCompanySeriesBtn = document.getElementById("closePopupCompanySeriesBtn");

    // Function to open the popup
    openPopupCompanySeriesBtn.onclick = function() {
        popupCompanySeries.style.display = "block";
    };

    // Function to close the popup
    closePopupCompanySeriesBtn.onclick = function() {
        popupCompanySeries.style.display = "none";
    };

    // Click event to close the popup if the user clicks outside of it
    window.onclick = function(event) {
        if (event.target == popupCompanySeries) {
            popupCompanySeries.style.display = "none";
        }
    };


    const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5 MB limit for file uploads

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
    checkFileSize('company_picture_size_limit_1');
    checkFileSize('company_picture_size_limit_2');

  });