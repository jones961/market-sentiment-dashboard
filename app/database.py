from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///sentiment.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class SentimentRun(Base):
    __tablename__ = "sentiment_runs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source = Column(String)
    num_headlines = Column(Integer)
    avg_positive = Column(Float)
    avg_negative = Column(Float)
    avg_neutral = Column(Float)
    classification = Column(String)
    topics = Column(String)
    summary = Column(String)


def init_db():
    Base.metadata.create_all(bind=engine)
