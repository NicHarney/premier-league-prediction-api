from django.urls import path

from .views import (
    predict_match_view,
    value_bet_view,
    backtest_view,
)

urlpatterns = [
    path("predict/", predict_match_view, name="predict-match"),
    path("value/", value_bet_view, name="value-bet"),
    path("backtest/", backtest_view, name="backtest"),
]