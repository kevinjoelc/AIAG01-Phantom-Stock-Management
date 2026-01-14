# 🔄 Langflow Integration Guide

## Step-by-Step Instructions to Build Agent Pipeline in Langflow

---

## 📋 Prerequisites

1. **Install Langflow**
```bash
pip install langflow
```

2. **Start Langflow**
```bash
langflow run
```

3. **Access Langflow UI**
```
http://localhost:7860
```

---

## 🎯 Overview

We'll create 4 agent nodes connected in sequence:

```
Data Source → Monitoring Agent → Validation Agent → Risk Agent → Supervisor Agent → Output
```

---

## Step 1: Create New Flow

1. Open Langflow at http://localhost:7860
2. Click **"New Flow"**
3. Name it: **"AIAG01 Phantom Stock Detection"**
4. Click **"Create"**

---

## Step 2: Add Data Source Node

### 2.1 Add API Request Node
1. From left sidebar, search **"API Request"**
2. Drag to canvas
3. Configure:
   - **URL:** `http://localhost:8000/api/suppliers`
   - **Method:** `GET`
   - **Name:** `Data Source`

### 2.2 Alternative: Add Custom Python Node
1. Search **"Custom Component"** or **"Python Function"**
2. Drag to canvas
3. Add this code:

```python
import requests

def get_inventory_data():
    response = requests.get('http://localhost:8000/api/suppliers')
    data = response.json()
    return {
        "inventory_data": data["suppliers"]
    }

return get_inventory_data()
```

---

## Step 3: Add Monitoring Agent Node

### 3.1 Add Agent Node
1. Search **"Agent"** or **"Conversational Agent"**
2. Drag to canvas
3. Position to the right of Data Source

### 3.2 Configure Monitoring Agent
- **Agent Name:** `Monitoring Agent`
- **System Message:**
```
You are a Supply Monitoring Agent. Your role is to validate inventory data quality.

RULES:
1. Check if reported_stock >= 0
2. Verify production_rate > 0
3. Ensure all required fields are present
4. Flag any anomalies found

INPUT: Raw inventory data
OUTPUT: Validated data with quality flags
```

- **Tools:** Add Custom Tool (see below)

### 3.3 Add Custom Tool for Monitoring
Click **"Add Tool"** → **"Custom Tool"**

**Tool Name:** `validate_data`

**Tool Code:**
```python
def validate_data(inventory_data):
    """Validate inventory data quality"""
    anomalies = []
    processed = []
    
    for record in inventory_data:
        issues = []
        if record.get("reported_stock", 0) < 0:
            issues.append("negative_stock")
        if record.get("production_rate", 0) <= 0:
            issues.append("invalid_production")
        
        if issues:
            anomalies.append({
                "supplier_id": record.get("supplier_id"),
                "issues": issues
            })
        
        processed.append({
            **record,
            "data_quality": "poor" if issues else "good"
        })
    
    return {
        "processed_data": processed,
        "anomalies": anomalies,
        "total_records": len(processed)
    }
```

---

## Step 4: Add Validation Agent Node

### 4.1 Add Agent Node
1. Search **"Agent"**
2. Drag to canvas
3. Position to the right of Monitoring Agent

### 4.2 Configure Validation Agent
- **Agent Name:** `Validation Agent`
- **System Message:**
```
You are a Validation Agent. Your role is to predict expected inventory and detect deviations.

RULES:
1. Calculate deviation = |reported - expected| / expected
2. Flag deviations > 20% as high_deviation
3. Skip poor quality data

INPUT: Validated data from Monitoring Agent
OUTPUT: Validations with deviation percentages
```

### 4.3 Add Custom Tool
**Tool Name:** `calculate_deviations`

**Tool Code:**
```python
def calculate_deviations(processed_data):
    """Calculate inventory deviations"""
    validations = []
    high_deviations = []
    
    for record in processed_data:
        if record.get("data_quality") == "poor":
            continue
        
        reported = record.get("reported_stock", 0)
        expected = record.get("expected_stock", 0)
        
        if expected > 0:
            deviation = abs(reported - expected) / expected
        else:
            deviation = 0
        
        validation = {
            "supplier_id": record.get("supplier_id"),
            "supplier_name": record.get("supplier_name"),
            "tier": record.get("tier"),
            "reported_stock": reported,
            "expected_stock": expected,
            "deviation": deviation,
            "deviation_percentage": round(deviation * 100, 2)
        }
        
        if deviation > 0.20:
            validation["flag"] = "high_deviation"
            high_deviations.append(validation)
        
        validations.append(validation)
    
    return {
        "validations": validations,
        "high_deviations": high_deviations
    }
```

---

## Step 5: Add Risk Agent Node

### 5.1 Add Agent Node
1. Search **"Agent"**
2. Drag to canvas
3. Position to the right of Validation Agent

