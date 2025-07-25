import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSON, UUID as PG_UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class JournalAnalysis(Base):
    __tablename__ = "journal_analysis"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    journal_id = Column(PG_UUID(as_uuid=True), nullable=False)
    user_id = Column(PG_UUID(as_uuid=True), nullable=False, index=True)

    analysis_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    readability = Column(Float)
    sentiment_score = Column(Float)
    self_talk_tone = Column(String)
    energy_score = Column(Float)
    keywords = Column(JSON)
    text_mood = Column(JSON)
    emoji_mood = Column(JSON)
    image_mood = Column(JSON)
    combined_mood = Column(JSON)
    goal_mentions = Column(JSON)
    topics = Column(JSON)
    text_vector = Column(String)
    text_embedding = Column(JSON)
    extracted_actions = Column(String)
    date = Column(String)
    model = Column(String, nullable=False)


class ConnectedAnalysis(Base):
    __tablename__ = "connected_analysis"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    mood_trends = Column(JSON)
    energy_trends = Column(JSON)
    average_sentiment = Column(Float)
    goal_emotion_map = Column(JSON)
    goal_progress = Column(JSON)
    goal_matches = Column(JSON)
    keyword_emotion_map = Column(JSON)
    keyword_energy_map = Column(JSON)
    journal_weights = Column(JSON)
    model = Column(String, nullable=False)

    feedback = relationship("Feedback", back_populates="connected_analysis", lazy="joined")


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), nullable=False)
    connected_analysis_id = Column(PG_UUID(as_uuid=True), ForeignKey("connected_analysis.id"), nullable=False)
    
    tone = Column(String, nullable=False)
    feedback = Column(String, nullable=False)
    reflective_question = Column(String, nullable=False)
    motivation = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    connected_analysis = relationship("ConnectedAnalysis", back_populates="feedback", lazy="joined")
