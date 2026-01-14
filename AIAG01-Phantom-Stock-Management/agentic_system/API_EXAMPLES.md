# 📡 REST API Documentation with Example Outputs

## Base URL
```
http://localhost:8000/api
```

---

## 1️⃣ GET /api/suppliers

**Description:** Get all supplier data across Tier-1, Tier-2, and Tier-3

**Request:**
```bash
curl http://localhost:8000/api/suppliers
```

**Response:**
```json
{
  "suppliers": [
    {
      "id": "T1-001",
      "name": "Tier1 Electronics",
      "tier": 1,
      "capacity": 10000,
      "reliability": 0.95
    },
    {
      "id": "T1-002",
      "name": "Tier1 Components",
      "tier": 1,
      "capacity": 8000,
      "reliability": 0.90
    },
    {
      "id": "T2-001",
      "name": "Tier2 Parts Co",
      "tier": 2,
      "capacity": 5000,
      "reliability": 0.85
    },
    {
      "id": "T2-002",
      "name": "Tier2 Materials",
      "tier": 2,
      "capacity": 6000,
      "reliability": 0.80
    },
    {
      "id": "T2-003",
      "name": "Tier2 Assembly",
      "tier": 2,
      "capacity": 4500,
      "reliability": 0.88
    },
    {
      "id": "T3-001",
      "name": "Tier3 Raw Materials",
      "tier": 3,
      "capacity": 3000,
      "reliability": 0.75
    },
    {
      "id": "T3-002",
      "name": "Tier3 Metals Ltd",
      "tier": 3,
      "capacity": 3500,
      "reliability": 0.70
    },
    {
      "id": "T3-003",
      "name": "Tier3 Plastics Inc",
      "tier": 3,
      "capacity": 2800,
      "reliability": 0.78
    }
  ],
  "total": 8,
  "by_tier": {
    "tier1": 2,
    "tier2": 3,
    "tier3": 3
  }
}
```

---

## 2️⃣ GET /api/predicted-stock

**Description:** Get predicted stock vs reported stock for all suppliers

**Request:**
```bash
curl http://localhost:8000/api/predicted-stock
```

**Response:**
```json
{
  "predicted_stock": [
    {
      "supplier_id": "T1-001",
      "supplier_name": "Tier1 Electronics",
      "tier": 1,
      "reported_stock": 1450,
      "predicted_stock": 1400,
      "deviation": 0.036,
      "deviation_percentage": 3.6
    },
    {
      "supplier_id": "T2-001",
      "supplier_name": "Tier2 Parts Co",
      "tier": 2,
      "reported_stock": 850,
      "predicted_stock": 700,
      "deviation": 0.214,
      "deviation_percentage": 21.4
    },
    {
      "supplier_id": "T3-002",
      "supplier_name": "Tier3 Metals Ltd",
      "tier": 3,
      "reported_stock": 6500,
      "predicted_stock": 4200,
      "deviation": 0.548,
      "deviation_percentage": 54.8
    }
  ],
  "total": 3
}
```

**Use Case:** Display reported vs predicted inventory comparison chart

---

## 3️⃣ GET /api/risk-scores

**Description:** Get risk scores and classifications for all suppliers

**Request:**
```bash
curl http://localhost:8000/api/risk-scores
```

**Response:**
```json
{
  "risk_scores": [
    {
      "supplier_id": "T1-001",
      "supplier_name": "Tier1 Electronics",
      "tier": 1,
      "risk_score": 8.47,
      "risk_level": "NORMAL",
      "classification": "normal",
      "components": {
        "deviation_score": 1.8,
        "tier_score": 6.67,
        "history_score": 0.0
      }
    },
    {
      "supplier_id": "T2-001",
      "supplier_name": "Tier2 Parts Co",
      "tier": 2,
      "risk_score": 47.35,
      "risk_level": "WARNING",
      "classification": "monitor_closely",
      "components": {
        "deviation_score": 10.7,
        "tier_score": 13.34,
        "history_score": 0.0
      }
    },
    {
      "supplier_id": "T3-002",
      "supplier_name": "Tier3 Metals Ltd",
      "tier": 3,
      "risk_score": 77.41,
      "risk_level": "CRITICAL",
      "classification": "phantom_stock_likely",
      "components": {
        "deviation_score": 27.4,
        "tier_score": 20.01,
        "history_score": 10.0
      }
    }
  ],
  "total": 3,
  "summary": {
    "critical": 1,
    "warning": 1,
    "normal": 1
  }
}
```

