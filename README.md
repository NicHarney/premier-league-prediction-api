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
- ==EV = (model_probability x odds) -1 ==

