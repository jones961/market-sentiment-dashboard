from fastapi import FastAPI
import sqlite3

app = FastAPI()

DB_PATH = "sentiment.db"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/run")
def run():
    from core.pipeline import run_pipeline
    result = run_pipeline()
    return result


@app.get("/history")
def history(limit: int = 10):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM sentiment_runs
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]
