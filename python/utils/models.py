from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "user_tb"
    
    user_idx = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), unique=True, index=True, nullable=False)
    pw = Column(String(255), nullable=False)
    user_name = Column(String(255), nullable=False)
    phone_number = Column(String(255))
    gender = Column(Integer, default=0)
    provider = Column(String(255), default="local")
    sns_id = Column(String(255))
    device_token = Column(String(255))
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")
    deleted_at = Column(TIMESTAMP)

    iots = relationship("IoT", back_populates="owner")
    subscriptions = relationship("Subscribe", back_populates="owner")
    inquiries = relationship("Inquiry", back_populates="user")
