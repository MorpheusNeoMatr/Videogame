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

    setupDropdownToggle('toggleDirectors', 'directorsList', 'arrowDirectors');
    setupDropdownToggle('toggleCompanies', 'companiesList', 'arrowCompanies');
    setupDropdownToggle('toggleGenres', 'genresList', 'arrowGenres');

    function limitCheckboxSelection(className, limit) {
      const checkboxes = document.querySelectorAll(className);
      checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
          const checkedCheckboxes = document.querySelectorAll(className + ':checked');
          if (checkedCheckboxes.length > limit) {
            this.checked = false;
            alert('You can only select up to ' + limit + ' options.');
          }
        });
      });
    }

    limitCheckboxSelection('.checkbox-director', 3);
    limitCheckboxSelection('.checkbox-company', 3);
    limitCheckboxSelection('.checkbox-genre', 3);

    // Popup functionality
    var popupSeries = document.getElementById("popup-series");
    var openPopupSeriesBtn = document.getElementById("openPopupSeriesBtn");
    var closePopupSeriesBtn = document.getElementById("closePopupSeriesBtn");

    openPopupSeriesBtn.onclick = function() {
        popupSeries.style.display = "block";
    };

    closePopupSeriesBtn.onclick = function() {
        popupSeries.style.display = "none";
    };

    // Popup functionality for Genre
    var popupGenre = document.getElementById("popup-genre");
    var openPopupGenreBtn = document.getElementById("openPopupGenreBtn");
    var closePopupGenreBtn = document.getElementById("closePopupGenreBtn");

    openPopupGenreBtn.onclick = function() {
        popupGenre.style.display = "block";
    };

    closePopupGenreBtn.onclick = function() {
        popupGenre.style.display = "none";
    };

    window.onclick = function(event) {
      if (event.target == popupSeries) {
          popupSeries.style.display = "none";
      }
      if (event.target == popupGenre) {
          popupGenre.style.display = "none";
      }
    };
  });