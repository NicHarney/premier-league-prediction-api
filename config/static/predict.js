const API_BASE = "/api";

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

async function predictMatch() {

    const homeTeam = document.getElementById("homeTeam").value;
    const awayTeam = document.getElementById("awayTeam").value;

    if (homeTeam === awayTeam) {
        alert("Home and Away teams must be different");
        return;
    }

    try {

        const response = await fetch(`${API_BASE}/predictions/predict/`, {

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

        if (!response.ok) {

            handleApiError(response.status, data);
            return;

        }

        displayResults(data.data);

    } catch (error) {

        console.error("Prediction request failed:", error);

    }

}

function displayResults(data) {

    const results = document.getElementById("results");

    let scorelinesHTML = "";

    data.top_scorelines.slice(0, 5).forEach(s => {

        scorelinesHTML += `<li>${s.score} (${(s.probability * 100).toFixed(1)}%)</li>`;

    });

    results.innerHTML = `

    <div class="card p-4">

    <h3>${data.teams.home} vs ${data.teams.away}</h3>

    <h5 class="mt-3">Expected Goals</h5>
    Home: ${data.expected_goals.home} <br>
    Away: ${data.expected_goals.away}

    <h5 class="mt-3">Match Probabilities</h5>
    Home Win: ${(data.probabilities.home_win * 100).toFixed(1)}% <br>
    Draw: ${(data.probabilities.draw * 100).toFixed(1)}% <br>
    Away Win: ${(data.probabilities.away_win * 100).toFixed(1)}%

    <h5 class="mt-3">Goals Market</h5>
    Over 2.5: ${(data.totals.over_2_5 * 100).toFixed(1)}% <br>
    Under 2.5: ${(data.totals.under_2_5 * 100).toFixed(1)}%

    <h5 class="mt-3">Top Scorelines</h5>
    <ul>${scorelinesHTML}</ul>

    </div>

    `;

}

document.addEventListener("DOMContentLoaded", function () {
    loadTeams();
});