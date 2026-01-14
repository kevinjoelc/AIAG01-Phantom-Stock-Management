# 🤖 Truly Agentic System - AIAG01

## What Makes This "Truly Agentic"

Each agent is **autonomous** with:
- ✅ **Clear input contract** - Defined message format
- ✅ **Independent processing logic** - Own decision rules
- ✅ **Explicit output contract** - Structured message output
- ✅ **Communication protocol** - Agent-to-agent messaging

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENT PIPELINE                            │
└─────────────────────────────────────────────────────────────┘

Raw Data
   │
   ↓ [AgentMessage]
┌──────────────────┐
│ MonitoringAgent  │  INPUT:  Raw inventory data
│                  │  PROCESS: Validate quality, detect anomalies
│                  │  OUTPUT: MonitoringOutput (validated data)
└────────┬─────────┘
         │
         ↓ [MonitoringOutput]
┌──────────────────┐
│ ValidationAgent  │  INPUT:  MonitoringOutput
│                  │  PROCESS: Predict inventory, calc deviations
│                  │  OUTPUT: ValidationOutput (validations)
└────────┬─────────┘
         │
         ↓ [ValidationOutput]
┌──────────────────┐
│   RiskAgent      │  INPUT:  ValidationOutput
│                  │  PROCESS: Calculate risk scores
│                  │  OUTPUT: RiskOutput (risk assessments)
└────────┬─────────┘
         │
         ↓ [RiskOutput]
┌──────────────────┐
│ SupervisorAgent  │  INPUT:  RiskOutput
│                  │  PROCESS: Generate alerts & recommendations
│                  │  OUTPUT: SupervisorOutput (alerts)
└────────┬─────────┘
         │
         ↓ [SupervisorOutput]
    Dashboard
```

---

## Agent Contracts

### 1. MonitoringAgent

**INPUT:**
```python
AgentMessage(
    sender="DataSource",
    data={"inventory_data": [...]},
    metadata={}
)
```

**PROCESSING:**
- Validate reported_stock >= 0
- Check production_rate > 0
- Verify required fields present
- Flag anomalies

**OUTPUT:**
```python
MonitoringOutput(
    processed_data=[...],  # Validated records
    anomalies=[...],       # Quality issues
    stats={
        "total_records": 30,
        "anomaly_count": 2,
        "quality_rate": 0.93
    }
)
```

---

### 2. ValidationAgent

**INPUT:**
```python
MonitoringOutput(
    processed_data=[...],
    anomalies=[...],
    stats={...}
)
```

**PROCESSING:**
- Calculate deviation = |reported - expected| / expected
- Flag deviations > 20%
- Skip poor quality data

**OUTPUT:**
```python
ValidationOutput(
    validations=[...],      # All validations
    high_deviations=[...],  # Deviations > 20%
    stats={
        "total_validated": 28,
        "high_deviation_count": 5,
        "deviation_rate": 0.18
    }
)
```

---

### 3. RiskAgent

**INPUT:**
```python
ValidationOutput(
    validations=[...],
    high_deviations=[...],
    stats={...}
)
```

**PROCESSING:**
- Calculate risk_score = (deviation × 50) + (tier × 6.67) + (history × 10)
- Classify: CRITICAL (>70), WARNING (>40), NORMAL
- Categorize by severity

**OUTPUT:**
```python
RiskOutput(
    risk_assessments=[...],  # All assessments
    critical_risks=[...],    # Score > 70
    warnings=[...],          # Score > 40
    stats={
        "total_assessed": 28,
        "critical_count": 2,
        "warning_count": 3
    }
)
```

---

### 4. SupervisorAgent

**INPUT:**
```python
RiskOutput(
    risk_assessments=[...],
    critical_risks=[...],
    warnings=[...],
    stats={...}
)
```

**PROCESSING:**
- For CRITICAL: Generate alert + recommend IMMEDIATE_AUDIT
- For WARNING: Generate alert + recommend INCREASE_MONITORING
- Make final decision: ATTENTION_REQUIRED or NORMAL

**OUTPUT:**
```python
SupervisorOutput(
    alerts=[...],           # All alerts
    recommendations=[...],  # Action items
    decision="ATTENTION_REQUIRED",
    stats={
        "total_alerts": 5,
        "critical_alerts": 2,
        "warning_alerts": 3
    }
)
```

---

## Communication Flow

```python
# Step 1: Create initial message
message = AgentMessage(sender="DataSource", data={"inventory_data": data})

# Step 2: MonitoringAgent receives and processes
monitoring_output = monitoring_agent.execute(message)
# Returns: MonitoringOutput

# Step 3: ValidationAgent receives MonitoringOutput
validation_output = validation_agent.execute(monitoring_output)
# Returns: ValidationOutput

# Step 4: RiskAgent receives ValidationOutput
risk_output = risk_agent.execute(validation_output)
# Returns: RiskOutput

# Step 5: SupervisorAgent receives RiskOutput
supervisor_output = supervisor_agent.execute(risk_output)
# Returns: SupervisorOutput
```

---

## Quick Start

### 1. Install
```bash
cd agentic_system
pip install -r requirements.txt
```

### 2. Run
```bash
python main.py
```

### 3. Test
Visit http://localhost:8000/docs

---

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/health` | Health check |
| `POST /api/analysis/run` | Run agent pipeline |
| `GET /api/agents/reasoning` | Get agent logic |
| `GET /api/alerts` | Get alerts |
| `GET /api/dashboard` | Get dashboard data |
| `GET /api/pipeline/trace` | **See full communication flow** |

