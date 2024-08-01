// Declare state variables
let directorListVisible = true;


function updateGameList(games) {
    var gameList = document.getElementById("gameList");
    gameList.innerHTML = ""; // Clear previous list

    if (games.length === 0) {
        var noGameMessage = document.createElement("p");
        noGameMessage.textContent = "No games match the specified filters.";
        noGameMessage.className = "no-game-message"; // Add a class for styling if needed
        gameList.appendChild(noGameMessage);
        return;
    }

    games.forEach(game => {
        // Create a link element
        var link = document.createElement("a");
        link.href = `/game/${game.id}`; // URL to the game detail page
        link.className = "game-item-link"; // Add a class for styling

        // Create a container div for each game
        var div = document.createElement("div");
        div.className = "game-item"; // Add a class for styling

        // Create an image element
        var img = document.createElement("img");
        img.src = `/static/games_images/${game.picture_4}`; // Adjust to your image path
        img.className = "game-image"; // Add a class for styling

        // Create a paragraph element for the game name
        var p = document.createElement("p");
        p.textContent = game.name;
        p.className = "game-name"; // Add a class for styling

        // Append the image and name to the container div
        div.appendChild(img);
        div.appendChild(p);

        // Append the container div to the link
        link.appendChild(div);

        // Append the link to the game list
        gameList.appendChild(link);
    });
}


function fetchAllGames() {
    fetch(`/api/games`)  // No query parameters to fetch all games initially
        .then(response => response.json())
        .then(data => {
            updateGameList(data.games);  // Update the game list in the UI with names only
        })
        .catch(error => console.error('Error fetching games:', error));
}

function filterGames() {
    var genreId = document.getElementById("genreDropdown").value;
    var companyId = document.getElementById("companyDropdown").value;
    var directorId = document.getElementById("directorDropdown").value;
    var seriesId = document.getElementById("seriesDropdown").value;

    // Perform AJAX request to fetch filtered games based on selected filters
    fetch(`/api/games?Genre=${genreId}&Company=${companyId}&Director=${directorId}&Series=${seriesId}`)
        .then(response => response.json())
        .then(data => {
            updateGameList(data.games);  // Update the game list in the UI with names only
        })
        .catch(error => console.error('Error fetching games:', error));
}

// Fetch all games initially when the page loads
window.addEventListener('load', fetchAllGames);

// Event listener for Apply Filters button
document.getElementById('filterButton').addEventListener('click', filterGames);

// //add_stuff_to_games
// document.addEventListener('DOMContentLoaded', function() {
//     var selects = document.querySelectorAll('select.form-control');

//     selects.forEach(function(select) {
//         select.addEventListener('change', function() {
//             if (select.value !== "") {
//                 select.classList.remove('placeholder');
//             } else {
//                 select.classList.add('placeholder');
//             }
//         });
//     });
// });




// // Function to toggle the visibility of the director list
// function toggleDirectors() {
//     const directorList = document.getElementById("director-list");
//     const showDirectorsButton = document.getElementById("showDirectorsButton");

//     if (directorListVisible) {
//         directorList.style.display = "none";
//         showDirectorsButton.textContent = "Show Directors";
//         directorListVisible = false;
//     } else {
//         directorList.style.display = "block";
//         showDirectorsButton.textContent = "Hide Directors";
//         directorListVisible = true;
//     }
// }

// // Function to update the selected director(s)
// function updateSelectedDirectors() {
//     const selectedDirectorsContainer = document.getElementById("selectedDirectors");
//     const selectedOptions = document.querySelectorAll('input[name="game_directors"]:checked');
    
//     if (selectedOptions.length === 0) {
//         selectedDirectorsContainer.textContent = "No director selected.";
//     } else {
//         const selectedNames = Array.from(selectedOptions).map(option => {
//             return option.nextSibling.textContent.trim();
//         }).join(', ');

//         selectedDirectorsContainer.textContent = `Selected Director(s): ${selectedNames}`;
//         document.getElementById("showDirectorsButton").textContent = selectedNames || "Show Directors";
//     }
// }

// // Attach event listeners to the checkboxes and buttons
// document.addEventListener('DOMContentLoaded', function() {
//     const showDirectorsButton = document.getElementById('showDirectorsButton');

//     if (showDirectorsButton) {
//         showDirectorsButton.addEventListener('click', toggleDirectors);
//     } else {
//         console.error('Button with ID "showDirectorsButton" not found.');
//     }

//     // Update selected directors on checkbox change
//     document.querySelectorAll('input[name="game_directors"]').forEach(checkbox => {
//         checkbox.addEventListener('change', updateSelectedDirectors);
//     });
// });

