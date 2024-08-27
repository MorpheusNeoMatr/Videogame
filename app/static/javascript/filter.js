// Update the game list (existing function)
function updateGameList(games) {
    var gameList = document.getElementById("gameList");
    gameList.innerHTML = ""; // Clear previous list

    if (games.length === 0) {
        var noGameMessage = document.createElement("p");
        noGameMessage.textContent = "No games match the specified filters.";
        noGameMessage.className = "no-filter-message"; // Add a class for styling if needed
        gameList.appendChild(noGameMessage);
        return;
    }

    games.forEach(game => {
        var link = document.createElement("a");
        link.href = `/game/${game.id}`;
        link.className = "item-link";

        var div = document.createElement("div");
        div.className = "item";

        var img = document.createElement("img");
        img.src = game.picture_1 ? `/static/games_images/${game.picture_1}` : '/static/games_images/default_image.jpg';
        img.className = "image";


        var p = document.createElement("p");
        p.textContent = game.name;
        p.className = "name";

        div.appendChild(img);
        div.appendChild(p);
        link.appendChild(div);
        gameList.appendChild(link);
    });
}


// Filter functions
function filterGames() {
    var genreId = document.getElementById("genreDropdown").value;
    var companyId = document.getElementById("companyDropdown").value;
    var directorId = document.getElementById("directorDropdown").value;
    var seriesId = document.getElementById("seriesDropdown").value;
    var usersId = document.getElementById("usersDropdown").value;

    fetch(`/api/games?Genre=${genreId}&Company=${companyId}&Director=${directorId}&Series=${seriesId}&User=${usersId}`)
        .then(response => response.json())
        .then(data => updateGameList(data.games))
        .catch(error => console.error('Error fetching games:', error));
}


// Update the user list (existing function)
function updateUserList(users) {
    var userList = document.getElementById("userList");
    userList.innerHTML = ""; // Clear previous list

    if (users.length === 0) {
        var noUserMessage = document.createElement("p");
        noUserMessage.textContent = "No users match the specified filters.";
        noUserMessage.className = "no-filter-message"; // Add a class for styling if needed
        userList.appendChild(noUserMessage);
        return;
    }

    users.forEach(user => {
        var link = document.createElement("a");
        link.href = `/dashboard/${user.id}`;
        link.className = "item-link";

        var div = document.createElement("div");
        div.className = "item";

        var img = document.createElement("img");
        img.src = user.picture ? `/static/user_images/${user.picture}` : '/static/games_images/default_image.jpg';
        img.className = "image";


        var p = document.createElement("p");
        p.textContent = user.name;
        p.className = "name";

        div.appendChild(img);
        div.appendChild(p);
        link.appendChild(div);
        userList.appendChild(link);
    });
}

// Filter functions
function filterUsers() {
    var companyId = document.getElementById("companyDropdown").value;
    var directorId = document.getElementById("directorDropdown").value;
    var founderId = document.getElementById("founderDropdown").value;
    var gameId = document.getElementById("gameDropdown").value;

    fetch(`/api/users?Game=${gameId}&Company=${companyId}&Director=${directorId}&Founder=${founderId}`)
        .then(response => response.json())
        .then(data => updateUserList(data.users))
        .catch(error => console.error('Error fetching users:', error));
}


// Update the company list
function updateCompanyList(companies) {
    var companyList = document.getElementById("companyList");
    companyList.innerHTML = ""; // Clear previous list

    if (companies.length === 0) {
        var noCompanyMessage = document.createElement("p");
        noCompanyMessage.textContent = "No companies match the specified filters.";
        noCompanyMessage.className = "no-filter-message"; // Add a class for styling if needed
        companyList.appendChild(noCompanyMessage);
        return;
    }

    companies.forEach(company => {
        var link = document.createElement("a");
        link.href = `/company/${company.id}`;
        link.className = "item-link";

        var img = document.createElement("img");
        img.src = company.picture_1 ? `/static/companies_images/${company.picture_1}` : '/static/games_images/default_image.jpg';
        img.className = "image";

        var div = document.createElement("div");
        div.className = "item";

        var p = document.createElement("p");
        p.textContent = company.name;
        p.className = "name";

        div.appendChild(img)
        div.appendChild(p);
        link.appendChild(div);
        companyList.appendChild(link);
    });
}


