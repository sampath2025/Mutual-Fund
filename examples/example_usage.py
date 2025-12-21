"""
Example usage of the AI Agent
"""
import asyncio
from src.agent.core import AIAgent, Fund
from src.agent.data_collector import DataCollector
from src.agent.notifier import Notifier

async def main():
    # Initialize components
    data_collector = DataCollector()
    notifier = Notifier()
    agent = AIAgent(data_collector, notifier)
    
    # Add some funds to track
    funds = [
        Fund(
            scheme_code="125497",
            scheme_name="HDFC Equity Fund",
            fund_house="HDFC Mutual Fund",
            category="Equity",
            alert_threshold=2.0
        ),
        Fund(
            scheme_code="120465",
            scheme_name="SBI Bluechip Fund",
            fund_house="SBI Mutual Fund",
            category="Equity",
            alert_threshold=2.5
        ),
    ]
    
    for fund in funds:
        agent.add_fund(fund)
        print(f"Added {fund.scheme_name} to tracking")
    
    # Run one cycle manually
    print("\nRunning monitoring cycle...")
    await agent.run_cycle()
    
    # Or start continuous monitoring
    # await agent.start(interval_seconds=300)  # Check every 5 minutes
    
    # Cleanup
    await data_collector.close()

if __name__ == "__main__":
    asyncio.run(main())

