import streamlit as st
import pandas as pd
import requests
import sqlite3

API_URL = "http://127.0.0.1:8000"
DB_PATH = "sentiment.db"

st.set_page_config(
    page_title="Market Sentiment Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📈 Market Sentiment Dashboard")

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.header("⚙️ Controls")

headline_limit = st.sidebar.slider(
    "Headlines to analyze",
    min_value=5,
    max_value=50,
    value=10
)

# -----------------------------
# Run sentiment analysis
# -----------------------------
st.subheader("▶️ Run New Sentiment Analysis")

if st.button("Run Sentiment Analysis"):
    try:
        response = requests.post(f"{API_URL}/run", timeout=60)

        if response.status_code != 200:
            st.error("Invalid API response")
            st.json(response.json())
        else:
            result = response.json()

            # Insert into DB
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO sentiment_runs (
                    timestamp,
                    source,
                    num_headlines,
                    avg_positive,
                    avg_negative,
                    avg_neutral,
                    classification,
                    topics,
                    summary
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pd.Timestamp.utcnow().isoformat(),
                result["source"],
                result["num_headlines"],
                result["avg_positive"],
                result["avg_negative"],
                result["avg_neutral"],
                result["classification"],
                ", ".join(result["topics"]),
                result["summary"]
            ))

            conn.commit()
            conn.close()

            st.success("✅ Sentiment analysis completed and saved!")

    except Exception as e:
        st.error(f"Failed to run analysis: {e}")

st.divider()

# -----------------------------
# Load historical data
# -----------------------------
st.subheader("📜 Historical Sentiment Runs")

n = st.slider("Number of past runs to display", 5, 50, 10)

try:
    history = requests.get(
        f"{API_URL}/history?limit={n}",
        timeout=10
    ).json()
except Exception:
    history = []

if not history:
    st.info("No historical data available yet.")
    st.stop()

df = pd.DataFrame(history)

# Ensure proper ordering
df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce",
    utc=True
)

df = df.dropna(subset=["timestamp"])
df = df.sort_values("timestamp", ascending=False)


# -----------------------------
# Latest summary
# -----------------------------
st.subheader("📝 Latest Market Summary")

latest = df.iloc[0]

st.subheader("📌 Market Classification")

classification = latest["classification"]

if "Bull" in classification:
    st.success(classification)
elif "Bear" in classification:
    st.error(classification)
else:
    st.warning(classification)

st.markdown(f"""
**Source:** {latest['source']}  
**Classification:** `{latest['classification']}`  
**Headlines Analyzed:** {latest['num_headlines']}  

**Summary:**  
{latest['summary']}
""")

if len(df) > 1:
    prev = df.iloc[1]

    delta_pos = latest["avg_positive"] - prev["avg_positive"]
    delta_neg = latest["avg_negative"] - prev["avg_negative"]

    st.caption(
        f"Δ Positive: {delta_pos:+.2f} | Δ Negative: {delta_neg:+.2f}"
    )

st.subheader("📌 Latest Snapshot")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Market Mood", latest["classification"])
col2.metric("Positive", f"{latest['avg_positive']:.2f}")
col3.metric("Negative", f"{latest['avg_negative']:.2f}")
col4.metric("Headlines", latest["num_headlines"])
st.divider()


# -----------------------------
# Sentiment bar chart (latest)
# -----------------------------
st.subheader("📊 Latest Sentiment Breakdown")

sentiment_df = pd.DataFrame({
    "Sentiment": ["Positive", "Negative", "Neutral"],
    "Score": [
        latest["avg_positive"],
        latest["avg_negative"],
        latest["avg_neutral"]
    ]
})

st.bar_chart(sentiment_df.set_index("Sentiment"))

st.divider()

# -----------------------------
# Historical sentiment trends
# -----------------------------
st.subheader("📈 Sentiment Trends Over Time")

trend_df = df.sort_values("timestamp")

trend_df = trend_df[[
    "timestamp",
    "avg_positive",
    "avg_negative",
    "avg_neutral"
]].set_index("timestamp")

trend_df = trend_df.rename(columns={
    "avg_positive": "Positive",
    "avg_negative": "Negative",
    "avg_neutral": "Neutral"
})

st.line_chart(trend_df)

st.divider()

# -----------------------------
# Raw data table
# -----------------------------
st.divider()

with st.expander("🔍 View Raw Historical Data"):
    st.dataframe(df, use_container_width=True)

