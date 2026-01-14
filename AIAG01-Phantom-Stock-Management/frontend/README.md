# Professional Frontend Setup

## What This Frontend Does

✅ **Connects to your existing backend** (no backend changes)  
✅ **Live Supply Chain Dashboard** with Tier-1/2/3 table  
✅ **Animated Agent Panel** showing 4 agents with status  
✅ **Charts** - Risk distribution bar chart + Risk heatmap  
✅ **Flashing Alerts** when risk > 50%  
✅ **AI Insights Box** with explanations  
✅ **Simulation Controls** - Breakdown, Delay, Reset buttons  

---

## Quick Start

### Step 1: Make sure backend is running
```bash
cd agentic_system
py main.py
```
Backend should be on `http://localhost:8001`

### Step 2: Open the frontend
```bash
# Simply double-click:
frontend/index.html

# Or from command line:
start frontend\index.html
```

That's it! The frontend will automatically connect to your backend APIs.

---

## Features Breakdown

### 1️⃣ Live Supply Chain Table
- Shows all 8 suppliers (Tier-1, Tier-2, Tier-3)
- Columns: Supplier, Tier, Reported Stock, Predicted Stock, Deviation, Risk %, Status
- **Red rows** = High risk (>70%)
- **Yellow rows** = Medium risk (40-70%)
- **Green rows** = Normal (<40%)

### 2️⃣ Animated Agent Panel
- 4 agent cards with emojis
- **Thinking animation** - Card pulses and glows
- **Status updates** - "Monitoring...", "Calculating...", "Analyzing...", "Deciding..."
- **Color coding** - Yellow (processing), Green (complete)

### 3️⃣ Charts
- **Risk Distribution** - Bar chart showing risk score per supplier
- **Risk Heatmap** - Average risk by tier (Tier 1, 2, 3)
- Auto-updates with new data

### 4️⃣ Flashing Alerts
- Appears when any supplier has risk > 50%
- **Red flashing box** with border
- Shows which agent raised the alert
- Lists all high-risk suppliers

### 5️⃣ AI Insights Box
- "Analysis Complete: Processed X suppliers"
- "Risk Assessment: X critical, Y warnings"
- "Recommendation: Immediate action required" or "System normal"
- "Phantom Stock: X instances detected"

### 6️⃣ Simulation Controls
- **Run Analysis** - Triggers `/api/analysis/run`
- **Simulate Breakdown** - Runs analysis (simulates failure)
- **Simulate Delay** - Runs analysis (simulates delay)
- **Reset Data** - Reloads page

---

## API Endpoints Used

The frontend calls these existing APIs:

```javascript
POST /api/analysis/run       // Trigger agent pipeline
GET  /api/suppliers          // Get supplier list
GET  /api/risk-scores        // Get risk assessments
GET  /api/predicted-stock    // Get stock predictions
GET  /api/dashboard          // Get summary data
```

**No backend changes needed!**

---

## Customization

### Change API URL
Edit `frontend/index.html`, line 127:
```javascript
const API_BASE = 'http://localhost:8001/api';
```

### Change Colors
Edit the Tailwind classes:
- `bg-red-900` = High risk background
- `bg-yellow-900` = Medium risk background
- `bg-green-900` = Normal background

### Change Animation Speed
Edit CSS animations (lines 8-18):
```css
@keyframes thinking {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}
```

---

## Deployment

### Option 1: Static Hosting (Vercel/Netlify)
1. Push `frontend/` folder to GitHub
2. Connect to Vercel/Netlify
3. Set root directory to `frontend`
4. Deploy
5. Update `API_BASE` to your production backend URL

### Option 2: Same Server as Backend
1. Copy `frontend/index.html` to `agentic_system/static/`
2. Add to `main.py`:
```python
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="static", html=True), name="static")
```
3. Access at `http://localhost:8001/`

### Option 3: GitHub Pages
1. Push `frontend/` to GitHub
2. Go to Settings → Pages
3. Select branch and `/frontend` folder
4. Your URL: `https://username.github.io/repo-name/`

---

## Tech Stack

- **Tailwind CSS** - Styling (CDN)
- **Chart.js** - Charts (CDN)
- **Vanilla JavaScript** - No frameworks
- **No build process** - Just open HTML file

---

## Troubleshooting

### "Failed to connect to backend"
- Make sure backend is running: `py main.py`
- Check backend is on port 8001
- Check console for CORS errors

### Charts not showing
- Wait for "Run Analysis" to complete
- Check browser console for errors
- Verify Chart.js CDN loaded

### Agents not animating
- Click "Run Analysis" button
- Check backend is responding
- Verify `/api/analysis/run` endpoint works

### Table shows "Loading data..."
- Backend not responding
- Check API endpoints are accessible
- Try manual API call: `curl http://localhost:8001/api/suppliers`

---

## Demo Tips for Judges

1. **Start with backend running**
2. **Open frontend** - Shows professional UI immediately
3. **Click "Run Analysis"** - Watch agents animate
4. **Point to table** - Show red/yellow/green risk levels
5. **Show charts** - Risk distribution and heatmap
6. **Show alert** - Flashing red box for high risk
7. **Show AI insights** - Explain recommendations
8. **Click simulation buttons** - Show interactivity

**Total demo time: 2-3 minutes**

---

## File Structure

```
frontend/
├── index.html          # Complete frontend (single file)
└── README.md          # This file
```

**That's it!** No dependencies, no build process, no configuration.

---

## Next Steps

1. ✅ Backend running on port 8001
2. ✅ Open `frontend/index.html`
3. ✅ Click "Run Analysis"
4. ✅ Watch the magic happen!

**Your professional hackathon demo is ready!** 🚀
