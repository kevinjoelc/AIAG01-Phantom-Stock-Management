# 🎯 Dashboard Developer Guide

## Quick Reference for Frontend Integration

---

## 🚀 Getting Started

### 1. Start the Backend
```bash
cd agentic_system
pip install -r requirements.txt
python main.py
```

Backend runs at: **http://localhost:8000**

### 2. Test APIs
```bash
python test_apis.py
```

### 3. View Interactive Docs
Open: **http://localhost:8000/docs**

---

## 📡 Essential Endpoints for Dashboard

### **Main Dashboard Endpoint**
```
GET /api/dashboard
```
Returns everything you need in one call:
- Summary metrics
- Active alerts
- Critical risks
- Warnings

**Use this for:** Main dashboard overview

---

### **Supplier Data**
```
GET /api/suppliers
```
Returns all 8 suppliers (Tier-1, 2, 3)

**Use this for:** Supplier list, supplier map

---

### **Predicted Stock**
```
GET /api/predicted-stock
```
Returns reported vs predicted inventory

**Use this for:** Stock comparison charts, deviation analysis

---

### **Risk Scores**
```
GET /api/risk-scores
```
Returns risk scores (0-100) for all suppliers

**Use this for:** Risk heatmap, gauge charts, risk distribution

---

### **Alerts**
```
GET /api/alerts
```
Returns active alerts and recommendations

**Use this for:** Alert notifications, action items

---

## 📊 Dashboard Components

### 1. Summary Cards

**Endpoint:** `GET /api/dashboard`

**Data:**
```json
{
  "summary": {
    "phantom_stock_detected": 1,
    "total_alerts": 2,
    "status": "ATTENTION_REQUIRED",
    "total_suppliers": 8,
    "high_deviations": 2
  }
}
```

**Display:**
```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Phantom Stock   │  │ Total Alerts    │  │ System Status   │
│      1          │  │       2         │  │ ATTENTION_REQ   │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

---

### 2. Alert List

**Endpoint:** `GET /api/alerts`

**Data:**
```json
{
  "alerts": [
    {
      "severity": "CRITICAL",
      "message": "CRITICAL: Phantom stock detected at Tier3 Metals Ltd",
      "risk_score": 77.41,
      "deviation": "54.8%",
      "timestamp": "2024-01-15T14:30:22"
    }
  ]
}
```

**Display:**
```
🔴 CRITICAL: Phantom stock detected at Tier3 Metals Ltd
   Risk Score: 77.41 | Deviation: 54.8%
   Time: 2024-01-15 14:30:22

🟡 WARNING: Potential disruption at Tier2 Parts Co
   Risk Score: 47.35 | Deviation: 21.4%
   Time: 2024-01-15 14:30:23
```

---

### 3. Risk Heatmap

**Endpoint:** `GET /api/risk-scores`

**Data:**
```json
{
  "risk_scores": [
    {
      "supplier_name": "Tier3 Metals Ltd",
      "risk_score": 77.41,
      "risk_level": "CRITICAL"
    },
    {
      "supplier_name": "Tier2 Parts Co",
      "risk_score": 47.35,
      "risk_level": "WARNING"
    }
  ]
}
```

**Display:**
```
Tier3 Metals Ltd    ████████████████████ 77.41 🔴 CRITICAL
Tier2 Parts Co      ██████████           47.35 🟡 WARNING
Tier1 Electronics   ██                    8.47 🟢 NORMAL
```

---

### 4. Stock Comparison Chart

**Endpoint:** `GET /api/predicted-stock`

**Data:**
```json
{
  "predicted_stock": [
    {
      "supplier_name": "Tier3 Metals Ltd",
      "reported_stock": 6500,
      "predicted_stock": 4200,
      "deviation_percentage": 54.8
    }
  ]
}
```

**Display:**
```
Tier3 Metals Ltd
  Reported:  ████████████████ 6500
  Predicted: ██████████       4200
  Deviation: 54.8% ⚠️
```

---

### 5. Supplier Map

**Endpoint:** `GET /api/suppliers`

**Data:**
```json
{
  "suppliers": [
    {
      "id": "T1-001",
      "name": "Tier1 Electronics",
      "tier": 1,
      "capacity": 10000,
      "reliability": 0.95
    }
  ]
}
```

**Display:**
```
        OEM
         ↑
    ┌────┴────┐
  Tier-1   Tier-1
    ↑         ↑
  ┌─┴─┐     ┌─┴─┐
Tier-2 Tier-2 Tier-2
  ↑     ↑     ↑
Tier-3 Tier-3 Tier-3
```

---

## 💻 Code Examples

### React Component
```jsx
import { useEffect, useState } from 'react';

