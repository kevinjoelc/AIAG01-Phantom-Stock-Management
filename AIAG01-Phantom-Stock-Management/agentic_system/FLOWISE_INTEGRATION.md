# 🌊 Flowise Integration Guide

## Step-by-Step Instructions to Build Agent Pipeline in Flowise

---

## 📋 Prerequisites

1. **Install Flowise**
```bash
npm install -g flowise
```

2. **Start Flowise**
```bash
npx flowise start
```

3. **Access Flowise UI**
```
http://localhost:3000
```

---

## 🎯 Overview

We'll create 4 agent nodes connected in sequence:

```
API Chain → Monitoring Agent → Validation Agent → Risk Agent → Supervisor Agent
```

---

## Step 1: Create New Chatflow

1. Open Flowise at http://localhost:3000
2. Click **"Add New"**
3. Name it: **"AIAG01 Phantom Stock Detection"**
4. Click **"Create"**

---

## Step 2: Add Data Source (API Chain)

### 2.1 Add API Chain Node
1. From left panel, search **"API Chain"** or **"Custom Tool"**
2. Drag **"API Chain"** to canvas
3. Position at the left

### 2.2 Configure API Chain
- **Name:** `Data Source`
- **API URL:** `http://localhost:8000/api/suppliers`
- **Method:** `GET`
- **Headers:** `Content-Type: application/json`

### 2.3 Alternative: Add Custom Function
1. Search **"Custom JS Function"**
2. Add this code:

```javascript
async function getInventoryData() {
    const response = await fetch('http://localhost:8000/api/suppliers');
    const data = await response.json();
    return JSON.stringify({
        inventory_data: data.suppliers
    });
}

return await getInventoryData();
```

---

## Step 3: Add Monitoring Agent

### 3.1 Add Conversational Agent
1. Search **"Conversational Agent"** or **"Agent"**
2. Drag to canvas
3. Position to the right of Data Source

### 3.2 Configure Agent
- **Agent Name:** `Monitoring Agent`
- **System Message:**
```
You are a Supply Monitoring Agent responsible for validating inventory data quality.

Your tasks:
1. Check if reported_stock is non-negative
2. Verify production_rate is positive
3. Ensure all required fields exist
4. Flag any data quality issues

Input: Raw inventory data
Output: Validated data with quality flags and anomaly list
```

### 3.3 Add Custom Tool
Click **"Add Tool"** → **"Custom Tool"**

**Tool Name:** `validate_inventory_data`

**Tool Description:** `Validates inventory data and flags quality issues`

**Tool Function:**
```javascript
async function validateInventoryData(inventoryData) {
    const data = JSON.parse(inventoryData);
    const anomalies = [];
    const processed = [];
    
    for (const record of data.inventory_data || data) {
        const issues = [];
        
        if ((record.reported_stock || 0) < 0) {
            issues.push("negative_stock");
        }
        if ((record.production_rate || 0) <= 0) {
            issues.push("invalid_production_rate");
        }
        
        if (issues.length > 0) {
            anomalies.push({
                supplier_id: record.supplier_id,
                issues: issues
            });
        }
        
        processed.push({
            ...record,
            data_quality: issues.length > 0 ? "poor" : "good",
            quality_issues: issues
        });
    }
    
    return JSON.stringify({
        processed_data: processed,
        anomalies: anomalies,
        total_records: processed.length,
        anomaly_count: anomalies.length
    });
}

return await validateInventoryData($input);
```

---

## Step 4: Add Validation Agent

### 4.1 Add Conversational Agent
1. Search **"Conversational Agent"**
2. Drag to canvas
3. Position to the right of Monitoring Agent

### 4.2 Configure Agent
- **Agent Name:** `Validation Agent`
- **System Message:**
```
You are a Validation Agent responsible for predicting expected inventory and detecting deviations.

Your tasks:
1. Calculate deviation = |reported - expected| / expected
2. Flag deviations greater than 20%
3. Skip records with poor data quality

Input: Validated data from Monitoring Agent
Output: Validations with deviation percentages and high deviation flags
```

### 4.3 Add Custom Tool
**Tool Name:** `calculate_inventory_deviations`

**Tool Description:** `Calculates deviations between reported and expected inventory`