function filterCompanies() {
    var directorId = document.getElementById("directorDropdown").value;
    var seriesId = document.getElementById("seriesDropdown").value;
    var founderId = document.getElementById("founderDropdown").value;
    var userId = document.getElementById("usersDropdown").value;
    var gameId = document.getElementById("gameDropdown").value;

    fetch(`/api/companies?Director=${directorId}&Game=${gameId}&Series=${seriesId}&Founder=${founderId}&User=${userId}`)
        .then(response => response.json())
        .then(data => updateCompanyList(data.companies))
        .catch(error => console.error('Error fetching companies:', error));
}


// Update the director list
function updateDirectorList(directors) {
    var directorList = document.getElementById("directorList");
    directorList.innerHTML = ""; // Clear previous list

    if (directors.length === 0) {
        var noDirectorMessage = document.createElement("p");
        noDirectorMessage.textContent = "No directors match the specified filters.";
        noDirectorMessage.className = "no-filter-message"; // Add a class for styling if needed
        directorList.appendChild(noDirectorMessage);
        return;
    }

    directors.forEach(director => {
        var link = document.createElement("a");
        link.href = `/director/${director.id}`;
        link.className = "item-link";

        var div = document.createElement("div");
        div.className = "item";

        var p = document.createElement("p");
        p.textContent = director.name;
        p.className = "name";

        var img = document.createElement("img");
        img.src = director.picture_1 ? `/static/directors_images/${director.picture_1}` : '/static/games_images/default_image.jpg';
        img.className = "image";

        div.appendChild(img);
        div.appendChild(p);
        link.appendChild(div);
        directorList.appendChild(link);
    });
}

function filterDirectors() {
    var companyId = document.getElementById("companyDropdown").value;
    var gameId = document.getElementById("gameDropdown").value;
    var userId = document.getElementById("usersDropdown").value;

    fetch(`/api/directors?Company=${companyId}&Game=${gameId}&User=${userId}`)
        .then(response => response.json())
        .then(data => updateDirectorList(data.directors))
        .catch(error => console.error('Error fetching directors:', error));
}

// Update the founder list
function updateFounderList(founders) {
    var founderList = document.getElementById("founderList");
    founderList.innerHTML = ""; // Clear previous list

    if (founders.length === 0) {
        var noFounderMessage = document.createElement("p");
        noFounderMessage.textContent = "No founders match the specified filters.";
        noFounderMessage.className = "no-filter-message"; // Add a class for styling if needed
        founderList.appendChild(noFounderMessage);
        return;
    }

    founders.forEach(founder => {
        var link = document.createElement("a");
        link.href = `/founder/${founder.id}`;
        link.className = "item-link";

        var img = document.createElement("img");
        img.src = founder.picture_1 ? `/static/founders_images/${founder.picture_1}` : '/static/games_images/default_image.jpg';
        img.className = "image";

        var div = document.createElement("div");
        div.className = "item";

        var p = document.createElement("p");
        p.textContent = founder.name;
        p.className = "name";
        
        div.appendChild(img);
        div.appendChild(p);
        link.appendChild(div);
        founderList.appendChild(link);
    });
}

function filterFounders() {
    var companyId = document.getElementById("companyDropdown").value;
    var userId = document.getElementById("usersDropdown").value;
    

    fetch(`/api/founders?Company=${companyId}&User=${userId}`)
        .then(response => response.json())
        .then(data => updateFounderList(data.founders))
        .catch(error => console.error('Error fetching founders:', error));
}


// Fetch all lists on page load
window.addEventListener('load', () => {
    fetch(`/api/games`).then(response => response.json()).then(data => updateGameList(data.games));
    fetch(`/api/companies`).then(response => response.json()).then(data => updateCompanyList(data.companies));
    fetch(`/api/directors`).then(response => response.json()).then(data => updateDirectorList(data.directors));
    fetch(`/api/founders`).then(response => response.json()).then(data => updateFounderList(data.founders));
    fetch(`/api/users`).then(response => response.json()).then(data => updateUserList(data.users));
});

// Event listeners for filter buttons
document.getElementById('filterGamesButton').addEventListener('click', filterGames);
document.getElementById('filterCompaniesButton').addEventListener('click', filterCompanies);
document.getElementById('filterDirectorsButton').addEventListener('click', filterDirectors);
document.getElementById('filterFoundersButton').addEventListener('click', filterFounders);
document.getElementById('filterUsersButton').addEventListener('click', filterUsers);