"""
Script to find scheme code for a mutual fund by name
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent.data_collector import DataCollector, AMFIDataCollector


async def find_fund(fund_name: str):
    """Find scheme code for a fund by name"""
    print(f"\nSearching for: {fund_name}")
    print("=" * 60)
    
    # Use data collector to search
    collector = DataCollector()
    results = await collector.search_funds(fund_name)
    
    if results:
        print(f"\nFound {len(results)} matching funds:\n")
        for i, fund in enumerate(results, 1):
            print(f"{i}. {fund.get('scheme_name', 'N/A')}")
            print(f"   Scheme Code: {fund.get('scheme_code', 'N/A')}")
            print(f"   Fund House: {fund.get('fund_house', 'N/A')}")
            if fund.get('nav'):
                print(f"   Latest NAV: Rs. {fund.get('nav', 0):.2f}")
            print()
        
        # Test the first result
        if results:
            first_code = results[0].get('scheme_code')
            print(f"\nTesting NAV fetch for scheme code: {first_code}")
            nav_data = await collector.get_latest_nav(first_code)
            if nav_data:
                print(f"Success! NAV: Rs. {nav_data.nav:.2f} (Date: {nav_data.date.strftime('%d-%b-%Y')})")
            else:
                print("Failed to fetch NAV")
    else:
        print(f"\nNo funds found matching '{fund_name}'")
        print("\nSuggestions:")
        print("   - Try a partial name (e.g., 'Nippon' instead of full name)")
        print("   - Check spelling")
        print("   - Visit https://www.mfapi.in/ to search manually")
    
    await collector.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        fund_name = input("Enter fund name to search: ")
    else:
        fund_name = sys.argv[1]
    
    asyncio.run(find_fund(fund_name))