**Tool Function:**
```javascript
async function calculateDeviations(validatedData) {
    const data = JSON.parse(validatedData);
    const processedData = data.processed_data || data;
    const validations = [];
    const highDeviations = [];
    
    for (const record of processedData) {
        if (record.data_quality === "poor") continue;
        
        const reported = record.reported_stock || 0;
        const expected = record.expected_stock || 0;
        
        let deviation = 0;
        if (expected > 0) {
            deviation = Math.abs(reported - expected) / expected;
        }
        
        const validation = {
            supplier_id: record.supplier_id,
            supplier_name: record.supplier_name,
            tier: record.tier,
            reported_stock: reported,
            expected_stock: expected,
            deviation: deviation,
            deviation_percentage: Math.round(deviation * 100 * 100) / 100
        };
        
        if (deviation > 0.20) {
            validation.flag = "high_deviation";
            validation.escalate = true;
            highDeviations.push(validation);
        } else {
            validation.flag = "normal";
            validation.escalate = false;
        }
        
        validations.push(validation);
    }
    
    return JSON.stringify({
        validations: validations,
        high_deviations: highDeviations,
        total_validated: validations.length,
        high_deviation_count: highDeviations.length
    });
}

return await calculateDeviations($input);
```

---

## Step 5: Add Risk Agent

### 5.1 Add Conversational Agent
1. Search **"Conversational Agent"**
2. Drag to canvas
3. Position to the right of Validation Agent

### 5.2 Configure Agent
- **Agent Name:** `Risk Agent`
- **System Message:**
```
You are a Risk Analysis Agent responsible for calculating phantom stock risk scores.

Risk Formula:
risk_score = (deviation × 50) + (tier × 6.67) + (historical_issues × 10)

Classification:
- Score > 70: CRITICAL (phantom stock likely)
- Score > 40: WARNING (monitor closely)
- Score ≤ 40: NORMAL

Input: Validations from Validation Agent
Output: Risk assessments with scores and classifications
```

### 5.3 Add Custom Tool
**Tool Name:** `calculate_risk_scores`

**Tool Description:** `Calculates risk scores for phantom stock detection`

**Tool Function:**
```javascript
async function calculateRiskScores(validationData) {
    const data = JSON.parse(validationData);
    const validations = data.validations || data;
    const riskAssessments = [];
    const criticalRisks = [];
    const warnings = [];
    
    for (const validation of validations) {
        const deviation = validation.deviation || 0;
        const tier = validation.tier || 1;
        const historicalIssues = deviation > 0.3 ? 1 : 0;
        
        // Calculate risk score components
        const deviationScore = Math.min(deviation * 50, 50);
        const tierScore = tier * 6.67;
        const historyScore = Math.min(historicalIssues * 10, 30);
        const totalRiskScore = deviationScore + tierScore + historyScore;
        
        // Classify risk level
        let riskLevel, classification, escalate;
        if (totalRiskScore > 70) {
            riskLevel = "CRITICAL";
            classification = "phantom_stock_likely";
            escalate = true;
        } else if (totalRiskScore > 40) {
            riskLevel = "WARNING";
            classification = "monitor_closely";
            escalate = true;
        } else {
            riskLevel = "NORMAL";
            classification = "normal";
            escalate = false;
        }
        
        const riskAssessment = {
            supplier_id: validation.supplier_id,
            supplier_name: validation.supplier_name,
            tier: tier,
            risk_score: Math.round(totalRiskScore * 100) / 100,
            risk_level: riskLevel,
            classification: classification,
            deviation_percentage: validation.deviation_percentage,
            reported_stock: validation.reported_stock,
            expected_stock: validation.expected_stock,
            escalate: escalate,
            components: {
                deviation_score: Math.round(deviationScore * 100) / 100,
                tier_score: Math.round(tierScore * 100) / 100,
                history_score: Math.round(historyScore * 100) / 100
            }
        };
        
        riskAssessments.push(riskAssessment);
        
        if (riskLevel === "CRITICAL") {
            criticalRisks.push(riskAssessment);
        } else if (riskLevel === "WARNING") {
            warnings.push(riskAssessment);
        }
    }
    
    return JSON.stringify({
        risk_assessments: riskAssessments,
        critical_risks: criticalRisks,
        warnings: warnings,
        total_assessed: riskAssessments.length,
        critical_count: criticalRisks.length,
        warning_count: warnings.length
    });
}

return await calculateRiskScores($input);
```

