# calculate expected value
def expected_value(prob, odds):

    if odds is None:
        return None

    return prob * odds - 1

# calculate ev and market edge
def evaluate_markets(predictions, odds):

    markets = {}

    # normalize 1X2 probabilities
    if odds["home_win"] and odds["draw"] and odds["away_win"]:
        p_home = 1 / odds["home_win"]
        p_draw = 1 / odds["draw"]
        p_away = 1 / odds["away_win"]

        total = p_home + p_draw + p_away

        bookmaker_probs = {
            "home_win": p_home / total,
            "draw": p_draw / total,
            "away_win": p_away / total,
        }
    else:
        bookmaker_probs = {}

    for market in predictions:

        if market not in odds:
            continue

        if odds[market] is None:
            continue

        model_prob = predictions[market]

        if market in bookmaker_probs:
            bookmaker_prob = bookmaker_probs[market]
        else:
            bookmaker_prob = 1 / odds[market]

        edge = model_prob - bookmaker_prob
        ev = model_prob * odds[market] - 1

        markets[market] = {
            "probability": model_prob,
            "bookmaker_probability": bookmaker_prob,
            "odds": odds[market],
            "edge": edge,
            "ev": ev
        }

    return markets