"""
Database setup and models
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import Optional
import logging

from .config import config

logger = logging.getLogger(__name__)

# Create database engine
engine = create_engine(
    config.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in config.DATABASE_URL else {},
    echo=config.DATABASE_ECHO
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


class FundModel(Base):
    """Fund database model"""
    __tablename__ = "funds"
    
    id = Column(Integer, primary_key=True, index=True)
    scheme_code = Column(String, unique=True, index=True, nullable=False)
    scheme_name = Column(String, nullable=False)
    fund_house = Column(String, nullable=False)
    category = Column(String, nullable=False)
    alert_threshold = Column(Float, default=2.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AlertModel(Base):
    """Alert database model"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    scheme_code = Column(String, index=True, nullable=False)
    scheme_name = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    drop_percentage = Column(Float, nullable=False)
    current_nav = Column(Float, nullable=False)
    previous_nav = Column(Float, nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String, nullable=False)
    acknowledged = Column(Boolean, default=False)



class SettingsModel(Base):
    """Application settings model"""
    __tablename__ = "settings"
    
    key = Column(String, primary_key=True, index=True)
    value = Column(String, nullable=False)
    description = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class NAVHistoryModel(Base):
    """NAV history database model"""
    __tablename__ = "nav_history"
    
    id = Column(Integer, primary_key=True, index=True)
    scheme_code = Column(String, index=True, nullable=False)
    date = Column(DateTime, nullable=False, index=True)
    nav = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Unique constraint on scheme_code and date
    __table_args__ = (
        {'sqlite_autoincrement': True} if "sqlite" in config.DATABASE_URL else {},
    )


def init_db():
    """Initialize database - create all tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise


def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize database on import
init_db()

