"""
AI Agent Core Engine for Mutual Fund NAV Tracking
"""
import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Fund:
    """Represents a mutual fund"""
    scheme_code: str
    scheme_name: str
    fund_house: str
    category: str
    alert_threshold: float = 2.0  # Default 2% drop threshold
    is_active: bool = True


@dataclass
class NAVData:
    """NAV data point"""
    date: datetime
    nav: float
    scheme_code: str


@dataclass
class AnalysisResult:
    """Result of NAV analysis"""
    fund: Fund
    current_nav: float
    previous_nav: float
    drop_percentage: float
    volatility: float
    trend: str  # 'uptrend', 'downtrend', 'sideways'
    anomaly_detected: bool
    risk_level: str  # 'low', 'medium', 'high'
    recommendation: str


@dataclass
class Alert:
    """Alert object"""
    fund: Fund
    timestamp: datetime
    drop_percentage: float
    current_nav: float
    previous_nav: float
    message: str
    severity: str  # 'low', 'medium', 'high', 'critical'


class NAVAnalyzer:
    """Analyzes NAV patterns and detects anomalies"""
    
    def __init__(self):
        self.volatility_window = 30  # days
        
    def analyze(self, fund: Fund, current_nav: float, historical_data: List[NAVData]) -> AnalysisResult:
        """
        Analyze NAV data and return insights
        """
        if len(historical_data) < 2:
            raise ValueError("Insufficient historical data")
        
        # Sort by date (most recent first)
        historical_data = sorted(historical_data, key=lambda x: x.date, reverse=True)
        
        current_nav_point = historical_data[0]
        previous_nav_point = historical_data[1] if len(historical_data) > 1 else historical_data[0]
        
        # Calculate drop percentage
        drop_percentage = ((previous_nav_point.nav - current_nav_point.nav) / previous_nav_point.nav) * 100
        
        # Calculate volatility (standard deviation of returns)
        navs = [d.nav for d in historical_data[:self.volatility_window]]
        returns = np.diff(navs) / navs[:-1] * 100
        volatility = np.std(returns) if len(returns) > 0 else 0
        
        # Detect trend
        trend = self._detect_trend(historical_data[:30])
        
        # Detect anomaly
        anomaly_detected = self._detect_anomaly(current_nav_point.nav, historical_data)
        
        # Assess risk level
        risk_level = self._assess_risk(drop_percentage, volatility)
        
        # Generate recommendation
        recommendation = self._generate_recommendation(drop_percentage, trend, risk_level)
        
        return AnalysisResult(
            fund=fund,
            current_nav=current_nav_point.nav,
            previous_nav=previous_nav_point.nav,
            drop_percentage=drop_percentage,
            volatility=volatility,
            trend=trend,
            anomaly_detected=anomaly_detected,
            risk_level=risk_level,
            recommendation=recommendation
        )
    
    def _detect_trend(self, data: List[NAVData]) -> str:
        """Detect trend from historical data"""
        if len(data) < 5:
            return "insufficient_data"
        
        navs = [d.nav for d in sorted(data, key=lambda x: x.date)]
        
        # Simple linear regression to detect trend
        x = np.arange(len(navs))
        coeffs = np.polyfit(x, navs, 1)
        slope = coeffs[0]
        
        if slope > 0.01:
            return "uptrend"
        elif slope < -0.01:
            return "downtrend"
        else:
            return "sideways"
    
    def _detect_anomaly(self, current_nav: float, historical_data: List[NAVData]) -> bool:
        """Detect if current NAV is an anomaly using Z-score"""
        if len(historical_data) < 10:
            return False
        
        navs = [d.nav for d in historical_data[:30]]
        mean_nav = np.mean(navs)
        std_nav = np.std(navs)
        
        if std_nav == 0:
            return False
        
        z_score = abs((current_nav - mean_nav) / std_nav)
        return z_score > 2.5  # Threshold for anomaly
    
    def _assess_risk(self, drop_percentage: float, volatility: float) -> str:
        """Assess risk level based on drop and volatility"""
        if drop_percentage > 5 or volatility > 3:
            return "high"
        elif drop_percentage > 2 or volatility > 1.5:
            return "medium"
        else:
            return "low"
    
    def _generate_recommendation(self, drop_percentage: float, trend: str, risk_level: str) -> str:
        """Generate investment recommendation"""
        if risk_level == "high" and drop_percentage > 5:
            return "Consider reviewing your investment. Significant drop detected."
        elif risk_level == "medium":
            return "Monitor closely. Moderate volatility detected."
        elif trend == "downtrend":
            return "Fund is in a downtrend. Review your strategy."
        else:
            return "Fund performance is within normal range."


