from transformers import pipeline

summariser = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

def summarise_market(headlines, stats, topics):
    input_text = (
        f"Market sentiment overview.\n\n"
        f"Headlines:\n" +
        "\n".join(headlines) +
        f"\n\nStatistics:\n"
        f"Positive: {stats['avg_positive']:.2f}, "
        f"Negative: {stats['avg_negative']:.2f}, "
        f"Neutral: {stats['avg_neutral']:.2f}\n\n"
        f"Key topics: {', '.join(topics)}"
    )

    summary = summariser(
        input_text,
        max_length=120,
        min_length=60,
        do_sample=False
    )[0]["summary_text"]

    return summary
