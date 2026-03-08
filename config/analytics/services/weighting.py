from django.utils import timezone
import math


DECAY_RATE = 0.002


def match_weight(match_date):

    today = timezone.now()

    days_old = (today - match_date).days

    weight = math.exp(-DECAY_RATE * days_old)

    return weight