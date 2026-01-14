# API Documentation

## Base URL
```
http://localhost:5000/api
```

---

## Endpoints

### 1. Health Check
**GET** `/health`

Check if the service is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "AIAG01 Phantom Stock Management",
  "agents": {
    "monitoring": "Supply Monitoring Agent",
    "validation": "Validation Agent",
    "risk_analysis": "Risk Analysis Agent",
    "supervisor": "Supervisor Agent"
  }
}
```

---

### 2. Get All Suppliers
**GET** `/suppliers`

Retrieve all suppliers across Tier-1, Tier-2, and Tier-3.

**Response:**
```json
{
  "suppliers": [
    {
      "id": "T1-001",
      "name": "Tier1 Electronics Inc",
      "tier": 1,
      "capacity": 10000,
      "reliability": 0.95
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

### 3. Get Reported Inventory
**GET** `/inventory/reported?days=30`

Get reported inventory data from suppliers.

**Query Parameters:**
- `days` (optional): Number of days to look back (default: 30)

**Response:**
```json
{
  "inventory_data": [
    {
      "supplier_id": "T1-001",
      "supplier_name": "Tier1 Electronics Inc",
      "tier": 1,
      "date": "2024-01-15",
      "reported_stock": 5000,
      "production_rate": 7000,
      "consumption_rate": 5600,
      "expected_stock": 1400,
      "reliability": 0.95
    }
  ],
  "total_records": 240
}
```

---

### 4. Get Predicted Inventory
**GET** `/inventory/predicted`

Get predicted inventory levels from Validation Agent.

**Response:**
```json
{
  "predictions": [
    {
      "supplier_id": "T1-001",
      "predicted_stock": 1400,
      "production_rate": 7000,
      "consumption_rate": 5600
    }
  ],
  "total": 8
}
```

---

### 5. Run Full Analysis (Main Endpoint)
**POST** `/analysis/run`

Execute the complete agentic AI pipeline. This orchestrates all 4 agents.

**Response:**
```json
{
  "status": "analysis_complete",
  "summary": {
    "agent": "Supervisor Agent",
    "summary": {
      "total_suppliers_monitored": 240,
      "validations_performed": 240,
      "risks_identified": 5,
      "alerts_generated": 5,
      "phantom_stock_detected": 2,
      "status": "ATTENTION_REQUIRED"
    }
  },
  "agent_outputs": {
    "monitoring": { ... },
    "validation": { ... },
    "risk_analysis": { ... },
    "supervisor": { ... }
  }
}
```

---

### 6. Get Risk Assessments
**GET** `/risks`

Retrieve risk scores and classifications from Risk Analysis Agent.

**Response:**
```json
{
  "agent": "Risk Analysis Agent",
  "risk_assessments": [
    {
      "supplier_id": "T3-002",
      "supplier_name": "Tier3 Metals Ltd",
      "tier": 3,
      "risk_score": 75.34,
      "risk_level": "CRITICAL",
      "classification": "phantom_stock_likely",
      "deviation_percentage": 45.2,
      "reported_stock": 6500,
      "expected_stock": 4200,
      "escalate": true,
      "components": {
        "deviation_score": 22.6,
        "tier_score": 20.0,
        "history_score": 10.0
      }
    }
  ],
  "critical_risks": [ ... ],
  "warnings": [ ... ],
  "total_assessed": 240,
  "critical_count": 2,
  "warning_count": 3
}
```

---

### 7. Get Alerts
**GET** `/alerts`

Retrieve active alerts and recommendations from Supervisor Agent.

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
      "risk_score": 75.34,
      "deviation": "45.2%",
      "reported_stock": 6500,
      "expected_stock": 4200,
      "timestamp": "2024-01-15T14:30:22.123456"
    }
  ],
  "recommendations": [
    {
      "supplier_id": "T3-002",
      "action": "IMMEDIATE_AUDIT",
      "description": "Conduct immediate physical inventory audit at Tier3 Metals Ltd",
      "priority": "P0",
      "estimated_impact": "High supply chain disruption risk"
    }
  ],
  "total_alerts": 5
}
```

---

### 8. Get Agent Reasoning
**GET** `/agents/reasoning`

Retrieve the reasoning process for all agents (for transparency).

**Response:**
```json
{
  "agents": {
    "supply_monitoring": {
      "name": "Supply Monitoring Agent",
      "role": "Data Collector and Normalizer",
      "reasoning": "Supply Monitoring Agent Reasoning:\n1. Validate all incoming data..."
    },
    "validation": { ... },
    "risk_analysis": { ... },
    "supervisor": { ... }
  }
}
```

---

### 9. Get Dashboard Data
**GET** `/dashboard`

Get complete data for dashboard visualization.

**Response:**
```json
{
  "suppliers": [ ... ],
  "summary": {
    "total_suppliers_monitored": 240,
    "phantom_stock_detected": 2,
    "status": "ATTENTION_REQUIRED"
  },
  "alerts": [ ... ],
  "critical_risks": [ ... ],
  "warnings": [ ... ]
}
```

---

## Error Responses

All endpoints return standard error format:

```json
{
  "error": "Error message description",
  "status_code": 400
}
```

**Common Status Codes:**
- `200`: Success
- `400`: Bad Request (missing data)
- `500`: Internal Server Error

---

## Usage Example

### JavaScript (Fetch)
```javascript
// Run analysis
fetch('http://localhost:5000/api/analysis/run', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' }
})
.then(res => res.json())
.then(data => console.log(data));

// Get alerts
fetch('http://localhost:5000/api/alerts')
.then(res => res.json())
.then(data => console.log(data.alerts));
```

### Python (Requests)
```python
import requests

# Run analysis
response = requests.post('http://localhost:5000/api/analysis/run')
data = response.json()

# Get risks
risks = requests.get('http://localhost:5000/api/risks').json()
```

### cURL
```bash
# Run analysis
curl -X POST http://localhost:5000/api/analysis/run

# Get dashboard data
curl http://localhost:5000/api/dashboard
```

---

## Agent Pipeline Flow

```
POST /api/analysis/run
    ↓
Supply Monitoring Agent (validates data)
    ↓
Validation Agent (predicts expected inventory)
    ↓
Risk Analysis Agent (calculates risk scores)
    ↓
Supervisor Agent (generates alerts)
    ↓
Response with alerts & recommendations
```

---

## Rate Limiting

Currently no rate limiting (hackathon prototype).
For production, implement rate limiting on critical endpoints.

---

## CORS

CORS is enabled for all origins (development mode).
For production, restrict to specific domains.