---

## Step 6: Add Supervisor Agent

### 6.1 Add Conversational Agent
1. Search **"Conversational Agent"**
2. Drag to canvas
3. Position to the right of Risk Agent

### 6.2 Configure Agent
- **Agent Name:** `Supervisor Agent`
- **System Message:**
```
You are a Supervisor Agent responsible for making final decisions and generating alerts.

Decision Rules:
1. For CRITICAL risks: Generate CRITICAL alert, recommend IMMEDIATE_AUDIT (Priority P0)
2. For WARNING risks: Generate WARNING alert, recommend INCREASE_MONITORING (Priority P1)
3. Final decision: ATTENTION_REQUIRED if any critical alerts exist, otherwise NORMAL

Input: Risk assessments from Risk Agent
Output: Alerts, recommendations, and final decision
```

### 6.3 Add Custom Tool
**Tool Name:** `generate_alerts_and_recommendations`

**Tool Description:** `Generates alerts and actionable recommendations`

**Tool Function:**
```javascript
async function generateAlerts(riskData) {
    const data = JSON.parse(riskData);
    const criticalRisks = data.critical_risks || [];
    const warnings = data.warnings || [];
    const alerts = [];
    const recommendations = [];
    
    // Process critical risks
    for (const critical of criticalRisks) {
        const timestamp = new Date().toISOString();
        const alertId = `ALERT-${critical.supplier_id}-${Date.now()}`;
        
        alerts.push({
            alert_id: alertId,
            severity: "CRITICAL",
            supplier_id: critical.supplier_id,
            supplier_name: critical.supplier_name,
            tier: critical.tier,
            message: `CRITICAL: Phantom stock detected at ${critical.supplier_name}`,
            risk_score: critical.risk_score,
            deviation: `${critical.deviation_percentage}%`,
            reported_stock: critical.reported_stock,
            expected_stock: critical.expected_stock,
            timestamp: timestamp
        });
        
        recommendations.push({
            supplier_id: critical.supplier_id,
            action: "IMMEDIATE_AUDIT",
            description: `Conduct immediate physical inventory audit at ${critical.supplier_name}`,
            priority: "P0",
            estimated_impact: "High supply chain disruption risk"
        });
    }
    
    // Process warnings
    for (const warning of warnings) {
        const timestamp = new Date().toISOString();
        const alertId = `ALERT-${warning.supplier_id}-${Date.now()}`;
        
        alerts.push({
            alert_id: alertId,
            severity: "WARNING",
            supplier_id: warning.supplier_id,
            supplier_name: warning.supplier_name,
            tier: warning.tier,
            message: `WARNING: Potential disruption at ${warning.supplier_name}`,
            risk_score: warning.risk_score,
            deviation: `${warning.deviation_percentage}%`,
            timestamp: timestamp
        });
        
        recommendations.push({
            supplier_id: warning.supplier_id,
            action: "INCREASE_MONITORING",
            description: `Increase monitoring frequency for ${warning.supplier_name}`,
            priority: "P1",
            estimated_impact: "Medium supply chain disruption risk"
        });
    }
    
    const decision = criticalRisks.length > 0 ? "ATTENTION_REQUIRED" : "NORMAL";
    
    return JSON.stringify({
        alerts: alerts,
        recommendations: recommendations,
        decision: decision,
        total_alerts: alerts.length,
        critical_alerts: criticalRisks.length,
        warning_alerts: warnings.length,
        decision_timestamp: new Date().toISOString()
    });
}

return await generateAlerts($input);
```

---

## Step 7: Add Output Node

### 7.1 Add Output Node
1. Search **"Output"** or **"Final Output"**
2. Drag to canvas
3. Position to the right of Supervisor Agent

### 7.2 Configure Output
- **Output Type:** JSON
- **Format:** Pretty Print

---

## Step 8: Connect All Nodes

### 8.1 Create Connections
1. **Data Source → Monitoring Agent**
   - Click output port of Data Source
   - Drag to input port of Monitoring Agent

2. **Monitoring Agent → Validation Agent**
   - Click output port of Monitoring Agent
   - Drag to input port of Validation Agent

