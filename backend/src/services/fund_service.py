"""
Fund service for database operations
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime
import logging

from ..database import FundModel, NAVHistoryModel, get_db
from ..agent.core import Fund

logger = logging.getLogger(__name__)


class FundService:
    """Service for fund-related operations"""
    
    @staticmethod
    def create_fund(db: Session, fund: Fund) -> FundModel:
        """Create a new fund in database"""
        db_fund = FundModel(
            scheme_code=fund.scheme_code,
            scheme_name=fund.scheme_name,
            fund_house=fund.fund_house,
            category=fund.category,
            alert_threshold=fund.alert_threshold,
            is_active=fund.is_active
        )
        db.add(db_fund)
        db.commit()
        db.refresh(db_fund)
        logger.info(f"Created fund in database: {fund.scheme_name}")
        return db_fund
    
    @staticmethod
    def get_fund(db: Session, scheme_code: str) -> Optional[FundModel]:
        """Get fund by scheme code"""
        return db.query(FundModel).filter(FundModel.scheme_code == scheme_code).first()
    
    @staticmethod
    def get_all_funds(db: Session, active_only: bool = False) -> List[FundModel]:
        """Get all funds"""
        query = db.query(FundModel)
        if active_only:
            query = query.filter(FundModel.is_active == True)
        return query.all()
    
    @staticmethod
    def update_fund(db: Session, scheme_code: str, **kwargs) -> Optional[FundModel]:
        """Update fund"""
        fund = db.query(FundModel).filter(FundModel.scheme_code == scheme_code).first()
        if fund:
            for key, value in kwargs.items():
                if hasattr(fund, key):
                    setattr(fund, key, value)
            fund.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(fund)
        return fund
    
    @staticmethod
    def delete_fund(db: Session, scheme_code: str) -> bool:
        """Delete fund"""
        fund = db.query(FundModel).filter(FundModel.scheme_code == scheme_code).first()
        if fund:
            db.delete(fund)
            db.commit()
            logger.info(f"Deleted fund: {scheme_code}")
            return True
        return False
    
    @staticmethod
    def save_nav_history(db: Session, scheme_code: str, date: datetime, nav: float):
        """Save NAV history"""
        # Check if record exists
        existing = db.query(NAVHistoryModel).filter(
            NAVHistoryModel.scheme_code == scheme_code,
            NAVHistoryModel.date == date
        ).first()
        
        if not existing:
            nav_record = NAVHistoryModel(
                scheme_code=scheme_code,
                date=date,
                nav=nav
            )
            db.add(nav_record)
            db.commit()
    
    @staticmethod
    def get_nav_history(db: Session, scheme_code: str, days: int = 30) -> List[NAVHistoryModel]:
        """Get NAV history for a fund"""
        cutoff_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        cutoff_date = cutoff_date.replace(day=cutoff_date.day - days)
        
        return db.query(NAVHistoryModel).filter(
            NAVHistoryModel.scheme_code == scheme_code,
            NAVHistoryModel.date >= cutoff_date
        ).order_by(desc(NAVHistoryModel.date)).all()
    
    @staticmethod
    def convert_to_fund(db_fund: FundModel) -> Fund:
        """Convert database model to Fund object"""
        return Fund(
            scheme_code=db_fund.scheme_code,
            scheme_name=db_fund.scheme_name,
            fund_house=db_fund.fund_house,
            category=db_fund.category,
            alert_threshold=db_fund.alert_threshold,
            is_active=db_fund.is_active
        )

