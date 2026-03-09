def decimal_odds_to_probability(odds):
    return 1 / odds


def calculate_value(model_prob, odds):

    bookmaker_prob = decimal_odds_to_probability(odds)

    value = model_prob - bookmaker_prob

    return {
        "bookmaker_probability": round(bookmaker_prob, 3),
        "model_probability": round(model_prob, 3),
        "value": round(value, 3)
    }


def evaluate_match_value(model_predictions, odds):

    results = {}

    results["home_win"] = calculate_value(
        model_predictions["home_win_probability"],
        odds["home_win"]
    )

    results["draw"] = calculate_value(
        model_predictions["draw_probability"],
        odds["draw"]
    )

    results["away_win"] = calculate_value(
        model_predictions["away_win_probability"],
        odds["away_win"]
    )

    return results