3. **Validation Agent → Risk Agent**
   - Click output port of Validation Agent
   - Drag to input port of Risk Agent

4. **Risk Agent → Supervisor Agent**
   - Click output port of Risk Agent
   - Drag to input port of Supervisor Agent

5. **Supervisor Agent → Output**
   - Click output port of Supervisor Agent
   - Drag to input port of Output node

### 8.2 Verify Connections
Your flow should look like:
```
[API] → [Monitoring] → [Validation] → [Risk] → [Supervisor] → [Output]
```

---

## Step 9: Add Memory (Optional)

### 9.1 Add Buffer Memory
1. Search **"Buffer Memory"**
2. Drag to canvas (below agents)

### 9.2 Connect Memory to Agents
1. Connect Buffer Memory to each agent's memory input
2. This allows agents to maintain conversation context

---

## Step 10: Test the Chatflow

### 10.1 Run the Flow
1. Click **"Save Chatflow"** button
2. Click **"Test"** button at top right
3. Enter test input: `Run phantom stock analysis`
4. Watch data flow through each agent

### 10.2 View Agent Outputs
1. Click on each agent node
2. View intermediate outputs
3. Debug any issues

### 10.3 Check Final Output
1. View output in Output node
2. Verify alerts are generated
3. Check decision is correct

---

## Step 11: Deploy the Chatflow

### 11.1 Get API Endpoint
1. Click **"API"** tab
2. Copy the chatflow API endpoint
3. Example: `http://localhost:3000/api/v1/prediction/{chatflowId}`

### 11.2 Test API
```bash
curl -X POST http://localhost:3000/api/v1/prediction/{chatflowId} \
  -H "Content-Type: application/json" \
  -d '{"question": "Run phantom stock analysis"}'
```

### 11.3 Integrate with Dashboard
```javascript
fetch('http://localhost:3000/api/v1/prediction/{chatflowId}', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ question: 'Run analysis' })
})
.then(res => res.json())
.then(data => console.log(data));
```

---

## Step 12: Save and Share

### 12.1 Save Chatflow
1. Click **"Save"** button
2. Name: `AIAG01_Phantom_Stock_Detection`

### 12.2 Export Chatflow
1. Click **"Export"** button
2. Download JSON file
3. Share with team

### 12.3 Import Chatflow
1. Click **"Import"**
2. Upload JSON file
3. Chatflow is ready to use

---

## 📊 Expected Output

```json
{
  "alerts": [
    {
      "alert_id": "ALERT-T3-002-1705329022123",
      "severity": "CRITICAL",
      "supplier_name": "Tier3 Metals Ltd",
      "message": "CRITICAL: Phantom stock detected at Tier3 Metals Ltd",
      "risk_score": 77.41,
      "deviation": "54.8%"
    }
  ],
  "recommendations": [
    {
      "action": "IMMEDIATE_AUDIT",
      "description": "Conduct immediate physical inventory audit",
      "priority": "P0"
    }
  ],
  "decision": "ATTENTION_REQUIRED",
  "total_alerts": 2
}
```

---

## 🔧 Troubleshooting

### Issue: Nodes not connecting
**Solution:** Ensure output format is JSON. Check data types match.

### Issue: Tool not executing
**Solution:** Verify JavaScript syntax. Check $input variable is used correctly.

### Issue: API call fails
**Solution:** Ensure backend is running. Check CORS is enabled.

### Issue: Memory errors
**Solution:** Increase memory limit in Flowise settings.

---

## 📝 Checklist

- [ ] Flowise installed and running
- [ ] Backend API running at http://localhost:8000
- [ ] API Chain node added for data source
- [ ] Monitoring Agent with validation tool
- [ ] Validation Agent with deviation tool
- [ ] Risk Agent with risk scoring tool
- [ ] Supervisor Agent with alert tool
- [ ] Output node added
- [ ] All nodes connected
- [ ] Chatflow tested
- [ ] API endpoint obtained
- [ ] Chatflow saved and exported

---

## ✅ You're Done!

Your agentic system is now integrated into Flowise with:
- ✅ 4 autonomous agents as separate nodes
- ✅ Custom JavaScript tools for each agent
- ✅ Visual pipeline representation
- ✅ API endpoint for integration
- ✅ Easy to test and deploy

**Your phantom stock detection system is ready! 🚀**
