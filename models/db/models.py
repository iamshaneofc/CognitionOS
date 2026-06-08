from shared.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, JSON

# empty SQLAlchemy Base classes for User, Session, TelemetryEvent, SentimentScore, CognitiveScore, ConsentRecord, Intervention

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)

class TelemetryEvent(Base):
    __tablename__ = "telemetry_events"
    id = Column(Integer, primary_key=True, index=True)

class SentimentScore(Base):
    __tablename__ = "sentiment_scores"
    id = Column(Integer, primary_key=True, index=True)

class CognitiveScore(Base):
    __tablename__ = "cognitive_scores"
    id = Column(Integer, primary_key=True, index=True)

class ConsentRecord(Base):
    __tablename__ = "consent_records"
    id = Column(Integer, primary_key=True, index=True)

class Intervention(Base):
    __tablename__ = "interventions"
    id = Column(Integer, primary_key=True, index=True)
