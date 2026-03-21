from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    roadmaps = relationship("Roadmap", back_populates="owner")

class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    goal = Column(String, index=True)
    roadmap = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="roadmaps")