"""
Alert service for database operations
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime
import logging

from ..database import AlertModel, get_db
from ..agent.core import Alert

logger = logging.getLogger(__name__)


class AlertService:
    """Service for alert-related operations"""
    
    @staticmethod
    def create_alert(db: Session, alert: Alert) -> AlertModel:
        """Save alert to database"""
        db_alert = AlertModel(
            scheme_code=alert.fund.scheme_code,
            scheme_name=alert.fund.scheme_name,
            timestamp=alert.timestamp,
            drop_percentage=alert.drop_percentage,
            current_nav=alert.current_nav,
            previous_nav=alert.previous_nav,
            message=alert.message,
            severity=alert.severity,
            acknowledged=False
        )
        db.add(db_alert)
        db.commit()
        db.refresh(db_alert)
        logger.info(f"Saved alert to database: {alert.fund.scheme_name}")
        return db_alert
    
    @staticmethod
    def get_alerts(
        db: Session,
        scheme_code: Optional[str] = None,
        limit: int = 50,
        acknowledged: Optional[bool] = None
    ) -> List[AlertModel]:
        """Get alerts with optional filters"""
        query = db.query(AlertModel)
        
        if scheme_code:
            query = query.filter(AlertModel.scheme_code == scheme_code)
        
        if acknowledged is not None:
            query = query.filter(AlertModel.acknowledged == acknowledged)
        
        return query.order_by(desc(AlertModel.timestamp)).limit(limit).all()
    
    @staticmethod
    def acknowledge_alert(db: Session, alert_id: int) -> Optional[AlertModel]:
        """Mark alert as acknowledged"""
        alert = db.query(AlertModel).filter(AlertModel.id == alert_id).first()
        if alert:
            alert.acknowledged = True
            db.commit()
            db.refresh(alert)
        return alert
    
    @staticmethod
    def get_unacknowledged_count(db: Session, scheme_code: Optional[str] = None) -> int:
        """Get count of unacknowledged alerts"""
        query = db.query(AlertModel).filter(AlertModel.acknowledged == False)
        if scheme_code:
            query = query.filter(AlertModel.scheme_code == scheme_code)
        return query.count()

