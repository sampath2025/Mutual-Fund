"""
Health check endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import sys
import platform

from ..database import get_db, engine
from ..config import config

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": config.API_TITLE,
        "version": config.API_VERSION
    }


@router.get("/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """Detailed health check with database status"""
    db_status = "unknown"
    try:
        # Try to query database
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": config.API_TITLE,
        "version": config.API_VERSION,
        "python_version": sys.version,
        "platform": platform.platform(),
        "database": {
            "status": db_status,
            "url": config.DATABASE_URL.split("@")[-1] if "@" in config.DATABASE_URL else "sqlite"
        },
        "config": {
            "debug": config.DEBUG,
            "log_level": config.LOG_LEVEL,
            "agent_interval": config.AGENT_CHECK_INTERVAL
        }
    }