---

## Key Features

### 1. Base Agent Class
All agents inherit from `BaseAgent`:
```python
class BaseAgent(ABC):
    @abstractmethod
    def receive(self, message: AgentMessage) -> None:
        """Receive input"""
        pass
    
    @abstractmethod
    def process(self) -> None:
        """Process data"""
        pass
    
    @abstractmethod
    def send(self) -> AgentMessage:
        """Send output"""
        pass
```

### 2. Typed Messages
Each agent has its own message type:
- `MonitoringOutput`
- `ValidationOutput`
- `RiskOutput`
- `SupervisorOutput`

### 3. Agent Orchestrator
Manages the pipeline:
```python
orchestrator = AgentOrchestrator()
result = orchestrator.run_pipeline(data)
```

### 4. Console Logging
See agent communication in real-time:
```
STEP 1: MonitoringAgent
[MonitoringAgent] Received 30 records
[MonitoringAgent] Found 2 anomalies
[MonitoringAgent] Sending output to ValidationAgent

STEP 2: ValidationAgent
[ValidationAgent] Received 30 validated records
[ValidationAgent] Found 5 high deviations
[ValidationAgent] Sending output to RiskAgent
...
```

---

## File Structure

```
agentic_system/
├── main.py                    # FastAPI app
├── orchestrator.py            # Agent pipeline manager
├── models/
│   └── messages.py            # Message contracts
├── agents/
│   ├── base_agent.py          # Base agent class
│   ├── monitoring_agent.py    # Agent 1
│   ├── validation_agent.py    # Agent 2
│   ├── risk_agent.py          # Agent 3
│   └── supervisor_agent.py    # Agent 4
└── requirements.txt
```

---

## Testing Agent Communication

### View Pipeline Trace
```bash
curl http://localhost:8000/api/pipeline/trace
```

Response shows exact message flow:
```json
{
  "pipeline": "MonitoringAgent → ValidationAgent → RiskAgent → SupervisorAgent",
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
      "message_type": "MonitoringOutput"
    },
    ...
  ]
}
```

---

## Agent Independence

Each agent:
- ✅ Has its own state (`self.input_data`, `self.processed_data`)
- ✅ Makes independent decisions (own rules)
- ✅ Doesn't know about other agents (loose coupling)
- ✅ Communicates via messages only
- ✅ Can be tested in isolation

---

## Example: Testing Single Agent

```python
from agents.monitoring_agent import MonitoringAgent
from models.messages import AgentMessage

# Create agent
agent = MonitoringAgent()

# Create input message
message = AgentMessage(
    sender="Test",
    data={"inventory_data": [{"supplier_id": "T1-001", ...}]}
)

# Execute agent
output = agent.execute(message)

# Check output
print(output.data["processed_data"])
print(output.data["anomalies"])
```

---

## Why This Is Truly Agentic

| Feature | Previous Version | Truly Agentic Version |
|---------|------------------|----------------------|
| **Agent structure** | Functions | Classes with state |
| **Communication** | Direct function calls | Message passing |
| **Input/Output** | Implicit | Explicit contracts |
| **Independence** | Coupled | Autonomous |
| **Testability** | Hard | Easy (isolated) |
| **Traceability** | None | Full pipeline trace |
| **Extensibility** | Modify functions | Add new agents |

---

## Adding a New Agent

1. Create agent class:
```python
class NewAgent(BaseAgent):
    def receive(self, message):
        self.input_data = message.data
    
    def process(self):
        # Your logic here
        pass
    
    def send(self):
        return AgentMessage(...)
```

2. Add to orchestrator:
```python
self.new_agent = NewAgent()
new_output = self.new_agent.execute(previous_output)
```

3. Done! Agent is now part of pipeline.

---

## Console Output Example

```
============================================================
STARTING AGENTIC PIPELINE
============================================================

STEP 1: MonitoringAgent
------------------------------------------------------------
[MonitoringAgent] Received 30 records
[MonitoringAgent] Processing data quality checks...
[MonitoringAgent] Found 2 anomalies
[MonitoringAgent] Sending output to ValidationAgent

STEP 2: ValidationAgent
------------------------------------------------------------
[ValidationAgent] Received 30 validated records
[ValidationAgent] Calculating inventory deviations...
[ValidationAgent] Found 5 high deviations
[ValidationAgent] Sending output to RiskAgent

STEP 3: RiskAgent
------------------------------------------------------------
[RiskAgent] Received 30 validations
[RiskAgent] Calculating risk scores...
[RiskAgent] Found 2 critical risks, 3 warnings
[RiskAgent] Sending output to SupervisorAgent

STEP 4: SupervisorAgent
------------------------------------------------------------
[SupervisorAgent] Received 2 critical risks, 3 warnings
[SupervisorAgent] Making final decisions...
[SupervisorAgent] Generated 5 alerts, Decision: ATTENTION_REQUIRED
[SupervisorAgent] Final decision: ATTENTION_REQUIRED

============================================================
PIPELINE COMPLETE
============================================================
```

---

## Summary

This is a **truly agentic system** because:

1. ✅ Each agent is **autonomous** (own state, logic, decisions)
2. ✅ Agents **communicate via messages** (not direct calls)
3. ✅ Clear **input/output contracts** (typed messages)
4. ✅ **Loose coupling** (agents don't know about each other)
5. ✅ **Testable in isolation** (each agent independently)
6. ✅ **Traceable** (full pipeline visibility)
7. ✅ **Extensible** (easy to add new agents)

**This is production-grade agentic architecture! 🚀**
