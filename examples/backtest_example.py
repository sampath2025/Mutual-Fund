"""
Example backtesting usage
"""
import asyncio
import pandas as pd
from src.agent.data_collector import DataCollector
from src.backtest.engine import BacktestEngine

async def main():
    # Initialize
    data_collector = DataCollector()
    backtest_engine = BacktestEngine()
    
    # Fetch historical data
    scheme_code = "125497"  # HDFC Equity Fund
    print(f"Fetching historical data for scheme {scheme_code}...")
    
    historical_nav = await data_collector.get_historical_nav(scheme_code, days=365)
    
    if len(historical_nav) < 30:
        print("Insufficient data for backtesting")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame([
        {"date": nav.date, "nav": nav.nav}
        for nav in historical_nav
    ])
    
    print(f"Loaded {len(df)} days of data")
    
    # Run backtest with 2% threshold
    print("\nRunning backtest with 2% threshold...")
    result = backtest_engine.backtest(df, threshold=2.0)
    
    print(f"\nBacktest Results:")
    print(f"  Total Alerts: {result.total_alerts}")
    print(f"  True Positives: {result.true_positives}")
    print(f"  False Positives: {result.false_positives}")
    print(f"  Accuracy: {result.accuracy * 100:.2f}%")
    print(f"  Precision: {result.precision * 100:.2f}%")
    print(f"  Recall: {result.recall * 100:.2f}%")
    print(f"  F1 Score: {result.f1_score * 100:.2f}%")
    print(f"  Avg Drop After Alert: {result.avg_drop_after_alert:.2f}%")
    
    # Optimize threshold
    print("\nFinding optimal threshold...")
    optimization = backtest_engine.optimize_threshold(df, threshold_range=(0.5, 5.0), step=0.5)
    
    print(f"\nOptimization Results:")
    print(f"  Optimal Threshold: {optimization['optimal_threshold']:.2f}%")
    print(f"  Best F1 Score: {optimization['best_f1_score'] * 100:.2f}%")
    
    await data_collector.close()

if __name__ == "__main__":
    asyncio.run(main())

