async function runBacktest() {

    const response = await fetch("/api/predictions/backtest/");

    const data = await response.json();

    displayResults(data.data);

}


function displayResults(data) {

    const container = document.getElementById("results");

    container.innerHTML = `

    <div class="row text-center">

        <div class="col-md-3">
            <div class="card p-3 shadow">
                <h4>Matches Tested</h4>
                <h2>${data.matches_tested}</h2>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card p-3 shadow">
                <h4>Bets Placed</h4>
                <h2>${data.bets_placed}</h2>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card p-3 shadow">
                <h4>Wins</h4>
                <h2>${data.wins}</h2>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card p-3 shadow">
                <h4>ROI</h4>
                <h2>${(data.roi * 100).toFixed(2)}%</h2>
            </div>
        </div>

    </div>

    <div class="card mt-4 p-4 text-center shadow">

        <h4>Total Profit</h4>

        <h2>${data.profit}</h2>

    </div>

    `;

}