**Use Case:** Display risk heatmap, risk score gauges

---

## 4️⃣ GET /api/alerts

**Description:** Get active alerts and recommendations

**Request:**
```bash
curl http://localhost:8000/api/alerts
```

**Response:**
```json
{
  "alerts": [
    {
      "alert_id": "ALERT-T3-002-20240115143022",
      "severity": "CRITICAL",
      "supplier_id": "T3-002",
      "supplier_name": "Tier3 Metals Ltd",
      "tier": 3,
      "message": "CRITICAL: Phantom stock detected at Tier3 Metals Ltd",
      "risk_score": 77.41,
      "deviation": "54.8%",
      "reported_stock": 6500,
      "expected_stock": 4200,
      "timestamp": "2024-01-15T14:30:22.123456"
    },
    {
      "alert_id": "ALERT-T2-001-20240115143023",
      "severity": "WARNING",
      "supplier_id": "T2-001",
      "supplier_name": "Tier2 Parts Co",
      "tier": 2,
      "message": "WARNING: Potential disruption at Tier2 Parts Co",
      "risk_score": 47.35,
      "deviation": "21.4%",
      "timestamp": "2024-01-15T14:30:23.456789"
    }
  ],
  "recommendations": [
    {
      "supplier_id": "T3-002",
      "action": "IMMEDIATE_AUDIT",
      "description": "Conduct immediate physical inventory audit at Tier3 Metals Ltd",
      "priority": "P0",
      "estimated_impact": "High supply chain disruption risk"
    },
    {
      "supplier_id": "T2-001",
      "action": "INCREASE_MONITORING",
      "description": "Increase monitoring frequency for Tier2 Parts Co",
      "priority": "P1",
      "estimated_impact": "Medium supply chain disruption risk"
    }
  ],
  "total_alerts": 2
}
```

**Use Case:** Display alert notifications, action items

---

## 5️⃣ GET /api/dashboard

**Description:** Get complete dashboard data (all-in-one endpoint)

**Request:**
```bash
curl http://localhost:8000/api/dashboard
```

**Response:**
```json
{
  "summary": {
    "phantom_stock_detected": 1,
    "total_alerts": 2,
    "status": "ATTENTION_REQUIRED",
    "total_suppliers": 8,
    "high_deviations": 2
  },
  "alerts": [
    {
      "alert_id": "ALERT-T3-002-20240115143022",
      "severity": "CRITICAL",
      "supplier_id": "T3-002",
      "supplier_name": "Tier3 Metals Ltd",
      "tier": 3,
      "message": "CRITICAL: Phantom stock detected at Tier3 Metals Ltd",
      "risk_score": 77.41,
      "deviation": "54.8%",
      "reported_stock": 6500,
      "expected_stock": 4200,
      "timestamp": "2024-01-15T14:30:22.123456"
    }
  ],
  "critical_risks": [
    {
      "supplier_id": "T3-002",
      "supplier_name": "Tier3 Metals Ltd",
      "tier": 3,
      "risk_score": 77.41,
      "risk_level": "CRITICAL",
      "classification": "phantom_stock_likely",
      "deviation_percentage": 54.8,
      "reported_stock": 6500,
      "expected_stock": 4200,
      "escalate": true
    }
  ],
  "warnings": [
    {
      "supplier_id": "T2-001",
      "supplier_name": "Tier2 Parts Co",
      "tier": 2,
      "risk_score": 47.35,
      "risk_level": "WARNING",
      "classification": "monitor_closely",
      "deviation_percentage": 21.4,
      "reported_stock": 850,
      "expected_stock": 700,
      "escalate": true
    }
  ]
}
```

