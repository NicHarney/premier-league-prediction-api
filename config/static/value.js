function handleApiError(status, data) {

    const container = document.getElementById("results");

    if (status === 400) {

        const errors = Object.entries(data)
            .map(([field, messages]) =>
                `<li><strong>${field}</strong>: ${messages.join(", ")}</li>`
            )
            .join("");

        container.innerHTML = `
        <div class="alert alert-warning">
        <strong>Input error:</strong>
        <ul>${errors}</ul>
        </div>
        `;

        return;
    }

    if (status === 429) {

        container.innerHTML = `
        <div class="alert alert-danger">
        Too many requests. Please wait before trying again.
        </div>
        `;

        return;
    }

    container.innerHTML = `
    <div class="alert alert-danger">
    Server error (${status})
    </div>
    `;
}
async function loadTeams() {

    try {

        let url = "/api/teams/";
        let teams = [];

        while (url) {

            const response = await fetch(url);
            const data = await response.json();

            // Handle paginated responses
            if (data.results) {
                teams = teams.concat(data.results);
                url = data.next;
            } else {
                // Non-paginated fallback
                teams = data;
                url = null;
            }

        }

        const homeSelect = document.getElementById("homeTeam");
        const awaySelect = document.getElementById("awayTeam");

        homeSelect.innerHTML = "";
        awaySelect.innerHTML = "";

        teams
            .sort((a, b) => a.name.localeCompare(b.name))
            .forEach(team => {

                const homeOption = new Option(team.name, team.id);
                const awayOption = new Option(team.name, team.id);

                homeSelect.add(homeOption);
                awaySelect.add(awayOption);

            });

    } catch (error) {

        console.error("Error loading teams:", error);

    }
}

async function calculateValue() {

    const homeTeam = document.getElementById("homeTeam").value;
    const awayTeam = document.getElementById("awayTeam").value;

    if (homeTeam === awayTeam) {
        alert("Home and Away teams must be different");
        return;
    }
    const homeOdds = document.getElementById("homeOdds").value;
    const drawOdds = document.getElementById("drawOdds").value;
    const awayOdds = document.getElementById("awayOdds").value;

    const response = await fetch("/api/predictions/value/", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            home_team: homeTeam,
            away_team: awayTeam,
            home_odds: homeOdds,
            draw_odds: drawOdds,
            away_odds: awayOdds

        })

    });

    const data = await response.json();


    if(!response.ok) {

       handleApiError(response.status,data);
       return;
    }
    
    

    displayResults(data.data);

}

function displayResults(data) {

    const container = document.getElementById("results");

    const markets = data?.markets || data?.value_markets;

    if (!markets) {
        container.innerHTML = `
            <div class="alert alert-danger">
                Could not load value betting results.
            </div>
        `;
        return;
    }

    container.innerHTML = `
    <div class="card p-4">

    <h4>Value Analysis</h4>

    <table class="table mt-3">

    <thead>
    <tr>
        <th>Market</th>
        <th>Model Probability</th>
        <th>Odds</th>
        <th>Expected Value</th>
    </tr>
    </thead>

    <tbody>

    ${Object.entries(markets).map(([market, m]) => `
        <tr>
            <td>${market}</td>
            <td>${(m.probability * 100).toFixed(2)}%</td>
            <td>${m.odds}</td>
            <td>${m.ev.toFixed(3)}</td>
        </tr>
    `).join("")}

    </tbody>

    </table>

    </div>
    `;
}

document.addEventListener("DOMContentLoaded", loadTeams);