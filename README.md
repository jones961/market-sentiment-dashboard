Market Sentiment Analysis Dashboard
Overview

This project collects, analyses, and visualises market sentiment from financial news headlines. It implements an end-to-end pipeline that scrapes headlines, cleans text, performs sentiment analysis, extracts key topics, classifies overall market sentiment, and generates a short summary. Results are persisted in a local SQLite database and exposed via a FastAPI backend and an interactive Streamlit dashboard.

Features

Automated scraping — collects finance headlines (currently via an RSS feed).

Sentiment analysis — computes average positive, negative, and neutral scores for headlines.

Topic extraction — identifies dominant topics from recent headlines.

Market classification — produces a concise market classification (e.g., Bullish, Bearish, Neutral).

Summary generation — generates a short natural-language summary describing recent market drivers.

Dashboard visualisation — interactive Streamlit UI includes:

current sentiment metrics

a bar chart of sentiment distribution

historical runs of sentiment analysis

the latest summary and classification

## Project Structure

```
WebScraper/
├── app/                  # FastAPI backend
│   ├── database.py
│   ├── main.py
│   └── logger.py
├── core/                 # Core pipeline logic
│   ├── scraper.py
│   ├── preprocess.py
│   ├── sentiment.py
│   ├── aggregator.py
│   ├── classifier.py
│   ├── summariser.py
│   └── pipeline.py
├── dashboard/            # Streamlit frontend
│   └── app.py
├── requirements.txt
├── sentiment.db          # SQLite database (runtime; usually gitignored)
└── README.md
```

Installation

Clone the repository:

git clone <repository_url>
cd WebScraper


Create and activate a virtual environment:

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate


Install dependencies:

pip install -r requirements.txt

Usage
Start the backend API
uvicorn app.main:app --reload


API documentation: http://127.0.0.1:8000/docs

Endpoints:

GET /health — health check

POST /run — run sentiment analysis and return the result

Start the dashboard
streamlit run dashboard/app.py


Dashboard: http://localhost:8501

Use the dashboard to run new analyses, view charts and trends, and inspect historical runs.

Example API response
```
{
  "source": "Reuters",
  "num_headlines": 10,
  "avg_positive": 0.26,
  "avg_negative": 0.25,
  "avg_neutral": 0.48,
  "classification": "Neutral / Mixed",
  "topics": ["trump", "deal", "markets"],
  "summary": "Markets show mixed sentiment driven by geopolitical and corporate developments."
}
```

Technologies

Python 3.9+

FastAPI - API

Streamlit - dashboard

SQLite - lightweight persistence

Pandas & Matplotlib - data handling and charts

Requests & BeautifulSoup - web scraping

Notes

Ensure you have a stable internet connection to fetch headlines from the RSS source.

The system currently targets one RSS feed but can be extended to additional sources.

The sentiment.db file contains historical runs and should usually be added to .gitignore in public repositories.

Future work

Add multiple news sources (CNBC, Bloomberg, Reuters, etc.).

Improve topic extraction with NLP models or named-entity recognition.

Add interactive filters and more trend analytics to the dashboard.

Containerise the application and deploy to a cloud provider.

Add authentication and user profiles if it becomes a multi-user product.