function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/dashboard')
      .then(res => res.json())
      .then(data => setData(data));
  }, []);

  if (!data) return <div>Loading...</div>;

  return (
    <div>
      <h1>Phantom Stock Dashboard</h1>
      
      {/* Summary Cards */}
      <div className="summary">
        <Card title="Phantom Stock" value={data.summary.phantom_stock_detected} />
        <Card title="Total Alerts" value={data.summary.total_alerts} />
        <Card title="Status" value={data.summary.status} />
      </div>

      {/* Alerts */}
      <div className="alerts">
        {data.alerts.map(alert => (
          <Alert key={alert.alert_id} severity={alert.severity}>
            {alert.message}
          </Alert>
        ))}
      </div>

      {/* Critical Risks */}
      <div className="risks">
        {data.critical_risks.map(risk => (
          <RiskCard key={risk.supplier_id} risk={risk} />
        ))}
      </div>
    </div>
  );
}
```

---

### Vue Component
```vue
<template>
  <div class="dashboard">
    <h1>Phantom Stock Dashboard</h1>
    
    <div class="summary">
      <div class="card">
        <h3>Phantom Stock</h3>
        <p>{{ dashboard.summary.phantom_stock_detected }}</p>
      </div>
      <div class="card">
        <h3>Total Alerts</h3>
        <p>{{ dashboard.summary.total_alerts }}</p>
      </div>
    </div>

    <div class="alerts">
      <div v-for="alert in dashboard.alerts" :key="alert.alert_id" 
           :class="['alert', alert.severity.toLowerCase()]">
        {{ alert.message }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dashboard: null
    }
  },
  mounted() {
    fetch('http://localhost:8000/api/dashboard')
      .then(res => res.json())
      .then(data => this.dashboard = data);
  }
}
</script>
```

---

### Vanilla JavaScript
```javascript
// Fetch dashboard data
async function loadDashboard() {
  const response = await fetch('http://localhost:8000/api/dashboard');
  const data = await response.json();

  // Update summary
  document.getElementById('phantom-stock').textContent = 
    data.summary.phantom_stock_detected;
  document.getElementById('total-alerts').textContent = 
    data.summary.total_alerts;
  document.getElementById('status').textContent = 
    data.summary.status;

  // Display alerts
  const alertsContainer = document.getElementById('alerts');
  data.alerts.forEach(alert => {
    const div = document.createElement('div');
    div.className = `alert ${alert.severity.toLowerCase()}`;
    div.textContent = alert.message;
    alertsContainer.appendChild(div);
  });
}

// Load on page load
window.onload = loadDashboard;
```

---

## 🔄 Real-Time Updates

### Polling (Simple)
```javascript
// Refresh every 30 seconds
setInterval(() => {
  fetch('http://localhost:8000/api/dashboard')
    .then(res => res.json())
    .then(data => updateDashboard(data));
}, 30000);
```

### Manual Refresh
```javascript
function refreshData() {
  // Run analysis
  fetch('http://localhost:8000/api/analysis/run', { method: 'POST' })
    .then(() => fetch('http://localhost:8000/api/dashboard'))
    .then(res => res.json())
    .then(data => updateDashboard(data));
}

// Add refresh button
<button onClick={refreshData}>🔄 Refresh</button>
```

---

## 🎨 Styling Recommendations

### Alert Colors
```css
.alert.critical {
  background: #fee;
  border-left: 4px solid #e74c3c;
  color: #c0392b;
}

.alert.warning {
  background: #fef5e7;
  border-left: 4px solid #f39c12;
  color: #d68910;
}

.alert.normal {
  background: #e8f5e9;
  border-left: 4px solid #27ae60;
  color: #1e8449;
}
```

### Risk Score Colors
```javascript
function getRiskColor(score) {
  if (score > 70) return '#e74c3c'; // Red
  if (score > 40) return '#f39c12'; // Orange
  return '#27ae60'; // Green
}
```

---

## 🧪 Testing Your Integration

### 1. Test API Connection
```javascript
fetch('http://localhost:8000/api/health')
  .then(res => res.json())
  .then(data => console.log('API Status:', data.status))
  .catch(err => console.error('API Error:', err));
```

### 2. Test Data Loading
```javascript
fetch('http://localhost:8000/api/dashboard')
  .then(res => res.json())
  .then(data => {
    console.log('Phantom Stock:', data.summary.phantom_stock_detected);
    console.log('Alerts:', data.alerts.length);
    console.log('Status:', data.summary.status);
  });
```

### 3. Test Analysis Trigger
```javascript
fetch('http://localhost:8000/api/analysis/run', { method: 'POST' })
  .then(res => res.json())
  .then(data => console.log('Analysis Status:', data.status));
```

---

## 📝 API Response Times

| Endpoint | Typical Response Time |
|----------|----------------------|
| `/api/suppliers` | <10ms |
| `/api/predicted-stock` | <50ms |
| `/api/risk-scores` | <50ms |
| `/api/alerts` | <10ms |
| `/api/dashboard` | <100ms |
| `/api/analysis/run` | <200ms |

---

## ✅ Checklist for Dashboard

- [ ] Display summary metrics (phantom stock, alerts, status)
- [ ] Show alert list with severity colors
- [ ] Display risk scores with visual indicators
- [ ] Show stock comparison (reported vs predicted)
- [ ] Add refresh button to trigger analysis
- [ ] Handle loading states
- [ ] Handle error states
- [ ] Add auto-refresh (optional)
- [ ] Style alerts by severity
- [ ] Show supplier hierarchy

---

## 🆘 Troubleshooting

### CORS Error
**Solution:** Backend already has CORS enabled. Check backend is running.

### 404 Error
**Solution:** Ensure backend is at http://localhost:8000

### Empty Data
**Solution:** Call `POST /api/analysis/run` first to generate data

### Slow Response
**Solution:** Normal for first request. Subsequent requests are cached.

---

## 📞 Quick Reference

| Need | Endpoint |
|------|----------|
| Everything | `GET /api/dashboard` |
| Suppliers | `GET /api/suppliers` |
| Stock Data | `GET /api/predicted-stock` |
| Risk Scores | `GET /api/risk-scores` |
| Alerts | `GET /api/alerts` |
| Run Analysis | `POST /api/analysis/run` |

---

## 🚀 You're Ready!

1. ✅ Backend running at http://localhost:8000
2. ✅ APIs documented with examples
3. ✅ Test script available (`test_apis.py`)
4. ✅ Interactive docs at http://localhost:8000/docs
5. ✅ Code examples for React/Vue/Vanilla JS

**Start building your dashboard! 🎨**
