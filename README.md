# Premier League Prediction & Betting Value analytics API #
## Overview ##
This project is a data-driven sports analytics API built using Django and the Django REST FRAMEWORK. It allows users to access premier league data from 2015 to 2026, including:
- Match data
- Team data
- predictive modelling
- betting value analysis
- Backtesting analysis

This API uses this publicly available data, at [https://www.football-data.co.uk/data.php], to calculate team home and away attack and defence strengths to then calculate expected goals. This calculation then allows the API to simulate match outcomes using Poisson probability models and then spot odds mismatches with live bookmakers. In order to evaluate the accuracy of the API, a backtesting engine is included to show how practical the model is for previous seasons. 

This project includes advanced backend engineering concepts including statistical modelling, rate limiting, automated testing and modular architecture.

## Key Features ##
### Core API Functionality ###
Provides full CRUD support for the following entities:
- Teams
- Matches
- Players 
- Player Match Statistics 
- Betting odds

Endpoints support filtering, searching and ordering to allow flexible data access.

### Predictive Match Modelling ###
The API estimates match outcomes using a Poisson-based statistical model.

The model:
1. Calculates team attack and defence strength, separate for home and away
2. Uses league goal averages
3. Computes expected goals
4. Simulates match scorelines probabilistically
From this it dervies probabilities for:
- Home win
- Draw
- Away win
- Over/Under 2.5 goals
- Most likely scorelines
A Dixon-Coles adjustment is applied to improve the probability of low-scoring outcomes, as per industry standard.

### Value Betting Analytics ###
After calculating probabilities, the system can then compare results to bookmaker odds to identify positive value bets. The expected value is calculated by: 
- EV = (model_probability x odds) -1
If EV is positive -> possible betting opportunity.

### Historical Backtesting ###
The API has a backtesting engine that evaluates model accuracy from previous matches. It simulates placing a bet when the predicted edge exceeds a threshold and this predicted edge provides a positve possible betting opportunity.
It then returns:
- number of matches tested
- number of bets placed
- number of wins
- total profit
- return on investment (ROI)
This provides a quantative evaluation of model performance.

### Data Explorer Interface ###
A frontend feature allowing users to analyse the database.

The interface supports:
- Predicting match outcomes
- Calculating value bets
- running model backtests
- exploring teams and matches
- filtering historical seasons

### Backend Player data ###
As the API mainly focuses on team and match prediction, player integration holds as a background feature that would be improved on in the future. Currently, as it does not affect predictions, it is only seen in the backend and the API docs. It can be accessed through the route /api/players for player information and api/player-match-stats. Both of these have CRUD integration and users can access individual players through {id} search within these routes.

## System Architecture ## 
Modular Django architecture:
- project
  - analytics
      - management
        - commands
            - calculate_team_strengths.py
      - migrations
      - services
        - team_strength_service.py
        - weighting.py
    - admin.py
    - apps.py
    - models.py
    - serializers.py 
    - views.py
  - config
    - settings.py
    - urls.py
  - matches
    - management
      - commands
        - load_football_data.py
        - load_player_stats.py
    - migrations
    - tests
      - test_matches.py
    - admin.py
    - apps.py
    - managers.py
    - models.py
    - serializers.py
    - views.py
  - players
    - data
      - player_match_stats.csv
      - players.csv
    - management
      - commands
        - load_players.py
    - migrations
    - admin.py
    - apps.py
    - models.py
    - serializers.py
    - views.py
  - predictions
    - migrations
    - services
      - backtest.py
      - dixon_coles.py
      - expected_goals.py
      - poisson_model.py
      - value_bets.py
    - tests
      - test_backtest.py
      - test_predictions.py
      - test_throttling.py
      - test_value.py
    - admin.py
    - apps.py
    - models.py
    - serializers.py
    - throttles.py
    - urls.py
    - views.py
  - static
    - backtest.js
    - explorer.js
    - predict.js
    - styles.css
    - value.js
  - teams
    - migrations
    - tests
      - test_teams.py
    - admin.py
    - apps.py
    - models.py
    - serializers.py
    - views.py
  - templates
    - backtest.html
    - explorer.html
    - index.html
    - predict.html
    - value.html

### Architecture Principles ###
- Domain-driven app separation
- Service layer for business logic
- RESTful API design
- Serializer validation for input security
- Modular prediction engine

This structure focuses on **maintainability, scalability and testability**.

## Data Models ##
Key entities include:

### Team ###
Stores team information and derived stats such as attack and defence strengths.

### Player ###
Stores player information such as the team they played for and date of birth.

### Match ###
Stores match results including:
- home team
- away team
- goals scored
- season 
- match date

### Player Match Stats
Stores player stats per game.

### Betting odds ###
Stores bookmaker odds for match outcomes used in value analysis.

## Security Features ##

### Rate Limiting ###
Custom throttling classes prevent abuse of prediction and backtesting endpoints

### Input Validation
All API inputs are validated using serializers to enforce:
- valid team IDs
- realistic odds values
- prevention of invalid matchups
- correct data types

### Error Handling ###
Endpoints return structured JSON responses with appropriate HTTP status codes:
- 200 OK
- 400 Bad Request
- 404 Not Found
- 429 Too many requests
- 500 Internal Server Error

## Testing ##
A comprehensive automated test suite ensures reliability and correctness.

Tests cover:
- API Endpoints
- Serializer validation
- rate limiting
- prediction logic
- value betting calculations
- filtering functionality

Example test categories:
- predictions/tests
- matches/tests
- teams/tests

**Tests are executed using:**

**python manage.py test**

## API Documentation ##
Interactive API documentation is available through Swagger:
**api/docs**

This allows exploration of endpoints and request formats directly from the browser. All endpoints are seen in this doc, all of them allow users to enter parameters in JSON format. A couple of important things to note for certain searches:
- For POST /api/betting-odds the user should go to POST /api/matches and create a new match and make note of the ID before adding odds, and when entering odds use this new match ID as the system has in built protection of changing odds in matches already in the system.
- For PUT /api/betting-odds{id}, team IDs and match ID must line up to protect against invalid inputs, use GET /api/betting-odds to check for valid inputs
- For GET /api/matches, ordering can be match_date and -match_date
- For GET /api/matches/{id}, verify valid match IDs first through standard GET /api/matches, as the system protects against invalid match IDs and so a valid ID must be inputted to retrieve information
- For GET /api/matches/{id}/player_stats, as the player data is sampled and not there for every match, use GET api/player-match-stats/ to check match IDs that have player stats data first

## Example Endpoints ##
### Predict Match Outcome ###
**POST /api/predictions/predict**

Input
{
  "home_team":1,
  "away_team":2
}

Response includes:
- expected goals
- win probabilities
- scoreline probabilities

### Value Betting Analysis ###
**POST /api/predictions/value**
{
  "home_team":1,
  "away_team":2,
  "home_odds":2.2,
  "draw_odds":3.4,
  "away_odds":3.1
}

Returns expected value for each market

### Backtesting ###
**GET /api/predictions/backtest**
Returns model performance metrics including ROI. Please note that as this loads data from over 4000 rows, it will take a couple of minutes to return its metrics.

### Other endpoints ###
-**/api/teams**
- **api/matches**
- **api/players**
- **api/player-match-stats**
- **api/betting-odds**

For teams and matches, entering urls such as "/api/teams/1" returns unique teams/matches which can be updated. Through these Urls users can also create new teams/matches that will be live inputted into the database.

## Data Sources ##
Match and odds data are sourced from publicly available datasets. These datasets provide:
- historical match results
- bookmaker odds
- season statistics

## Running the Project ##
### Install dependencies ###
**pip install -r requirements.txt**

### Apply migrations ###
**python manage.py migrate**

### Load datasets ###
**python manage.py load_football_data**
**python manage.py load_players**
**python manage.py load_player_stats**


## Start Server ##
**python manage.py runserver**

## Run tests ##
**python manage.py test**

## Technologies Used ##
- python
- Django
- Django REST Framework
- SQLite
- Docker
- Swagger (drf-spectacular)
- JavaScript frontend

## Conclusion ##
This project demonstrates the application of software enginnering principles to API design, combining statistical modelling, secure RESTful architecture and comprehensive testing to produce a robust sports analytics platform.


