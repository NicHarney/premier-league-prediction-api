async function loadTeams() {

    const response = await fetch("/api/teams/");
    const data = await response.json();

    const homeSelect = document.getElementById("homeTeam");
    const awaySelect = document.getElementById("awayTeam");

    homeSelect.innerHTML = "";
    awaySelect.innerHTML = "";

    data.results.forEach(team => {

        const option1 = document.createElement("option");
        option1.value = team.id;
        option1.textContent = team.name;

        const option2 = document.createElement("option");
        option2.value = team.id;
        option2.textContent = team.name;

        homeSelect.appendChild(option1);
        awaySelect.appendChild(option2);

    });

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