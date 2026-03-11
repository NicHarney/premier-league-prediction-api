async function loadTeamsDropdown() {

    const response = await fetch("/api/teams/?page_size=100");
    const data = await response.json();

    const home = document.getElementById("homeTeam");
    const away = document.getElementById("awayTeam");

    home.innerHTML = "<option value=''>Any</option>";
    away.innerHTML = "<option value=''>Any</option>";

    data.results.forEach(team => {

        const option1 = document.createElement("option");
        option1.value = team.id;
        option1.textContent = team.name;

        const option2 = option1.cloneNode(true);

        home.appendChild(option1);
        away.appendChild(option2);

    });

}



async function searchTeams() {

    const query = document.getElementById("teamSearch")
        .value
        .toLowerCase()
        .trim();

    const response = await fetch("/api/teams/?page_size=100");
    const data = await response.json();

    const container = document.getElementById("results");

    const teams = data.results.filter(team => {

        const name = team.name.toLowerCase();

        return (
            name.includes(query) ||
            query.includes(name) ||
            name.replace("man", "manchester").includes(query) ||
            query.replace("manchester", "man").includes(name)
        );

    });

    if (teams.length === 0) {

        container.innerHTML = `
        <div class="alert alert-warning">
        No teams found.
        </div>
        `;

        return;

    }

    container.innerHTML = `

    <h3 class="mb-3">Teams</h3>

    <table class="table table-striped">

    <thead>
    <tr>
        <th>Name</th>
        <th>Home Attack</th>
        <th>Away Attack</th>
        <th>Home Defence</th>
        <th>Away Defence</th>
    </tr>
    </thead>

    <tbody>

    ${teams.map(team => `
        <tr>
            <td>${team.name}</td>
            <td>${team.home_attack_strength ?? "N/A"}</td>
            <td>${team.away_attack_strength ?? "N/A"}</td>
            <td>${team.home_defence_strength ?? "N/A"}</td>
            <td>${team.away_defence_strength ?? "N/A"}</td>
        </tr>
    `).join("")}

    </tbody>

    </table>

    `;
}


async function searchMatches() {

    const home = document.getElementById("homeTeam").value;
    const away = document.getElementById("awayTeam").value;
    const season = document.getElementById("season").value;
    
    let seasonQuery = "";
    if(season){
        const year = parseInt(season);

        if(!isNaN(year)){
            const start = (year - 1).toString().slice(-2);
            const end = year.toString().slice(-2);
            seasonQuery = start + end;

        }
        if(season.includes("/")){
            seasonQuery = season.replace("/", "");
        }
    }

    let query = "/api/matches/?";
    if(home) query += `home_team=${home}&`;
    if(away) query += `away_team=${away}&`;
    if(seasonQuery) query += `season=${seasonQuery}&`;


    const response = await fetch(query);
    const data = await response.json();

    const container = document.getElementById("results");

    if(data.results.length === 0){

        container.innerHTML = `
        <div class="alert alert-warning">
        No matches found.
        </div>
        `;

        return;

    }

    container.innerHTML = `

    <h3 class="mb-3">Matches</h3>

    <table class="table table-striped">

    <thead>

    <tr>
        <th>Date</th>
        <th>Home</th>
        <th>Away</th>
        <th>Score</th>
    </tr>

    </thead>

    <tbody>

    ${data.results.map(match => `
        <tr>
            <td>${match.match_date}</td>
            <td>${match.home_team_name}</td>
            <td>${match.away_team_name}</td>
            <td>${match.home_score} - ${match.away_score}</td>
        </tr>
    `).join("")}

    </tbody>

    </table>

    `;

}



document.addEventListener("DOMContentLoaded", loadTeamsDropdown);