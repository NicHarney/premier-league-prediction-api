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
- Players (no data populated)
- Player Match Statistics (no data populated)
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
Would represent individual players and their team -> out of scope.

### Match ###
Stores match results including:
- home team
- away team
- goals scored
- season 
- match date

### Player Match Stats
Would store per match player performance such as goals, assists, shots and fouls.

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

** Tests are executed using:**
==python manage.py test==

