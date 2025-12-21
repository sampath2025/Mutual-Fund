# Fix: Nippon Realty Fund NAV Fetching

## Problem
Unable to fetch real-time NAV for Nippon Realty Fund - likely incorrect scheme code.

## Quick Solution

### Step 1: Find the Correct Scheme Code

**Option A: Use MFAPI.in Website**
1. Visit: https://www.mfapi.in/
2. Search for "Nippon Realty" or "Nippon India Realty"
3. Click on the fund
4. The scheme code is in the URL (e.g., `https://www.mfapi.in/mf/123456`)
5. Copy the scheme code (numbers only)

**Option B: Use API Search (if backend is running)**
```bash
# In browser or Postman
GET http://localhost:8000/api/search?query=Nippon
```

**Option C: Check Nippon India Mutual Fund Website**
- Visit: https://www.nipponindiaim.com/
- Find "Nippon India Realty Fund"
- Scheme code is usually displayed on fund details page

### Step 2: Test the Scheme Code

Once you have a scheme code (e.g., `123456`), test it:

```bash
# Test endpoint
GET http://localhost:8000/api/nav/test/123456
```

Or in browser:
```
http://localhost:8000/api/nav/test/123456
```

### Step 3: Add Fund with Correct Code

1. Open the web app: http://localhost:3000
2. Go to "Manage Funds" tab
3. Click "Add Fund"
4. Enter:
   - **Scheme Code**: [The correct code you found]
   - **Scheme Name**: Nippon India Realty Fund
   - **Fund House**: Nippon India Mutual Fund
   - **Category**: Real Estate / Equity
   - **Alert Threshold**: 2.0
5. Click "Add Fund"

### Step 4: Verify NAV Fetching

1. Go to "Dashboard" tab
2. You should see the NAV data loading
3. If it shows "Loading..." or error, the scheme code might still be wrong

## Common Nippon Fund Names

The fund might be listed as:
- Nippon India Realty Fund
- Nippon Realty Fund
- Nippon India Real Estate Fund
- Reliance Realty Fund (if it was renamed)

## Enhanced Features Added

✅ **Better Search**: Now searches AMFI data directly
✅ **NAV Test Endpoint**: `/api/nav/test/{scheme_code}` to verify codes
✅ **Better Error Messages**: More helpful error messages
✅ **AMFI Fallback**: Falls back to AMFI if MFAPI fails

## API Endpoints

### Search Funds
```
GET /api/search?query=Nippon
```

### Test NAV Fetch
```
GET /api/nav/test/{scheme_code}
```

### Get NAV Data
```
GET /api/nav/{scheme_code}?days=30
```

## Troubleshooting

### If search returns no results:
- AMFI data might be slow to fetch
- Try searching manually on MFAPI.in
- Check if fund name is correct

### If NAV fetch fails:
1. Verify scheme code is correct
2. Check if fund is still active
3. Try the test endpoint to see detailed error
4. Fund might be discontinued

### If you get "Scheme code not found":
- The scheme code is incorrect
- Fund might be renamed or merged
- Try searching for variations of the name

## Manual Scheme Code Lookup

If automated search doesn't work:

1. **MFAPI.in Method**:
   - Go to https://www.mfapi.in/
   - Search for your fund
   - Scheme code is in URL: `/mf/{SCHEME_CODE}`

2. **AMFI Method**:
   - Go to https://www.amfiindia.com/
   - Download NAV data file
   - Search for fund name in the file
   - First column is scheme code

3. **Fund House Website**:
   - Visit Nippon India Mutual Fund website
   - Find fund details
   - Scheme code is usually displayed

---

**Once you have the correct scheme code, add it to the app and NAV fetching will work!**

