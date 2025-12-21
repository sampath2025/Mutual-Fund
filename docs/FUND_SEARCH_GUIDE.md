# 🔍 Finding Scheme Code for Nippon Realty Fund

## Issue
Unable to fetch real-time NAV for Nippon Realty Fund - likely due to incorrect scheme code.

## Solutions

### Method 1: Use the Search API

The backend now has an enhanced search endpoint:

```bash
# Search for funds
GET http://localhost:8000/api/search?query=Nippon

# Test a specific scheme code
GET http://localhost:8000/api/nav/test/{scheme_code}
```

### Method 2: Find Scheme Code Manually

1. **Visit MFAPI.in**:
   - Go to: https://www.mfapi.in/
   - Search for "Nippon Realty"
   - Get the scheme code from the URL or fund details

2. **Visit AMFI Website**:
   - Go to: https://www.amfiindia.com/
   - Navigate to NAV data
   - Search for the fund

3. **Check Fund House Website**:
   - Visit Nippon India Mutual Fund website
   - Find the fund details page
   - Scheme code is usually displayed

### Method 3: Use the Search Script

```bash
python scripts/find_fund.py "Nippon Realty"
# Or try variations:
python scripts/find_fund.py "Nippon"
python scripts/find_fund.py "Realty"
```

### Method 4: Common Nippon Fund Scheme Codes

Some common Nippon fund codes (verify these):
- Nippon India Growth Fund: Check MFAPI.in
- Nippon India Small Cap Fund: Check MFAPI.in
- Nippon India Realty Fund: **Need to find correct code**

## Enhanced Features Added

### 1. Enhanced Search
- Now searches AMFI data directly
- Better matching algorithm
- Returns scheme codes with fund details

### 2. NAV Test Endpoint
- Test if a scheme code works: `/api/nav/test/{scheme_code}`
- Shows which data source was used
- Provides helpful error messages

### 3. Better Error Handling
- More detailed error messages
- Fallback to AMFI if MFAPI fails
- Logging for debugging

## Steps to Fix

1. **Find the correct scheme code** using one of the methods above
2. **Test the scheme code**:
   ```bash
   curl http://localhost:8000/api/nav/test/{scheme_code}
   ```
3. **Add the fund** with the correct scheme code in the web app
4. **Verify NAV fetching** works

## API Endpoints

### Search Funds
```
GET /api/search?query=Nippon
```

Response:
```json
{
  "query": "Nippon",
  "count": 5,
  "results": [
    {
      "scheme_code": "123456",
      "scheme_name": "Nippon India Realty Fund",
      "fund_house": "Nippon India Mutual Fund",
      "nav": 45.67,
      "date": "21-Dec-2024"
    }
  ]
}
```

### Test NAV Fetch
```
GET /api/nav/test/123456
```

Response:
```json
{
  "success": true,
  "scheme_code": "123456",
  "source": "MFAPI",
  "nav": 45.67,
  "date": "2024-12-21T00:00:00"
}
```

## Troubleshooting

### If search returns no results:
1. Try partial names (e.g., "Nippon" instead of full name)
2. Check if fund name is correct
3. Fund might be discontinued or renamed

### If NAV fetch fails:
1. Verify scheme code is correct
2. Check if fund is active
3. Try the test endpoint to see detailed error

### If AMFI data is slow:
- First search uses AMFI (can be slow)
- Subsequent NAV fetches use MFAPI (faster)

---

**Once you have the correct scheme code, add it to the app and NAV fetching should work!**

