from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
import sys

# add throttles for rate limiting
class PredictionThrottle(UserRateThrottle):
    scope = 'prediction'

    def allow_request(self,request,view):

        if "test" in sys.argv:
            return True
       

        return super().allow_request(request,view)

class BacktestThrottle(UserRateThrottle):

    scope = 'backtest'
    def allow_request(self, request, view):

        if "test" in sys.argv:
            return True
        
        return super().allow_request(request,view)
