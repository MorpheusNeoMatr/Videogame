// Wait for the DOM to be fully loaded before executing the script
document.addEventListener('DOMContentLoaded', function() {
    // Function to set up dropdown toggle functionality
    function setupDropdownToggle(buttonId, listId, arrowId) {
      const button = document.getElementById(buttonId);
      const list = document.getElementById(listId); 
      const arrow = document.getElementById(arrowId);

      // Add a click event listener to the button
      button.addEventListener('click', function() {
        const isVisible = list.style.display === 'block';
        list.style.display = isVisible ? 'none' : 'block';
        arrow.classList.toggle('up', !isVisible);
        arrow.classList.toggle('down', isVisible);
      });
    }

    // Set up dropdown toggles for various sections
    setupDropdownToggle('toggleGamesDirectors', 'gamesdirectorsList', 'arrowGamesDirectors');
    setupDropdownToggle('toggleGamesCompanies', 'gamescompaniesList', 'arrowGamesCompanies');
    setupDropdownToggle('toggleGamesGenres', 'gamesgenresList', 'arrowGamesGenres');



    // Popup functionality for series
    var popupGamesSeries = document.getElementById("popup-games-series");
    var openPopupGamesSeriesBtn = document.getElementById("openPopupGamesSeriesBtn");
    var closePopupGamesSeriesBtn = document.getElementById("closePopupGamesSeriesBtn");

    openPopupGamesSeriesBtn.onclick = function() {
        popupGamesSeries.style.display = "block";
    };

    closePopupGamesSeriesBtn.onclick = function() {
        popupGamesSeries.style.display = "none";
    };


    // Popup functionality for Genre
    var popupGamesGenre = document.getElementById("popup-games-genre");
    var openPopupGamesGenreBtn = document.getElementById("openPopupGamesGenreBtn");
    var closePopupGamesGenreBtn = document.getElementById("closePopupGamesGenreBtn");

    openPopupGamesGenreBtn.onclick = function() {
        popupGamesGenre.style.display = "block";
    };

    closePopupGamesGenreBtn.onclick = function() {
        popupGamesGenre.style.display = "none";
    };

    window.onclick = function(event) {
      if (event.target == popupGamesSeries) {
          popupGamesSeries.style.display = "none";
      }
      if (event.target == popupGamesGenre) {
          popupGamesGenre.style.display = "none";
      }
    };


    const MAX_FILE_SIZE = 5 * 1024 * 1024; // Set maximum file size to 5 MB

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
    checkFileSize('game_picture_size_limit_1');
    checkFileSize('game_picture_size_limit_2');
    checkFileSize('game_picture_size_limit_3');
    checkFileSize('game_picture_size_limit_4');
    checkFileSize('game_picture_size_limit_5');
    checkFileSize('game_picture_size_limit_6');
  });