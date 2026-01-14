# AIAG01 Dashboard - Setup Instructions

## Quick Start (3 Steps)

### Step 1: Start the Backend Server
```bash
cd agentic_system
py main.py
```

The backend will start on `http://localhost:8000`

### Step 2: Open the Dashboard
Simply open `dashboard/index.html` in your browser:
- **Double-click** the file, OR
- **Right-click** → Open with → Chrome/Firefox/Edge

### Step 3: View Real-Time Data
The dashboard will automatically:
- Connect to the backend API
- Fetch supplier data every 5 seconds
- Display Tier-1, Tier-2, Tier-3 suppliers
- Highlight high-risk suppliers in red

---

## Dashboard Features

### 1. Summary Cards
- **Total Suppliers**: Count of all suppliers
- **Critical Risks**: Suppliers with risk score > 70
- **Warnings**: Suppliers with risk score 40-70
- **Normal**: Suppliers with risk score < 40

### 2. Tier-Based Display
- **Tier 1**: Primary suppliers (purple badge)
- **Tier 2**: Secondary suppliers (pink badge)
- **Tier 3**: Raw material suppliers (blue badge)

### 3. Supplier Cards Show:
- **Reported Stock**: What supplier claims
- **Predicted Stock**: AI-calculated expected stock
- **Phantom Stock**: Difference (reported - predicted)
- **Risk %**: Deviation percentage with color-coded bar
- **Risk Score**: Calculated risk score (0-100)

### 4. Color Coding
- **Red Border**: Critical risk (>70 score)
- **Yellow Border**: Warning (40-70 score)
- **Green Border**: Normal (<40 score)

### 5. Auto-Refresh
- Refreshes every **5 seconds**
- Shows countdown timer
- Displays "Refreshing..." indicator

---

## Troubleshooting

### Dashboard shows "Failed to connect to backend"
**Solution**: Make sure backend is running
```bash
cd agentic_system
py main.py
```

### CORS Error in Browser Console
**Solution**: Backend already has CORS enabled. If issue persists:
1. Close all browser windows
2. Restart backend
3. Open dashboard again

### Data not updating
**Solution**: Check browser console (F12) for errors. Verify backend is accessible at `http://localhost:8000/api/health`

---

## Customization

### Change Refresh Interval
Edit `dashboard/index.html`, line 318:
```javascript
const REFRESH_INTERVAL = 5000; // Change to 10000 for 10 seconds
```

### Change API URL
Edit `dashboard/index.html`, line 317:
```javascript
const API_BASE = 'http://localhost:8000/api'; // Change if backend runs elsewhere
```

### Modify Risk Thresholds
Edit deviation thresholds in `renderSupplierCard()` function:
```javascript
const deviationClass = deviation > 30 ? 'high' : deviation > 15 ? 'medium' : '';
```

---

## Alternative: Run with Local Server

If you prefer running with a local server:

### Option 1: Python HTTP Server
```bash
cd dashboard
py -m http.server 3000
```
Open: `http://localhost:3000`

### Option 2: Node.js HTTP Server
```bash
cd dashboard
npx http-server -p 3000
```
Open: `http://localhost:3000`

---

## API Endpoints Used

The dashboard calls these backend endpoints:

1. `POST /api/analysis/run` - Triggers agent pipeline
2. `GET /api/suppliers` - Gets supplier list
3. `GET /api/risk-scores` - Gets risk assessments
4. `GET /api/predicted-stock` - Gets stock predictions
5. `GET /api/dashboard` - Gets summary data

---

## Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+

---

## Demo Recording Tips

When recording demo video:
1. Start backend first
2. Open dashboard
3. Show auto-refresh working
4. Point out high-risk suppliers (red)
5. Explain Tier 1/2/3 structure
6. Show phantom stock calculations
7. Highlight real-time updates

---

## Production Deployment

For production, host the dashboard on:
- **Vercel**: Drag & drop `dashboard` folder
- **Netlify**: Deploy `dashboard` folder
- **GitHub Pages**: Push to `gh-pages` branch

Update `API_BASE` to your production backend URL.