### 5.2 Configure Risk Agent
- **Agent Name:** `Risk Agent`
- **System Message:**
```
You are a Risk Analysis Agent. Your role is to calculate phantom stock risk scores.

FORMULA:
risk_score = (deviation × 50) + (tier × 6.67) + (history × 10)

CLASSIFICATION:
- Score > 70: CRITICAL (phantom stock likely)
- Score > 40: WARNING (monitor closely)
- Score ≤ 40: NORMAL

INPUT: Validations from Validation Agent
OUTPUT: Risk assessments with classifications
```

### 5.3 Add Custom Tool
**Tool Name:** `calculate_risk_scores`

**Tool Code:**
```python
def calculate_risk_scores(validations):
    """Calculate risk scores for phantom stock detection"""
    risk_assessments = []
    critical_risks = []
    warnings = []
    
    for validation in validations:
        deviation = validation.get("deviation", 0)
        tier = validation.get("tier", 1)
        historical_issues = 1 if deviation > 0.3 else 0
        
        # Calculate risk score
        deviation_score = min(deviation * 50, 50)
        tier_score = tier * 6.67
        history_score = min(historical_issues * 10, 30)
        total_risk_score = deviation_score + tier_score + history_score
        
        # Classify risk
        if total_risk_score > 70:
            risk_level = "CRITICAL"
            classification = "phantom_stock_likely"
        elif total_risk_score > 40:
            risk_level = "WARNING"
            classification = "monitor_closely"
        else:
            risk_level = "NORMAL"
            classification = "normal"
        
        risk_assessment = {
            "supplier_id": validation["supplier_id"],
            "supplier_name": validation["supplier_name"],
            "tier": tier,
            "risk_score": round(total_risk_score, 2),
            "risk_level": risk_level,
            "classification": classification,
            "deviation_percentage": validation.get("deviation_percentage", 0)
        }
        
        risk_assessments.append(risk_assessment)
        
        if risk_level == "CRITICAL":
            critical_risks.append(risk_assessment)
        elif risk_level == "WARNING":
            warnings.append(risk_assessment)
    
    return {
        "risk_assessments": risk_assessments,
        "critical_risks": critical_risks,
        "warnings": warnings
    }
```

---

## Step 6: Add Supervisor Agent Node

### 6.1 Add Agent Node
1. Search **"Agent"**
2. Drag to canvas
3. Position to the right of Risk Agent

### 6.2 Configure Supervisor Agent
- **Agent Name:** `Supervisor Agent`
- **System Message:**
```
You are a Supervisor Agent. Your role is to make final decisions and generate alerts.

RULES:
1. For CRITICAL risks: Generate CRITICAL alert, recommend IMMEDIATE_AUDIT (P0)
2. For WARNING risks: Generate WARNING alert, recommend INCREASE_MONITORING (P1)
3. Make final decision: ATTENTION_REQUIRED if any critical alerts, else NORMAL

INPUT: Risk assessments from Risk Agent
OUTPUT: Alerts and recommendations
```

### 6.3 Add Custom Tool
**Tool Name:** `generate_alerts`

**Tool Code:**
```python
from datetime import datetime

def generate_alerts(risk_assessments):
    """Generate alerts and recommendations"""
    alerts = []
    recommendations = []
    
    critical_risks = risk_assessments.get("critical_risks", [])
    warnings = risk_assessments.get("warnings", [])
    
    # Process critical risks
    for critical in critical_risks:
        alert = {
            "alert_id": f"ALERT-{critical['supplier_id']}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "severity": "CRITICAL",
            "supplier_name": critical["supplier_name"],
            "message": f"CRITICAL: Phantom stock detected at {critical['supplier_name']}",
            "risk_score": critical["risk_score"],
            "deviation": f"{critical['deviation_percentage']}%"
        }
        
        recommendation = {
            "supplier_id": critical["supplier_id"],
            "action": "IMMEDIATE_AUDIT",
            "description": f"Conduct immediate physical inventory audit at {critical['supplier_name']}",
            "priority": "P0"
        }
        
        alerts.append(alert)
        recommendations.append(recommendation)
    
    # Process warnings
    for warning in warnings:
        alert = {
            "alert_id": f"ALERT-{warning['supplier_id']}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "severity": "WARNING",
            "supplier_name": warning["supplier_name"],
            "message": f"WARNING: Potential disruption at {warning['supplier_name']}",
            "risk_score": warning["risk_score"]
        }
        
        recommendation = {
            "supplier_id": warning["supplier_id"],
            "action": "INCREASE_MONITORING",
            "description": f"Increase monitoring frequency for {warning['supplier_name']}",
            "priority": "P1"
        }
        
        alerts.append(alert)
        recommendations.append(recommendation)
    
    decision = "ATTENTION_REQUIRED" if len(critical_risks) > 0 else "NORMAL"
    
    return {
        "alerts": alerts,
        "recommendations": recommendations,
        "decision": decision,
        "total_alerts": len(alerts)
    }
```

---

## Step 7: Add Output Node

### 7.1 Add Text Output Node
1. Search **"Text Output"** or **"Output"**
2. Drag to canvas
3. Position to the right of Supervisor Agent

### 7.2 Configure Output
- **Name:** `Final Output`
- **Format:** JSON