**Use Case:** Main dashboard overview with all key metrics

---

## 6️⃣ POST /api/analysis/run

**Description:** Run the agentic analysis pipeline

**Request:**
```bash
curl -X POST http://localhost:8000/api/analysis/run
```

**Response:**
```json
{
  "status": "complete",
  "pipeline": [
    "MonitoringAgent → ValidationAgent → RiskAgent → SupervisorAgent"
  ],
  "agent_outputs": {
    "monitoring": {
      "sender": "MonitoringAgent",
      "data": {
        "processed_data": [...],
        "anomalies": [...]
      },
      "metadata": {
        "total_records": 30,
        "anomaly_count": 0,
        "quality_rate": 1.0
      }
    },
    "validation": {
      "sender": "ValidationAgent",
      "data": {
        "validations": [...],
        "high_deviations": [...]
      },
      "metadata": {
        "total_validated": 30,
        "high_deviation_count": 2
      }
    },
    "risk": {
      "sender": "RiskAgent",
      "data": {
        "risk_assessments": [...],
        "critical_risks": [...],
        "warnings": [...]
      },
      "metadata": {
        "total_assessed": 30,
        "critical_count": 1,
        "warning_count": 1
      }
    },
    "supervisor": {
      "sender": "SupervisorAgent",
      "data": {
        "alerts": [...],
        "recommendations": [...],
        "decision": "ATTENTION_REQUIRED"
      },
      "metadata": {
        "total_alerts": 2,
        "critical_alerts": 1,
        "warning_alerts": 1
      }
    }
  },
  "summary": {
    "total_records": 30,
    "anomalies": 0,
    "high_deviations": 2,
    "critical_risks": 1,
    "warnings": 1,
    "total_alerts": 2,
    "final_decision": "ATTENTION_REQUIRED"
  }
}
```

**Use Case:** Trigger analysis and get full pipeline results

---

## 7️⃣ GET /api/pipeline/trace

**Description:** Get full agent communication trace

**Request:**
```bash
curl http://localhost:8000/api/pipeline/trace
```

**Response:**
```json
{
  "pipeline": "MonitoringAgent → ValidationAgent → RiskAgent → SupervisorAgent",
  "agent_outputs": {
    "monitoring": {...},
    "validation": {...},
    "risk": {...},
    "supervisor": {...}
  },
  "communication_flow": [
    {
      "step": 1,
      "from": "DataSource",
      "to": "MonitoringAgent",
      "message_type": "Raw inventory data"
    },
    {
      "step": 2,
      "from": "MonitoringAgent",
      "to": "ValidationAgent",
      "message_type": "MonitoringOutput (validated data + anomalies)"
    },
    {
      "step": 3,
      "from": "ValidationAgent",
      "to": "RiskAgent",
      "message_type": "ValidationOutput (validations + high deviations)"
    },
    {
      "step": 4,
      "from": "RiskAgent",
      "to": "SupervisorAgent",
      "message_type": "RiskOutput (risk assessments + critical risks)"
    },
    {
      "step": 5,
      "from": "SupervisorAgent",
      "to": "Dashboard",
      "message_type": "SupervisorOutput (alerts + recommendations)"
    }
  ]
}
```

**Use Case:** Debug agent communication, visualize pipeline

---

## 📊 Dashboard Integration Examples

### React Example
```javascript
// Fetch dashboard data
const response = await fetch('http://localhost:8000/api/dashboard');
const data = await response.json();

// Display summary
console.log(`Phantom Stock: ${data.summary.phantom_stock_detected}`);
console.log(`Status: ${data.summary.status}`);

// Display alerts
data.alerts.forEach(alert => {
  console.log(`${alert.severity}: ${alert.message}`);
});
```

