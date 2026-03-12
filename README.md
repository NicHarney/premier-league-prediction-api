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
