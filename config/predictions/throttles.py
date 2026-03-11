from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class PredictionThrottle(UserRateThrottle):
    scope = 'prediction'

class BacktestThrottle(UserRateThrottle):
    scope = 'backtest'