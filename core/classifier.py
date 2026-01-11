def classify_market(stats: dict) -> str:
    pos = stats["avg_positive"]
    neg = stats["avg_negative"]

    if pos > 0.55 and pos > neg:
        return "Bullish"
    elif neg > 0.55 and neg > pos:
        return "Bearish"
    else:
        return "Neutral / Mixed"
