# app/schemas.py
from pydantic import BaseModel
from typing import List


class SentimentResponse(BaseModel):
    source: str
    num_headlines: int
    avg_positive: float
    avg_negative: float
    avg_neutral: float
    classification: str
    topics: List[str]
    summary: str
