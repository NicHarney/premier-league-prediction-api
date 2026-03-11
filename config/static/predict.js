const API_BASE = "/api";

async function loadTeams() {

    try {

        const response = await fetch(`${API_BASE}/teams/`);
        const data = await response.json();

        const homeSelect = document.getElementById("homeTeam");
        const awaySelect = document.getElementById("awayTeam");

        // clear existing
        homeSelect.innerHTML = "";
        awaySelect.innerHTML = "";

        data.results.forEach(team => {

            const homeOption = document.createElement("option");
            homeOption.value = team.id;
            homeOption.textContent = team.name;

            const awayOption = document.createElement("option");
            awayOption.value = team.id;
            awayOption.textContent = team.name;

            homeSelect.appendChild(homeOption);
            awaySelect.appendChild(awayOption);

        });

    } catch (error) {

        console.error("Error loading teams:", error);

    }

}

async function predictMatch() {

    const homeTeam = document.getElementById("homeTeam").value;
    const awayTeam = document.getElementById("awayTeam").value;

    if (homeTeam === awayTeam) {
        alert("Home and Away teams must be different");
        return;
    }

    const response = await fetch("/api/predictions/predict/", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            home_team: homeTeam,
            away_team: awayTeam
        })

    });

    const data = await response.json();

    displayResults(data.data);
}

function displayResults(data) {

    const results = document.getElementById("results");

    let scorelinesHTML = "";

    data.top_scorelines.slice(0,5).forEach(s => {

        scorelinesHTML += `<li>${s.score} (${(s.probability*100).toFixed(1)}%)</li>`;

    });

    results.innerHTML = `

    <div class="card p-4">

    <h3>${data.teams.home} vs ${data.teams.away}</h3>

    <h5 class="mt-3">Expected Goals</h5>
    Home: ${data.expected_goals.home} <br>
    Away: ${data.expected_goals.away}

    <h5 class="mt-3">Match Probabilities</h5>
    Home Win: ${(data.probabilities.home_win*100).toFixed(1)}% <br>
    Draw: ${(data.probabilities.draw*100).toFixed(1)}% <br>
    Away Win: ${(data.probabilities.away_win*100).toFixed(1)}%

    <h5 class="mt-3">Goals Market</h5>
    Over 2.5: ${(data.totals.over_2_5*100).toFixed(1)}% <br>
    Under 2.5: ${(data.totals.under_2_5*100).toFixed(1)}%

    <h5 class="mt-3">Top Scorelines</h5>
    <ul>${scorelinesHTML}</ul>

    </div>

    `;

}

document.addEventListener("DOMContentLoaded", function() {
    loadTeams();
});