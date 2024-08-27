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


    setupDropdownToggle('toggleCompanyGames', 'companygamesList', 'arrowCompanyGames');
    setupDropdownToggle('toggleCompanyDirectors', 'companydirectorsList', 'arrowCompanyDirectors');
    setupDropdownToggle('toggleCompanyFounders', 'companyfoundersList', 'arrowCompanyFounders');
    setupDropdownToggle('toggleCompanySeries', 'companyseriesList', 'arrowCompanySeries');

    // Popup functionality for series in company
    var popupCompanySeries = document.getElementById("popup-company-series");
    var openPopupCompanySeriesBtn = document.getElementById("openPopupCompanySeriesBtn");
    var closePopupCompanySeriesBtn = document.getElementById("closePopupCompanySeriesBtn");

    openPopupCompanySeriesBtn.onclick = function() {
        popupCompanySeries.style.display = "block";
    };

    closePopupCompanySeriesBtn.onclick = function() {
        popupCompanySeries.style.display = "none";
    };

    window.onclick = function(event) {
        if (event.target == popupCompanySeries) {
            popupCompanySeries.style.display = "none";
        }
    };


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
    checkFileSize('company_picture_size_limit_1');
    checkFileSize('company_picture_size_limit_2');

  });