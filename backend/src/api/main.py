"""
FastAPI Backend for Mutual Fund NAV Tracking Web App
"""
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import asyncio
import logging

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
sys.path.insert(0, str(project_root))

from src.agent.core import AIAgent, Fund, Alert
from src.agent.data_collector import DataCollector, AMFIDataCollector
from src.agent.notifier import Notifier
from src.backtest.engine import BacktestEngine
from src.config import config
from src.database import get_db, init_db, Session
from src.services.fund_service import FundService
from src.services.alert_service import AlertService
from src.api.health import router as health_router
import pandas as pd

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title=config.API_TITLE, version=config.API_VERSION)

# Include health check router
app.include_router(health_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
data_collector = DataCollector()
notifier = Notifier(config.get_email_config(), AlertService)
agent = AIAgent(data_collector, notifier)
backtest_engine = BacktestEngine()

# WebSocket connections
active_connections: List[WebSocket] = []


# Pydantic models
class FundCreate(BaseModel):
    scheme_code: str
    scheme_name: str
    fund_house: str
    category: str
    alert_threshold: float = 2.0


class FundResponse(BaseModel):
    scheme_code: str
    scheme_name: str
    fund_house: str
    category: str
    alert_threshold: float
    is_active: bool


class AlertResponse(BaseModel):
    fund: dict
    timestamp: datetime
    drop_percentage: float
    current_nav: float
    previous_nav: float
    message: str
    severity: str


class BacktestRequest(BaseModel):
    scheme_code: str
    threshold: float
    start_date: Optional[str] = None
    end_date: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("Starting up API server...")
    logger.info(f"Database URL: {config.DATABASE_URL}")
    logger.info(f"Agent check interval: {config.AGENT_CHECK_INTERVAL} seconds")
    # Database is initialized on import, but we can verify here
    init_db()


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await data_collector.close()
    agent.stop()
    logger.info("Shutting down API server...")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Mutual Fund NAV Tracker API",
        "version": "1.0.0",
        "endpoints": {
            "funds": "/api/funds",
            "alerts": "/api/alerts",
            "backtest": "/api/backtest",
            "search": "/api/search",
            "nav": "/api/nav/{scheme_code}"
        }
    }


