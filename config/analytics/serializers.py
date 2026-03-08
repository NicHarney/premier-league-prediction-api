from rest_framework import serializers
from .models import BettingOdds


class BettingOddsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BettingOdds
        fields = "__all__"