"""
Data Collector for fetching NAV data from various APIs
"""
import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Optional
from .core import NAVData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataCollector:
    """Fetches NAV data from multiple sources"""
    
    def __init__(self):
        self.mfapi_base_url = "https://api.mfapi.in/mf"
        self.amfi_base_url = "https://portal.amfiindia.com"
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def _get_session(self):
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def close(self):
        """Close the session"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def get_latest_nav(self, scheme_code: str) -> Optional[NAVData]:
        """Get the latest NAV for a scheme"""
        try:
            session = await self._get_session()
            url = f"{self.mfapi_base_url}/{scheme_code}"
            
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('data') and len(data['data']) > 0:
                        latest = data['data'][0]
                        nav_date = datetime.strptime(latest['date'], '%d-%b-%Y')
                        return NAVData(
                            date=nav_date,
                            nav=float(latest['nav']),
                            scheme_code=scheme_code
                        )
                    else:
                        logger.warning(f"No NAV data found for scheme {scheme_code}")
                elif response.status == 404:
                    logger.warning(f"Scheme code {scheme_code} not found in MFAPI")
                else:
                    logger.warning(f"HTTP {response.status} error for scheme {scheme_code}")
        except Exception as e:
            logger.error(f"Error fetching latest NAV for {scheme_code}: {str(e)}")
            # Try alternative method
            return await self._get_latest_nav_alternative(scheme_code)
        
        return None
    
    async def _get_latest_nav_alternative(self, scheme_code: str) -> Optional[NAVData]:
        """Alternative method to fetch NAV from AMFI (fallback)"""
        try:
            amfi_collector = AMFIDataCollector()
            all_funds = await amfi_collector.fetch_amfi_nav_data()
            
            # Find the fund by scheme code
            for fund in all_funds:
                if fund.get('scheme_code') == scheme_code:
                    # Parse date
                    date_str = fund.get('date', '')
                    try:
                        # AMFI date format can vary, try common formats
                        nav_date = datetime.strptime(date_str, '%d-%b-%Y')
                    except:
                        try:
                            nav_date = datetime.strptime(date_str, '%d-%m-%Y')
                        except:
                            nav_date = datetime.now()
                    
                    return NAVData(
                        date=nav_date,
                        nav=float(fund.get('nav', 0)),
                        scheme_code=scheme_code
                    )
            
            logger.warning(f"Scheme code {scheme_code} not found in AMFI data")
        except Exception as e:
            logger.error(f"Error in alternative NAV fetch: {str(e)}")
        
        return None
    
    async def get_historical_nav(self, scheme_code: str, days: int = 30) -> List[NAVData]:
        """Get historical NAV data"""
        try:
            session = await self._get_session()
            url = f"{self.mfapi_base_url}/{scheme_code}"
            
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    nav_data_list = []
                    
                    for item in data.get('data', [])[:days]:
                        try:
                            nav_date = datetime.strptime(item['date'], '%d-%b-%Y')
                            nav_data_list.append(NAVData(
                                date=nav_date,
                                nav=float(item['nav']),
                                scheme_code=scheme_code
                            ))
                        except (ValueError, KeyError) as e:
                            logger.warning(f"Error parsing NAV data: {str(e)}")
                            continue
                    
                    return sorted(nav_data_list, key=lambda x: x.date, reverse=True)
        except Exception as e:
            logger.error(f"Error fetching historical NAV for {scheme_code}: {str(e)}")
        
        return []
    
    async def search_funds(self, query: str) -> List[dict]:
        """Search for mutual funds by name using AMFI data"""
        try:
            # Use AMFI data collector to search
            amfi_collector = AMFIDataCollector()
            all_funds = await amfi_collector.fetch_amfi_nav_data()
            
            # Filter by query (case-insensitive)
            query_lower = query.lower()
            results = []
            seen_codes = set()
            
            for fund in all_funds:
                scheme_name = fund.get('scheme_name', '').lower()
                scheme_code = fund.get('scheme_code', '')
                
                # Avoid duplicates
                if scheme_code in seen_codes:
                    continue
                
                # Check if query matches fund name
                if query_lower in scheme_name or scheme_name in query_lower:
                    # Try to get fund metadata from MFAPI
                    try:
                        session = await self._get_session()
                        test_url = f"{self.mfapi_base_url}/{scheme_code}"
                        async with session.get(test_url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                            if response.status == 200:
                                data = await response.json()
                                meta = data.get('meta', {})
                                results.append({
                                    'scheme_code': scheme_code,
                                    'scheme_name': fund.get('scheme_name', ''),
                                    'fund_house': meta.get('fund_house', ''),
                                    'scheme_type': meta.get('scheme_type', ''),
                                    'nav': fund.get('nav', 0),
                                    'date': fund.get('date', '')
                                })
                                seen_codes.add(scheme_code)
                    except:
                        # If MFAPI fails, still include from AMFI
                        results.append({
                            'scheme_code': scheme_code,
                            'scheme_name': fund.get('scheme_name', ''),
                            'fund_house': '',
                            'scheme_type': '',
                            'nav': fund.get('nav', 0),
                            'date': fund.get('date', '')
                        })
                        seen_codes.add(scheme_code)
            
            return results[:50]  # Limit to 50 results
        except Exception as e:
            logger.error(f"Error searching funds: {str(e)}")
        
        return []
    
    async def get_fund_list(self) -> List[dict]:
        """Get list of all available funds"""
        # This would typically require maintaining a local database
        # or fetching from AMFI's master file
        return []


class AMFIDataCollector:
    """Alternative data collector using AMFI official data"""
    
    def __init__(self):
        self.amfi_nav_url = "https://portal.amfiindia.com/spages/NAVAll.txt"
        
    async def fetch_amfi_nav_data(self) -> List[dict]:
        """Fetch NAV data from AMFI portal"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.amfi_nav_url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status == 200:
                        text = await response.text()
                        return self._parse_amfi_data(text)
        except Exception as e:
            logger.error(f"Error fetching AMFI data: {str(e)}")
        
        return []
    
    def _parse_amfi_data(self, text: str) -> List[dict]:
        """Parse AMFI NAV text format"""
        funds = []
        current_scheme = None
        
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # AMFI format: Scheme Code;ISIN Div Payout/ ISIN Growth / ISIN Div Reinvestment;Scheme Name;Net Asset Value;Date
            if ';' in line and not line.startswith('Open'):
                parts = line.split(';')
                if len(parts) >= 5:
                    try:
                        scheme_code = parts[0].strip()
                        scheme_name = parts[2].strip()
                        nav = float(parts[3].strip())
                        date_str = parts[4].strip()
                        
                        funds.append({
                            'scheme_code': scheme_code,
                            'scheme_name': scheme_name,
                            'nav': nav,
                            'date': date_str
                        })
                    except (ValueError, IndexError):
                        continue
        
        return funds