@app.post("/api/funds", response_model=FundResponse)
async def add_fund(fund_data: FundCreate, db: Session = Depends(get_db)):
    """Add a fund to tracking"""
    try:
        # Check if fund already exists
        existing = FundService.get_fund(db, fund_data.scheme_code)
        if existing:
            raise HTTPException(status_code=400, detail="Fund already exists")
        
        fund = Fund(
            scheme_code=fund_data.scheme_code,
            scheme_name=fund_data.scheme_name,
            fund_house=fund_data.fund_house,
            category=fund_data.category,
            alert_threshold=fund_data.alert_threshold
        )
        
        # Save to database
        db_fund = FundService.create_fund(db, fund)
        
        # Add to agent
        agent.add_fund(fund)
        
        return FundResponse(
            scheme_code=db_fund.scheme_code,
            scheme_name=db_fund.scheme_name,
            fund_house=db_fund.fund_house,
            category=db_fund.category,
            alert_threshold=db_fund.alert_threshold,
            is_active=db_fund.is_active
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding fund: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/funds", response_model=List[FundResponse])
async def get_funds(db: Session = Depends(get_db)):
    """Get all tracked funds"""
    db_funds = FundService.get_all_funds(db)
    return [
        FundResponse(
            scheme_code=f.scheme_code,
            scheme_name=f.scheme_name,
            fund_house=f.fund_house,
            category=f.category,
            alert_threshold=f.alert_threshold,
            is_active=f.is_active
        )
        for f in db_funds
    ]


@app.delete("/api/funds/{scheme_code}")
async def remove_fund(scheme_code: str, db: Session = Depends(get_db)):
    """Remove a fund from tracking"""
    # Remove from database
    deleted = FundService.delete_fund(db, scheme_code)
    if not deleted:
        raise HTTPException(status_code=404, detail="Fund not found")
    
    # Remove from agent
    agent.remove_fund(scheme_code)
    return {"message": f"Fund {scheme_code} removed from tracking"}


@app.get("/api/nav/{scheme_code}")
async def get_nav(scheme_code: str, days: int = 30):
    """Get NAV data for a scheme"""
    try:
        latest_nav = await data_collector.get_latest_nav(scheme_code)
        historical_nav = await data_collector.get_historical_nav(scheme_code, days=days)
        
        return {
            "scheme_code": scheme_code,
            "latest_nav": {
                "date": latest_nav.date.isoformat() if latest_nav else None,
                "nav": latest_nav.nav if latest_nav else None
            },
            "historical_nav": [
                {
                    "date": nav.date.isoformat(),
                    "nav": nav.nav
                }
                for nav in historical_nav
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/alerts", response_model=List[AlertResponse])
async def get_alerts(
    limit: int = 50,
    scheme_code: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get recent alerts"""
    db_alerts = AlertService.get_alerts(db, scheme_code=scheme_code, limit=limit)
    return [
        AlertResponse(
            fund={
                "scheme_code": alert.scheme_code,
                "scheme_name": alert.scheme_name,
                "category": ""  # Could be added to alert model
            },
            timestamp=alert.timestamp,
            drop_percentage=alert.drop_percentage,
            current_nav=alert.current_nav,
            previous_nav=alert.previous_nav,
            message=alert.message,
            severity=alert.severity
        )
        for alert in db_alerts
    ]


@app.post("/api/backtest")
async def run_backtest(request: BacktestRequest):
    """Run backtest on historical data"""
    try:
        # Fetch historical data
        historical_nav = await data_collector.get_historical_nav(
            request.scheme_code, days=365
        )
        
        if len(historical_nav) < 30:
            raise HTTPException(
                status_code=400,
                detail="Insufficient historical data for backtesting"
            )
        
        # Convert to DataFrame
        df = pd.DataFrame([
            {"date": nav.date, "nav": nav.nav}
            for nav in historical_nav
        ])
        
        # Run backtest
        result = backtest_engine.backtest(df, request.threshold)
        
        return {
            "scheme_code": request.scheme_code,
            "threshold": request.threshold,
            "results": {
                "total_alerts": result.total_alerts,
                "true_positives": result.true_positives,
                "false_positives": result.false_positives,
                "accuracy": round(result.accuracy * 100, 2),
                "precision": round(result.precision * 100, 2),
                "recall": round(result.recall * 100, 2),
                "f1_score": round(result.f1_score * 100, 2),
                "avg_drop_after_alert": round(result.avg_drop_after_alert, 2),
                "max_drop_after_alert": round(result.max_drop_after_alert, 2),
                "avg_recovery_time": round(result.avg_recovery_time, 2) if result.avg_recovery_time else None,
                "alerts_by_severity": result.alerts_by_severity,
                "performance_metrics": {
                    "sharpe_ratio": round(result.performance_metrics['sharpe_ratio'], 2),
                    "max_drawdown": round(result.performance_metrics['max_drawdown'], 2),
                    "volatility": round(result.performance_metrics['volatility'], 2)
                }
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/backtest/optimize")
async def optimize_threshold(request: BacktestRequest):
    """Find optimal threshold for a fund"""
    try:
        historical_nav = await data_collector.get_historical_nav(
            request.scheme_code, days=365
        )
        
        if len(historical_nav) < 30:
            raise HTTPException(
                status_code=400,
                detail="Insufficient historical data"
            )
        
        df = pd.DataFrame([
            {"date": nav.date, "nav": nav.nav}
            for nav in historical_nav
        ])
        
        optimization = backtest_engine.optimize_threshold(df)
        
        return {
            "scheme_code": request.scheme_code,
            "optimal_threshold": round(optimization['optimal_threshold'], 2),
            "best_f1_score": round(optimization['best_f1_score'] * 100, 2),
            "all_results": [
                {
                    "threshold": round(r['threshold'], 2),
                    "f1_score": round(r['f1_score'] * 100, 2),
                    "precision": round(r['precision'] * 100, 2),
                    "recall": round(r['recall'] * 100, 2),
                    "total_alerts": r['total_alerts']
                }
                for r in optimization['all_results']
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/search")
async def search_funds(query: str):
    """Search for mutual funds by name"""
    try:
        if not query or len(query) < 2:
            raise HTTPException(status_code=400, detail="Query must be at least 2 characters")
        
        results = await data_collector.search_funds(query)
        return {
            "query": query,
            "count": len(results),
            "results": results
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching funds: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/nav/test/{scheme_code}")
async def test_nav_fetch(scheme_code: str):
    """Test NAV fetching for a specific scheme code"""
    try:
        # Try MFAPI first
        nav_data = await data_collector.get_latest_nav(scheme_code)
        
        if nav_data:
            return {
                "success": True,
                "scheme_code": scheme_code,
                "source": "MFAPI",
                "nav": nav_data.nav,
                "date": nav_data.date.isoformat()
            }
        else:
            # Try AMFI
            amfi_collector = AMFIDataCollector()
            all_funds = await amfi_collector.fetch_amfi_nav_data()
            
            for fund in all_funds:
                if fund.get('scheme_code') == scheme_code:
                    return {
                        "success": True,
                        "scheme_code": scheme_code,
                        "source": "AMFI",
                        "scheme_name": fund.get('scheme_name', ''),
                        "nav": fund.get('nav', 0),
                        "date": fund.get('date', '')
                    }
            
            return {
                "success": False,
                "scheme_code": scheme_code,
                "error": "Scheme code not found in any data source",
                "suggestion": "Try searching for the fund name using /api/search endpoint"
            }
    except Exception as e:
        logger.error(f"Error testing NAV fetch: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Send periodic updates
            if agent.tracked_funds:
                for fund in agent.tracked_funds:
                    nav_data = await data_collector.get_latest_nav(fund.scheme_code)
                    if nav_data:
                        await websocket.send_json({
                            "type": "nav_update",
                            "scheme_code": fund.scheme_code,
                            "scheme_name": fund.scheme_name,
                            "nav": nav_data.nav,
                            "date": nav_data.date.isoformat()
                        })
            
            await asyncio.sleep(60)  # Update every minute
    except WebSocketDisconnect:
        active_connections.remove(websocket)


async def broadcast_alert(alert: Alert):
    """Broadcast alert to all WebSocket connections"""
    for connection in active_connections:
        try:
            await connection.send_json({
                "type": "alert",
                "scheme_code": alert.fund.scheme_code,
                "scheme_name": alert.fund.scheme_name,
                "drop_percentage": alert.drop_percentage,
                "current_nav": alert.current_nav,
                "message": alert.message,
                "severity": alert.severity,
                "timestamp": alert.timestamp.isoformat()
            })
        except Exception as e:
            logger.error(f"Error broadcasting alert: {str(e)}")


# Start agent in background
@app.on_event("startup")
async def start_agent():
    """Start the AI agent"""
    # Load funds from database
    db = next(get_db())
    try:
        db_funds = FundService.get_all_funds(db, active_only=True)
        for db_fund in db_funds:
            fund = FundService.convert_to_fund(db_fund)
            agent.add_fund(fund)
        logger.info(f"Loaded {len(db_funds)} funds from database")
    finally:
        db.close()
    
    # Start agent monitoring
    asyncio.create_task(agent.start(interval_seconds=config.AGENT_CHECK_INTERVAL))
    logger.info("AI Agent started")