---

## Step 8: Connect All Nodes

### 8.1 Connect Nodes in Sequence
1. **Data Source → Monitoring Agent**
   - Drag from Data Source output handle
   - Connect to Monitoring Agent input handle

2. **Monitoring Agent → Validation Agent**
   - Drag from Monitoring Agent output
   - Connect to Validation Agent input

3. **Validation Agent → Risk Agent**
   - Drag from Validation Agent output
   - Connect to Risk Agent input

4. **Risk Agent → Supervisor Agent**
   - Drag from Risk Agent output
   - Connect to Supervisor Agent input

5. **Supervisor Agent → Output**
   - Drag from Supervisor Agent output
   - Connect to Output node

### 8.2 Visual Verification
Your flow should look like:
```
[Data Source] → [Monitoring] → [Validation] → [Risk] → [Supervisor] → [Output]
```

---

## Step 9: Configure Agent Memory (Optional)

For each agent node:
1. Click on agent node
2. Find **"Memory"** section
3. Add **"Buffer Memory"** or **"Conversation Buffer Memory"**
4. This allows agents to maintain context

---

## Step 10: Test the Flow

### 10.1 Run the Flow
1. Click **"Run"** button (play icon) at top right
2. Watch data flow through each node
3. Check output in Output node

### 10.2 Debug Individual Nodes
1. Click on any node
2. Click **"Run Node"** to test individually
3. View output in node's output panel

### 10.3 View Logs
1. Click **"Logs"** tab at bottom
2. See execution logs for each agent
3. Debug any errors

---

## Step 11: Save and Export

### 11.1 Save Flow
1. Click **"Save"** button
2. Name: `AIAG01_Phantom_Stock_Detection`

### 11.2 Export Flow
1. Click **"Export"** button
2. Download JSON file
3. Share with team

### 11.3 Import Flow (for team members)
1. Click **"Import"**
2. Upload JSON file
3. Flow is ready to use

---

## 📊 Expected Output

When you run the flow, you should see:

```json
{
  "alerts": [
    {
      "severity": "CRITICAL",
      "message": "CRITICAL: Phantom stock detected at Tier3 Metals Ltd",
      "risk_score": 77.41
    }
  ],
  "recommendations": [
    {
      "action": "IMMEDIATE_AUDIT",
      "priority": "P0"
    }
  ],
  "decision": "ATTENTION_REQUIRED",
  "total_alerts": 2
}
```

---

## 🎨 Visual Flow Diagram

```
┌─────────────┐
│ Data Source │
│  (API Call) │
└──────┬──────┘
       │
       ↓
┌─────────────────┐
│ Monitoring Agent│
│ • Validate data │
│ • Check quality │
└──────┬──────────┘
       │
       ↓
┌──────────────────┐
│ Validation Agent │
│ • Calc deviations│
│ • Flag high dev  │
└──────┬───────────┘
       │
       ↓
┌─────────────┐
│ Risk Agent  │
│ • Calc risk │
│ • Classify  │
└──────┬──────┘
       │
       ↓
┌──────────────────┐
│ Supervisor Agent │
│ • Gen alerts     │
│ • Make decision  │
└──────┬───────────┘
       │
       ↓
┌─────────────┐
│   Output    │
│   (JSON)    │
└─────────────┘
```

---

## 🔧 Troubleshooting

### Issue: Nodes not connecting
**Solution:** Ensure output type matches input type. Use **"Text"** or **"JSON"** format.

### Issue: Agent not executing
**Solution:** Check system message is properly formatted. Verify tool code has no syntax errors.

### Issue: API call fails
**Solution:** Ensure backend is running at http://localhost:8000

### Issue: Tool not found
**Solution:** Make sure tool is properly added to agent. Check tool name matches.

---

## 🚀 Advanced Features

### Add Conditional Logic
1. Add **"If/Else"** node after Risk Agent
2. Route CRITICAL risks to one path
3. Route NORMAL to another path

### Add Parallel Processing
1. Duplicate Validation Agent
2. Process different supplier tiers in parallel
3. Merge results before Risk Agent

### Add Human-in-the-Loop
1. Add **"Human Input"** node after Supervisor
2. Require approval for CRITICAL alerts
3. Continue flow after approval

---

## 📝 Checklist

- [ ] Langflow installed and running
- [ ] Backend API running at http://localhost:8000
- [ ] Data Source node added and configured
- [ ] Monitoring Agent node added with validation tool
- [ ] Validation Agent node added with deviation tool
- [ ] Risk Agent node added with risk scoring tool
- [ ] Supervisor Agent node added with alert tool
- [ ] Output node added
- [ ] All nodes connected in sequence
- [ ] Flow tested and working
- [ ] Flow saved and exported

---

## ✅ You're Done!

Your agentic system is now integrated into Langflow with:
- ✅ 4 autonomous agents as separate nodes
- ✅ Clear data flow between agents
- ✅ Custom tools for each agent
- ✅ Visual pipeline representation
- ✅ Easy to modify and extend

**Next:** Try the Flowise integration guide!