class AlertManager:
    """Manages alert generation and notification"""
    
    def __init__(self):
        self.alert_history: List[Alert] = []
        self.cooldown_period = timedelta(hours=1)  # Prevent alert spam
        
    def should_trigger_alert(self, fund: Fund, analysis: AnalysisResult) -> bool:
        """Determine if alert should be triggered"""
        # Check threshold
        if abs(analysis.drop_percentage) >= fund.alert_threshold:
            # Check cooldown
            last_alert = self._get_last_alert(fund)
            if last_alert is None or (datetime.now() - last_alert.timestamp) > self.cooldown_period:
                return True
        
        # Check for anomalies
        if analysis.anomaly_detected and analysis.risk_level in ["high", "critical"]:
            return True
        
        return False
    
    def create_alert(self, fund: Fund, analysis: AnalysisResult) -> Alert:
        """Create an alert object"""
        severity = self._determine_severity(analysis)
        message = self._generate_alert_message(fund, analysis, severity)
        
        alert = Alert(
            fund=fund,
            timestamp=datetime.now(),
            drop_percentage=analysis.drop_percentage,
            current_nav=analysis.current_nav,
            previous_nav=analysis.previous_nav,
            message=message,
            severity=severity
        )
        
        self.alert_history.append(alert)
        return alert
    
    def _get_last_alert(self, fund: Fund) -> Optional[Alert]:
        """Get the last alert for a fund"""
        fund_alerts = [a for a in self.alert_history if a.fund.scheme_code == fund.scheme_code]
        return fund_alerts[-1] if fund_alerts else None
    
    def _determine_severity(self, analysis: AnalysisResult) -> str:
        """Determine alert severity"""
        if analysis.drop_percentage > 10 or analysis.risk_level == "high":
            return "critical"
        elif analysis.drop_percentage > 5:
            return "high"
        elif analysis.drop_percentage > 2:
            return "medium"
        else:
            return "low"
    
    def _generate_alert_message(self, fund: Fund, analysis: AnalysisResult, severity: str) -> str:
        """Generate human-readable alert message"""
        direction = "dropped" if analysis.drop_percentage > 0 else "increased"
        return (
            f"Alert: {fund.scheme_name} NAV {direction} by {abs(analysis.drop_percentage):.2f}%. "
            f"Current NAV: ₹{analysis.current_nav:.2f}. "
            f"Risk Level: {analysis.risk_level.upper()}. "
            f"{analysis.recommendation}"
        )


class AIAgent:
    """Main AI Agent for NAV tracking"""
    
    def __init__(self, data_collector, notifier):
        self.data_collector = data_collector
        self.notifier = notifier
        self.analyzer = NAVAnalyzer()
        self.alert_manager = AlertManager()
        self.tracked_funds: List[Fund] = []
        self.is_running = False
        
    def add_fund(self, fund: Fund):
        """Add a fund to tracking list"""
        self.tracked_funds.append(fund)
        logger.info(f"Added fund to tracking: {fund.scheme_name}")
    
    def remove_fund(self, scheme_code: str):
        """Remove a fund from tracking"""
        self.tracked_funds = [f for f in self.tracked_funds if f.scheme_code != scheme_code]
        logger.info(f"Removed fund from tracking: {scheme_code}")
    
    async def run_cycle(self):
        """Run one cycle of monitoring"""
        if not self.tracked_funds:
            logger.warning("No funds to track")
            return
        
        for fund in self.tracked_funds:
            if not fund.is_active:
                continue
            
            try:
                # Fetch latest NAV data
                current_nav_data = await self.data_collector.get_latest_nav(fund.scheme_code)
                historical_data = await self.data_collector.get_historical_nav(
                    fund.scheme_code, days=30
                )
                
                if not current_nav_data or not historical_data:
                    logger.warning(f"Could not fetch data for {fund.scheme_name}")
                    continue
                
                # Analyze NAV patterns
                analysis = self.analyzer.analyze(fund, current_nav_data.nav, historical_data)
                
                # Check if alert should be triggered
                if self.alert_manager.should_trigger_alert(fund, analysis):
                    alert = self.alert_manager.create_alert(fund, analysis)
                    await self.notifier.send_notification(alert)
                    logger.info(f"Alert triggered: {alert.message}")
                
                # Log analysis
                logger.info(
                    f"{fund.scheme_name}: NAV={analysis.current_nav:.2f}, "
                    f"Drop={analysis.drop_percentage:.2f}%, "
                    f"Trend={analysis.trend}, Risk={analysis.risk_level}"
                )
                
            except Exception as e:
                logger.error(f"Error processing fund {fund.scheme_name}: {str(e)}")
    
    async def start(self, interval_seconds: int = 300):
        """Start the agent with specified interval (default 5 minutes)"""
        self.is_running = True
        logger.info(f"AI Agent started with {interval_seconds}s interval")
        
        while self.is_running:
            await self.run_cycle()
            await asyncio.sleep(interval_seconds)
    
    def stop(self):
        """Stop the agent"""
        self.is_running = False
        logger.info("AI Agent stopped")

