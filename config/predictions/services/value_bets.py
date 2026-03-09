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


def evaluate_match_value(predictions, odds):

    value = {}

    def compute_value(model_prob, market_odds):

        if market_odds is None:
            return None

        bookmaker_prob = 1 / market_odds

        return {
            "model_probability": model_prob,
            "bookmaker_probability": bookmaker_prob,
            "value": model_prob - bookmaker_prob
        }


    value["home_win"] = compute_value(
        predictions["home_win_probability"],
        odds["home_win"]
    )

    value["draw"] = compute_value(
        predictions["draw_probability"],
        odds["draw"]
    )

    value["away_win"] = compute_value(
        predictions["away_win_probability"],
        odds["away_win"]
    )

    value["over_2_5"] = compute_value(
        predictions["over_2_5_goals"],
        odds["over_2_5"]
    )

    value["under_2_5"] = compute_value(
        predictions["under_2_5_goals"],
        odds["under_2_5"]
    )

    return value