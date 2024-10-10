from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    p5_balance = Column(Integer, default=100)
    rewards_balance = Column(Integer, default=0)

    # Relationship to track the rewards given by this user and received by this user
    rewards_given = relationship("RewardHistory", foreign_keys="[RewardHistory.given_by_id]", back_populates="given_by")
    rewards_received = relationship("RewardHistory", foreign_keys="[RewardHistory.given_to_id]", back_populates="given_to")


class RewardHistory(Base):
    __tablename__ = "reward_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    points = Column(Integer)

    # Foreign keys to link the User entities who give and receive rewards
    given_by_id = Column(String, ForeignKey("users.id"), nullable=False)
    given_to_id = Column(String, ForeignKey("users.id"), nullable=False)

    # Relationships with the User entity
    given_by = relationship("User", foreign_keys=[given_by_id], back_populates="rewards_given")
    given_to = relationship("User", foreign_keys=[given_to_id], back_populates="rewards_received")
