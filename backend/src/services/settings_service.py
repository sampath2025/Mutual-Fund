"""
Settings service for application configuration
"""
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
import json
import logging

from ..database import SettingsModel

logger = logging.getLogger(__name__)

class SettingsService:
    """Service for settings operations"""
    
    @staticmethod
    def get_setting(db: Session, key: str, default: Any = None) -> Any:
        """Get setting value by key"""
        setting = db.query(SettingsModel).filter(SettingsModel.key == key).first()
        if setting:
            try:
                return json.loads(setting.value)
            except json.JSONDecodeError:
                return setting.value
        return default
    
    @staticmethod
    def set_setting(db: Session, key: str, value: Any, description: str = None) -> SettingsModel:
        """Set setting value"""
        setting = db.query(SettingsModel).filter(SettingsModel.key == key).first()
        
        json_value = json.dumps(value)
        
        if setting:
            setting.value = json_value
            if description:
                setting.description = description
        else:
            setting = SettingsModel(
                key=key,
                value=json_value,
                description=description
            )
            db.add(setting)
        
        db.commit()
        db.refresh(setting)
        return setting
    
    @staticmethod
    def get_all_settings(db: Session) -> Dict[str, Any]:
        """Get all settings as a dictionary"""
        settings = db.query(SettingsModel).all()
        result = {}
        for setting in settings:
            try:
                result[setting.key] = json.loads(setting.value)
            except json.JSONDecodeError:
                result[setting.key] = setting.value
        return result
