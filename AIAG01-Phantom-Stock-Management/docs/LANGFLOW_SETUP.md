# Langflow / Flowise Integration Guide

## Overview
This guide shows how to integrate the AIAG01 Phantom Stock Management system with Langflow or Flowise to create a visual agent workflow.

---

## Option 1: Langflow Integration

### Step 1: Install Langflow
```bash
pip install langflow
```

### Step 2: Start Langflow
```bash
langflow run
```
Access at: http://localhost:7860

### Step 3: Create Agent Workflow

1. **Import Configuration**
   - Open Langflow UI
   - Click "Import Flow"
   - Upload `langflow_config/agent_workflow.json`

2. **Configure Agents**

   **Supply Monitoring Agent Node:**
   - Type: Agent
   - System Message: "You are a Supply Monitoring Agent. Validate inventory data and flag anomalies."
   - Tools: Add custom tool pointing to `/api/inventory/reported`

   **Validation Agent Node:**
   - Type: Agent
   - System Message: "You are a Validation Agent. Predict expected inventory and calculate deviations."
   - Tools: Add custom tool for inventory prediction logic

   **Risk Analysis Agent Node:**
   - Type: Agent
   - System Message: "You are a Risk Analysis Agent. Calculate phantom stock risk scores."
   - Tools: Add custom tool for risk calculation

   **Supervisor Agent Node:**
   - Type: Agent
   - System Message: "You are a Supervisor Agent. Generate alerts and recommendations."
   - Tools: Add custom tool for alert generation

3. **Connect Nodes**
   - Data Source → Monitoring Agent
   - Monitoring Agent → Validation Agent
   - Validation Agent → Risk Agent
   - Risk Agent → Supervisor Agent
   - Supervisor Agent → Output

4. **Add API Integration**
   - Add HTTP Request node
   - Configure: `POST http://localhost:5000/api/analysis/run`
   - Connect to agent pipeline

### Step 4: Test Workflow
- Click "Run" in Langflow
- Verify data flows through all agents
- Check output in dashboard

---

## Option 2: Flowise Integration

### Step 1: Install Flowise
```bash
npm install -g flowise
```

### Step 2: Start Flowise
```bash
npx flowise start
```
Access at: http://localhost:3000

### Step 3: Create Agent Chain

1. **Add Agent Nodes**
   - Drag "Conversational Agent" for each agent
   - Configure with respective roles

2. **Configure Each Agent**

   **Supply Monitoring Agent:**
   - Agent Name: Supply Monitoring Agent
   - System Message: "Validate and normalize supplier inventory data"
   - Tools: Custom API Tool → `/api/inventory/reported`

   **Validation Agent:**
   - Agent Name: Validation Agent
   - System Message: "Predict expected inventory and detect deviations"
   - Tools: Calculator, Custom Function

   **Risk Analysis Agent:**
   - Agent Name: Risk Analysis Agent
   - System Message: "Calculate phantom stock risk scores"
   - Tools: Custom Risk Calculator

   **Supervisor Agent:**
   - Agent Name: Supervisor Agent
   - System Message: "Generate alerts and recommendations"
   - Tools: Alert Generator

3. **Chain Agents**
   - Use "Agent Executor" to chain agents sequentially
   - Connect outputs to inputs

4. **Add Memory**
   - Add "Buffer Memory" to maintain context between agents

### Step 4: Deploy
- Click "Deploy" in Flowise
- Get API endpoint
- Integrate with frontend dashboard

---

## Agent Tool Definitions

### For Langflow/Flowise Custom Tools

**Tool 1: Data Validator**
```python
def validate_inventory_data(data):
    # Check for negative values, missing fields
    # Return validation status
    pass
```

**Tool 2: Inventory Predictor**
```python
def predict_inventory(production_rate, consumption_rate):
    expected = production_rate - consumption_rate
    return expected
```

**Tool 3: Risk Calculator**
```python
def calculate_risk(deviation, tier, history):
    risk_score = (deviation * 50) + (tier * 6.67) + (history * 10)
    return risk_score
```

**Tool 4: Alert Generator**
```python
def generate_alert(risk_score, supplier_id):
    if risk_score > 70:
        return {"severity": "CRITICAL", "action": "IMMEDIATE_AUDIT"}
    elif risk_score > 40:
        return {"severity": "WARNING", "action": "INCREASE_MONITORING"}
```

---

## Integration with Backend API

### Connect Langflow/Flowise to Flask Backend

1. **Add HTTP Request Node**
   - URL: `http://localhost:5000/api/analysis/run`
   - Method: POST
   - Headers: `Content-Type: application/json`

2. **Parse Response**
   - Extract agent outputs
   - Pass to respective agent nodes

3. **Display Results**
   - Connect to output node
   - Format as JSON for dashboard

---

## Testing the Integration

1. Start Flask backend: `python backend/app.py`
2. Start Langflow/Flowise
3. Run workflow
4. Verify:
   - All 4 agents execute
   - Data flows correctly
   - Alerts are generated
   - Dashboard receives data

---

## Troubleshooting

**Issue: Agents not communicating**
- Check API endpoints are accessible
- Verify CORS is enabled
- Check agent node connections

**Issue: No alerts generated**
- Verify risk thresholds in Risk Agent
- Check Supervisor Agent configuration
- Review agent reasoning logs

**Issue: Data not flowing**
- Check JSON format
- Verify API response structure
- Review node input/output mappings

---

## Advanced: Custom Agent Nodes

For advanced users, create custom Langflow components:

```python
# custom_monitoring_agent.py
from langflow import CustomComponent

class SupplyMonitoringAgent(CustomComponent):
    display_name = "Supply Monitoring Agent"
    
    def build(self, inventory_data: dict) -> dict:
        # Implement monitoring logic
        return validated_data
```

Import into Langflow for reusable agent components.
