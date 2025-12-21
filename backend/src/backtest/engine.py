"""
Backtesting Engine for NAV Drop Alert Strategy
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class BacktestResult:
    """Results from backtesting"""
    total_alerts: int
    true_positives: int
    false_positives: int
    true_negatives: int
    false_negatives: int
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    avg_drop_after_alert: float
    max_drop_after_alert: float
    avg_recovery_time: Optional[float]  # days
    total_return_if_followed: float
    alerts_by_severity: Dict[str, int]
    performance_metrics: Dict[str, float]


class BacktestEngine:
    """Backtesting engine for alert strategies"""
    
    def __init__(self):
        self.lookahead_days = 7  # Days to check after alert
        self.recovery_threshold = 0.5  # 0.5% recovery to consider "recovered"
        
    def backtest(
        self,
        historical_data: pd.DataFrame,
        threshold: float,
        scheme_name: str = "Unknown"
    ) -> BacktestResult:
        """
        Backtest the alert strategy on historical data
        
        Args:
            historical_data: DataFrame with columns ['date', 'nav']
            threshold: Drop percentage threshold for alerts
            scheme_name: Name of the fund
        
        Returns:
            BacktestResult object with metrics
        """
        if historical_data.empty or len(historical_data) < 2:
            raise ValueError("Insufficient historical data for backtesting")
        
        # Sort by date
        historical_data = historical_data.sort_values('date').reset_index(drop=True)
        
        alerts = []
        true_positives = 0
        false_positives = 0
        true_negatives = 0
        false_negatives = 0
        
        drops_after_alert = []
        recovery_times = []
        
        # Iterate through historical data
        for i in range(1, len(historical_data) - self.lookahead_days):
            current_nav = historical_data.iloc[i]['nav']
            previous_nav = historical_data.iloc[i-1]['nav']
            
            if previous_nav == 0:
                continue
            
            drop_percentage = ((previous_nav - current_nav) / previous_nav) * 100
            
            # Check if alert would have been triggered
            if drop_percentage >= threshold:
                alert_date = historical_data.iloc[i]['date']
                
                # Check future performance
                future_data = historical_data.iloc[i+1:i+1+self.lookahead_days]
                
                if len(future_data) > 0:
                    future_navs = future_data['nav'].values
                    min_future_nav = min(future_navs)
                    max_drop_from_alert = ((current_nav - min_future_nav) / current_nav) * 100
                    
                    drops_after_alert.append(max_drop_from_alert)
                    
                    # Check if NAV continued to drop (true positive)
                    if min_future_nav < current_nav:
                        true_positives += 1
                        # Calculate recovery time
                        recovery_time = self._calculate_recovery_time(
                            current_nav, future_data
                        )
                        if recovery_time:
                            recovery_times.append(recovery_time)
                    else:
                        false_positives += 1
                    
                    alerts.append({
                        'date': alert_date,
                        'nav': current_nav,
                        'drop_percentage': drop_percentage,
                        'max_drop_after': max_drop_from_alert,
                        'was_accurate': min_future_nav < current_nav
                    })
            else:
                # No alert triggered - check if we should have (false negative)
                future_data = historical_data.iloc[i+1:i+1+self.lookahead_days]
                if len(future_data) > 0:
                    min_future_nav = min(future_data['nav'].values)
                    if min_future_nav < current_nav * 0.95:  # 5% further drop
                        false_negatives += 1
                    else:
                        true_negatives += 1
        
        # Calculate metrics
        total_alerts = len(alerts)
        total_positives = true_positives + false_positives
        total_negatives = true_negatives + false_negatives
        
        accuracy = (true_positives + true_negatives) / (total_positives + total_negatives) if (total_positives + total_negatives) > 0 else 0
        precision = true_positives / total_positives if total_positives > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        # Calculate returns if strategy was followed
        total_return = self._calculate_strategy_return(historical_data, alerts)
        
        # Categorize alerts by severity
        alerts_by_severity = {
            'critical': sum(1 for a in alerts if a['drop_percentage'] > 10),
            'high': sum(1 for a in alerts if 5 < a['drop_percentage'] <= 10),
            'medium': sum(1 for a in alerts if 2 < a['drop_percentage'] <= 5),
            'low': sum(1 for a in alerts if a['drop_percentage'] <= 2)
        }
        
        return BacktestResult(
            total_alerts=total_alerts,
            true_positives=true_positives,
            false_positives=false_positives,
            true_negatives=true_negatives,
            false_negatives=false_negatives,
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1_score,
            avg_drop_after_alert=np.mean(drops_after_alert) if drops_after_alert else 0,
            max_drop_after_alert=max(drops_after_alert) if drops_after_alert else 0,
            avg_recovery_time=np.mean(recovery_times) if recovery_times else None,
            total_return_if_followed=total_return,
            alerts_by_severity=alerts_by_severity,
            performance_metrics={
                'sharpe_ratio': self._calculate_sharpe_ratio(historical_data),
                'max_drawdown': self._calculate_max_drawdown(historical_data),
                'volatility': self._calculate_volatility(historical_data)
            }
        )
    
    def _calculate_recovery_time(self, alert_nav: float, future_data: pd.DataFrame) -> Optional[float]:
        """Calculate days to recover to alert NAV level"""
        for idx, row in future_data.iterrows():
            if row['nav'] >= alert_nav * (1 + self.recovery_threshold / 100):
                return (row['date'] - future_data.iloc[0]['date']).days
        return None
    
    def _calculate_strategy_return(self, historical_data: pd.DataFrame, alerts: List[dict]) -> float:
        """Calculate total return if strategy was followed (sell on alert, buy back after recovery)"""
        # Simplified: Assume selling on alert and buying back after recovery
        # This is a simplified model - real strategy would be more complex
        if not alerts:
            return 0
        
        total_return = 0
        position = 1.0  # Start with 1 unit
        
        for alert in alerts:
            # Sell on alert
            sell_price = alert['nav']
            proceeds = position * sell_price
            
            # Find recovery point (simplified)
            alert_idx = historical_data[historical_data['date'] == alert['date']].index[0]
            recovery_data = historical_data.iloc[alert_idx+1:alert_idx+30]
            
            if len(recovery_data) > 0:
                # Buy back at 1% above alert price or after 7 days
                recovery_price = recovery_data.iloc[min(6, len(recovery_data)-1)]['nav']
                position = proceeds / recovery_price
                total_return = (position - 1.0) * 100
        
        return total_return
    
    def _calculate_sharpe_ratio(self, data: pd.DataFrame, risk_free_rate: float = 0.05) -> float:
        """Calculate Sharpe ratio"""
        if len(data) < 2:
            return 0
        
        returns = data['nav'].pct_change().dropna()
        if len(returns) == 0 or returns.std() == 0:
            return 0
        
        excess_returns = returns.mean() * 252 - risk_free_rate  # Annualized
        return excess_returns / (returns.std() * np.sqrt(252))
    
    def _calculate_max_drawdown(self, data: pd.DataFrame) -> float:
        """Calculate maximum drawdown"""
        if data.empty:
            return 0
        
        peak = data['nav'].expanding().max()
        drawdown = (data['nav'] - peak) / peak * 100
        return abs(drawdown.min())
    
    def _calculate_volatility(self, data: pd.DataFrame) -> float:
        """Calculate annualized volatility"""
        if len(data) < 2:
            return 0
        
        returns = data['nav'].pct_change().dropna()
        if len(returns) == 0:
            return 0
        
        return returns.std() * np.sqrt(252) * 100  # Annualized percentage
    
    def optimize_threshold(
        self,
        historical_data: pd.DataFrame,
        threshold_range: tuple = (0.5, 10.0),
        step: float = 0.5
    ) -> Dict[str, any]:
        """Find optimal threshold by testing multiple values"""
        best_threshold = threshold_range[0]
        best_f1_score = 0
        results = []
        
        for threshold in np.arange(threshold_range[0], threshold_range[1], step):
            result = self.backtest(historical_data, threshold)
            results.append({
                'threshold': threshold,
                'f1_score': result.f1_score,
                'precision': result.precision,
                'recall': result.recall,
                'total_alerts': result.total_alerts
            })
            
            if result.f1_score > best_f1_score:
                best_f1_score = result.f1_score
                best_threshold = threshold
        
        return {
            'optimal_threshold': best_threshold,
            'best_f1_score': best_f1_score,
            'all_results': results
        }