### Python Example
```python
import requests

# Get risk scores
response = requests.get('http://localhost:8000/api/risk-scores')
data = response.json()

# Display risk summary
print(f"Critical: {data['summary']['critical']}")
print(f"Warning: {data['summary']['warning']}")
print(f"Normal: {data['summary']['normal']}")

# Display risk scores
for risk in data['risk_scores']:
    print(f"{risk['supplier_name']}: {risk['risk_score']} ({risk['risk_level']})")
```

### JavaScript Fetch Example
```javascript
// Get predicted stock
fetch('http://localhost:8000/api/predicted-stock')
  .then(res => res.json())
  .then(data => {
    data.predicted_stock.forEach(item => {
      console.log(`${item.supplier_name}:`);
      console.log(`  Reported: ${item.reported_stock}`);
      console.log(`  Predicted: ${item.predicted_stock}`);
      console.log(`  Deviation: ${item.deviation_percentage}%`);
    });
  });
```

---

## 🎨 Dashboard UI Components

### 1. Summary Cards
**Data Source:** `GET /api/dashboard`
```javascript
{
  phantom_stock_detected: 1,
  total_alerts: 2,
  status: "ATTENTION_REQUIRED",
  total_suppliers: 8
}
```

### 2. Alert List
**Data Source:** `GET /api/alerts`
```javascript
alerts.map(alert => (
  <Alert severity={alert.severity}>
    {alert.message}
  </Alert>
))
```

### 3. Risk Heatmap
**Data Source:** `GET /api/risk-scores`
```javascript
risk_scores.map(risk => ({
  supplier: risk.supplier_name,
  score: risk.risk_score,
  color: risk.risk_level === 'CRITICAL' ? 'red' : 
         risk.risk_level === 'WARNING' ? 'orange' : 'green'
}))
```

### 4. Stock Comparison Chart
**Data Source:** `GET /api/predicted-stock`
```javascript
predicted_stock.map(item => ({
  supplier: item.supplier_name,
  reported: item.reported_stock,
  predicted: item.predicted_stock
}))
```

---

## 🔧 API Testing

### Using cURL
```bash
# Test all endpoints
curl http://localhost:8000/api/suppliers
curl http://localhost:8000/api/predicted-stock
curl http://localhost:8000/api/risk-scores
curl http://localhost:8000/api/alerts
curl http://localhost:8000/api/dashboard
curl -X POST http://localhost:8000/api/analysis/run
```

### Using Postman
1. Import collection from `/docs/postman_collection.json`
2. Run all requests
3. View responses in JSON format

### Using Python
```python
import requests

BASE_URL = "http://localhost:8000/api"

# Get all data
suppliers = requests.get(f"{BASE_URL}/suppliers").json()
predicted = requests.get(f"{BASE_URL}/predicted-stock").json()
risks = requests.get(f"{BASE_URL}/risk-scores").json()
alerts = requests.get(f"{BASE_URL}/alerts").json()
dashboard = requests.get(f"{BASE_URL}/dashboard").json()

print(f"Total suppliers: {suppliers['total']}")
print(f"Critical risks: {risks['summary']['critical']}")
print(f"Total alerts: {alerts['total_alerts']}")
```

---

## 📝 Response Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request (run analysis first) |
| 404 | Endpoint not found |
| 500 | Internal server error |

---

## 🚀 Quick Start

1. **Start the server:**
```bash
cd agentic_system
python main.py
```

2. **Test API:**
```bash
curl http://localhost:8000/api/dashboard
```

3. **View interactive docs:**
```
http://localhost:8000/docs
```

---

## ✅ All Endpoints Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/suppliers` | GET | Get all supplier data |
| `/api/predicted-stock` | GET | Get predicted vs reported stock |
| `/api/risk-scores` | GET | Get risk scores for all suppliers |
| `/api/alerts` | GET | Get active alerts |
| `/api/dashboard` | GET | Get complete dashboard data |
| `/api/analysis/run` | POST | Run agent pipeline |
| `/api/pipeline/trace` | GET | Get agent communication trace |

**All endpoints return JSON and are CORS-enabled for frontend integration.**
