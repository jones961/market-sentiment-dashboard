import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def aggregate_sentiment(df: pd.DataFrame) -> dict:
    avg_positive = df["positive"].mean()
    avg_negative = df["negative"].mean()
    avg_neutral = df["neutral"].mean()

    return {
        "avg_positive": avg_positive,
        "avg_negative": avg_negative,
        "avg_neutral": avg_neutral,
        "num_headlines": len(df)
    }

def extract_topics(texts, top_n=5):
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=50
    )
    tfidf = vectorizer.fit_transform(texts)
    scores = tfidf.sum(axis=0).A1

    terms = vectorizer.get_feature_names_out()
    ranked = sorted(zip(terms, scores), key=lambda x: x[1], reverse=True)

    return [term for term, _ in ranked[:top_n]]
