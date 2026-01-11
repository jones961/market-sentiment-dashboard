import logging
import pandas as pd

from core.scraper import scrape_reuters_finance
from core.preprocess import clean_text
from core.sentiment import get_sentiment
from core.aggregator import aggregate_sentiment, extract_topics
from core.classifier import classify_market
from core.summariser import summarise_market


# ------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------
# Pipeline
# ------------------------------------------------------------------
def run_pipeline(n_headlines: int = 10) -> dict:
    logger.info("Starting market sentiment pipeline")

    # 1️⃣ Scrape
    logger.info("Scraping Reuters finance headlines")
    headlines = scrape_reuters_finance(limit=n_headlines)
    logger.info(f"Collected {len(headlines)} headlines")

    # 2️⃣ Clean
    logger.info("Cleaning text")
    cleaned = [clean_text(h) for h in headlines]

    # 3️⃣ Sentiment
    logger.info("Running sentiment analysis")
    sentiment_results = [get_sentiment(text) for text in cleaned]

    df = pd.DataFrame(sentiment_results)

    # 4️⃣ Aggregate
    logger.info("Aggregating sentiment scores")
    stats = aggregate_sentiment(df)

    # 5️⃣ Topics
    logger.info("Extracting topics")
    topics = extract_topics(cleaned, top_n=5)

    # 6️⃣ Classification
    logger.info("Classifying overall market sentiment")
    classification = classify_market(stats)

    # 7️⃣ Summary
    logger.info("Generating market summary")
    summary = summarise_market(headlines, stats, topics)

    logger.info("Pipeline finished successfully")

    return {
        "source": "Reuters",
        "num_headlines": stats["num_headlines"],
        "avg_positive": stats["avg_positive"],
        "avg_negative": stats["avg_negative"],
        "avg_neutral": stats["avg_neutral"],
        "classification": classification,
        "topics": topics,
        "summary": summary
    }


# Optional local run
if __name__ == "__main__":
    import json
    print(json.dumps(run_pipeline(), indent=2))

