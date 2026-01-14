# System Architecture Document

## AIAG01 - Agentic AI–Enabled Multi-Tier Manufacturing Phantom Stock Management

---

## 1. Executive Summary

This system addresses the critical problem of **phantom stock** in multi-tier manufacturing supply chains. Unlike traditional single-model approaches, we implement a **multi-agent architecture** where four autonomous AI agents collaborate to detect inventory discrepancies that are invisible to conventional ERP systems.

**Key Innovation:** Agent-based reasoning that mimics human supply chain analysts working together.

---

## 2. Problem Analysis

### 2.1 The Phantom Stock Problem

**Definition:** Phantom stock occurs when inventory appears in ERP systems but doesn't physically exist.

**Root Causes:**
- Tier-2 and Tier-3 supplier disruptions invisible to OEMs
- Manual data entry errors
- Theft or damage not reported
- System synchronization delays
- Supplier misreporting (intentional or accidental)

**Business Impact:**
- Production delays: $50K-$500K per incident
- Emergency expediting costs: 3-5x normal shipping
- Customer satisfaction decline
- Inventory carrying cost inefficiencies

### 2.2 Why Traditional Solutions Fail

1. **Single-tier visibility:** ERP systems only track Tier-1
2. **Reactive alerts:** Detect problems after production stops
3. **No predictive capability:** Can't anticipate disruptions
4. **Monolithic AI:** Single model can't handle multi-faceted analysis

---

## 3. Solution Architecture

### 3.1 Multi-Agent Design Philosophy

**Why Agents?**
- **Specialization:** Each agent masters one task
- **Modularity:** Easy to update individual agents
- **Transparency:** Clear reasoning at each step
- **Scalability:** Add new agents without rewriting system
- **Fault tolerance:** One agent failure doesn't crash system

### 3.2 Agent Hierarchy

```
                    ┌─────────────────────┐
                    │  SUPERVISOR AGENT   │
                    │  (Decision Maker)   │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
        ┌───────▼──────┐  ┌────▼─────┐  ┌────▼──────┐
        │  MONITORING  │  │VALIDATION│  │   RISK    │
        │    AGENT     │─▶│  AGENT   │─▶│  ANALYSIS │
        │              │  │          │  │   AGENT   │
        └──────────────┘  └──────────┘  └───────────┘
```

**Communication Protocol:**
- Sequential pipeline with feedback loops
- JSON-based message passing
- Escalation triggers for critical issues
- Shared context maintained by Supervisor

---

## 4. Agent Specifications

### 4.1 Supply Monitoring Agent

**Role:** First line of defense - data quality gatekeeper

**Responsibilities:**
1. Ingest inventory data from all tiers
2. Validate data completeness and accuracy
3. Detect logistics anomalies (shipment delays)
4. Normalize data formats across suppliers
5. Flag data quality issues immediately

**Decision Algorithm:**
```python
def process(data):
    if data.reported_stock < 0:
        escalate_to_supervisor("negative_stock")
    elif data.missing_critical_fields():
        escalate_to_supervisor("incomplete_data")
    elif data.shipment_delay > 7_days:
        flag_as("logistics_anomaly")
    
    return validated_data
```

**Inputs:**
- Supplier ID, name, tier
- Reported inventory quantity
- Production rate (units/day)
- Consumption rate (units/day)
- Shipment logs

**Outputs:**
- Validated data records
- Data quality flags
- Anomaly alerts

**Escalation Triggers:**
- Negative inventory values
- Missing required fields
- Shipment delays > 7 days

---

### 4.2 Validation Agent

**Role:** Predictive validator - the "should be" calculator

**Responsibilities:**
1. Calculate expected inventory using physics-based model
2. Compare reported vs expected inventory
3. Calculate deviation percentages
4. Flag significant mismatches
5. Provide confidence intervals

**Prediction Model:**
```
Expected Stock = (Production Rate × Days) - (Consumption Rate × Days) + Initial Stock

Deviation = |Reported - Expected| / Expected

Classification:
  - Deviation ≤ 20%: Normal variance
  - Deviation > 20%: High deviation (escalate)
```

**Why This Works:**
- Simple, explainable model (not black box)
- Based on conservation of mass principle
- Accounts for production and consumption
- Can be enhanced with ML later

**Inputs:**
- Validated supplier data
- Historical production capacity
- Lead times
- Consumption patterns

**Outputs:**
- Expected inventory predictions
- Deviation percentages
- High deviation flags

**Escalation Triggers:**
- Deviation > 20%
- Consistent under-reporting pattern
- Sudden inventory spikes

---

### 4.3 Risk Analysis Agent

**Role:** Phantom stock detector - the risk quantifier

**Responsibilities:**
1. Calculate multi-factor risk scores
2. Classify risk levels (CRITICAL/WARNING/NORMAL)
3. Estimate phantom stock probability
4. Consider tier depth impact
5. Factor in historical reliability

**Risk Scoring Formula:**
```
Risk Score = (Deviation × 50) + (Tier Depth × 20) + (Historical Issues × 30)

Where:
  - Deviation: 0-1 (normalized)
  - Tier Depth: 1-3 (Tier-3 = highest risk)
  - Historical Issues: 0-3 (past incident count)

Classification:
  - Score > 70: CRITICAL (phantom stock likely)
  - Score 40-70: WARNING (monitor closely)
  - Score < 40: NORMAL
```

**Why This Formula?**
- **Deviation (50%):** Primary indicator of mismatch
- **Tier Depth (20%):** Deeper tiers = less visibility
- **History (30%):** Past behavior predicts future

**Inputs:**
- Validation results (deviations)
- Supplier tier information
- Historical issue database

**Outputs:**
- Risk scores (0-100)
- Risk classifications
- Phantom stock probability
- Risk component breakdown

**Escalation Triggers:**
- Risk score > 70 (CRITICAL)
- Risk score > 40 (WARNING)
- Multiple suppliers in same tier flagged

---

### 4.4 Supervisor Agent

**Role:** Decision maker - the executive agent

**Responsibilities:**
1. Review all agent outputs for consistency
2. Verify risk classifications are justified
3. Generate actionable alerts
4. Create prioritized recommendations
5. Maintain audit trail
6. Generate executive summaries

**Decision Matrix:**

| Risk Score | Severity | Action | Priority |
|------------|----------|--------|----------|
| > 70 | CRITICAL | Immediate physical audit | P0 |
| 40-70 | WARNING | Increase monitoring frequency | P1 |
| < 40 | NORMAL | Continue standard monitoring | P2 |

**Alert Generation Logic:**
```python
def generate_alert(risk_assessment):
    if risk_assessment.score > 70:
        return Alert(
            severity="CRITICAL",
            action="IMMEDIATE_AUDIT",
            message=f"Phantom stock detected at {supplier}",
            recommendation="Conduct physical inventory count within 24 hours"
        )
    elif risk_assessment.score > 40:
        return Alert(
            severity="WARNING",
            action="INCREASE_MONITORING",
            message=f"Potential disruption at {supplier}",
            recommendation="Request daily inventory updates"
        )
```

**Inputs:**
- All agent outputs
- Risk assessments
- Data quality reports

**Outputs:**
- Critical alerts
- Actionable recommendations
- Executive summary
- Audit logs

**Escalation Triggers:**
- Multiple CRITICAL alerts
- System-wide data quality issues
- Cascading tier failures

---

## 5. Data Flow Architecture

### 5.1 Sequential Pipeline

```
[Suppliers] → [Monitoring] → [Validation] → [Risk Analysis] → [Supervisor] → [Dashboard]
     ↓             ↓              ↓               ↓                ↓
  Raw Data    Validated     Deviations      Risk Scores       Alerts
```

### 5.2 Message Format

**Standard Agent Message:**
```json
{
  "agent": "Agent Name",
  "timestamp": "ISO-8601",
  "data": { ... },
  "flags": ["flag1", "flag2"],
  "escalate": true/false,
  "reasoning": "Human-readable explanation"
}
```

### 5.3 State Management

- **Stateless Agents:** Each agent processes input → output
- **Shared Context:** Supervisor maintains global state
- **Persistence:** Results stored for historical analysis
- **Caching:** Recent analyses cached for dashboard

---

## 6. Multi-Tier Supplier Simulation

### 6.1 Supplier Hierarchy

```
OEM (Manufacturer)
  ↑
Tier-1 Suppliers (2) ← Direct visibility
  ↑
Tier-2 Suppliers (3) ← Limited visibility
  ↑
Tier-3 Suppliers (3) ← No visibility (phantom stock risk)
```

### 6.2 Simulation Parameters

**Per Supplier:**
- Capacity: 2,800 - 10,000 units
- Reliability: 0.70 - 0.95
- Production rate: 70% of capacity
- Consumption rate: 80% of production

**Phantom Stock Injection:**
- 30% of suppliers have phantom stock
- Reported stock: 1.3x - 1.8x actual
- Duration: 10 days (recent data)

### 6.3 Realism Features

- Random daily variance (±100 units)
- Shipment delays (20% probability)
- Tier-based reliability degradation
- Historical issue tracking

---

## 7. API Architecture

### 7.1 RESTful Design

**Base URL:** `http://localhost:5000/api`

**Endpoint Categories:**
1. **Data Endpoints:** `/suppliers`, `/inventory/reported`
2. **Analysis Endpoints:** `/analysis/run` (main orchestrator)
3. **Results Endpoints:** `/risks`, `/alerts`, `/dashboard`
4. **Transparency Endpoints:** `/agents/reasoning`

### 7.2 Main Orchestration Endpoint

**POST /api/analysis/run**

```python
def run_analysis():
    # 1. Generate/fetch data
    inventory_data = simulator.generate_inventory_data()
    
    # 2. Agent pipeline
    monitoring_output = monitoring_agent.process(inventory_data)
    validation_output = validation_agent.validate(monitoring_output)
    risk_output = risk_agent.analyze(validation_output)
    supervisor_output = supervisor_agent.decide(risk_output)
    
    # 3. Return results
    return {
        "status": "complete",
        "summary": supervisor_output.summary,
        "agent_outputs": {...}
    }
```

### 7.3 Response Format

All endpoints return JSON with standard structure:
```json
{
  "agent": "Agent Name",
  "data": { ... },
  "metadata": {
    "timestamp": "...",
    "processing_time_ms": 123
  }
}
```

---

## 8. Technology Stack

| Layer | Technology | Justification |
|-------|------------|---------------|
| **Backend** | Python 3.8+ | Rich AI/ML ecosystem, readable |
| **Web Framework** | Flask | Lightweight, perfect for hackathon |
| **API** | REST/JSON | Universal compatibility |
| **Agents** | Custom Python classes | Full control, transparent logic |
| **Simulation** | Python (random, datetime) | Built-in, no dependencies |
| **Frontend** | Vanilla HTML/JS | No build step, works anywhere |
| **Deployment** | Docker | Portable, reproducible |

**Why No Heavy Frameworks?**
- Faster development for hackathon
- Easier for judges to understand
- Modifiable by student teams
- No vendor lock-in

---

## 9. Scalability Considerations

### 9.1 Current Limitations (Hackathon Scope)

- In-memory data storage
- Single-threaded processing
- No authentication
- Simulated data only

### 9.2 Production Enhancements

**Data Layer:**
- PostgreSQL for persistent storage
- Redis for caching
- Time-series DB for historical data

**Processing:**
- Celery for async agent execution
- Message queue (RabbitMQ) for agent communication
- Parallel processing for multiple suppliers

**Security:**
- JWT authentication
- Role-based access control
- API rate limiting
- Encrypted data transmission

**Monitoring:**
- Prometheus metrics
- Grafana dashboards
- Agent performance tracking
- Alert delivery confirmation

---

## 10. Integration Points

### 10.1 Langflow/Flowise Integration

**Purpose:** Visual agent workflow editor

**Integration Method:**
1. Each agent becomes a node
2. Nodes connected via edges
3. API endpoints as data sources
4. Output to dashboard

**Benefits:**
- Non-technical users can modify workflow
- Visual debugging of agent pipeline
- Easy to add new agents
- Shareable workflow templates

### 10.2 ERP Integration (Future)

**Supported Systems:**
- SAP (BAPI/RFC)
- Oracle (REST API)
- Microsoft Dynamics (OData)

**Integration Pattern:**
```
ERP → Data Extractor → Agent Pipeline → Alert System → ERP
```

---

## 11. Testing Strategy

### 11.1 Unit Tests

- Each agent tested independently
- Mock data for predictable results
- Edge case coverage (negative values, missing data)

### 11.2 Integration Tests

- Full pipeline execution
- Agent communication verification
- API endpoint testing

### 11.3 Scenario Tests

- Normal operation (no phantom stock)
- Single supplier phantom stock
- Multiple supplier disruption
- Data quality issues

---

## 12. Deployment Architecture

### 12.1 Local Development

```
Developer Machine
  ├── Python Backend (port 5000)
  └── Dashboard (file://)
```

### 12.2 Cloud Deployment

```
Load Balancer
  ├── Backend Instance 1
  ├── Backend Instance 2
  └── Backend Instance N
       ↓
  Database Cluster
       ↓
  Cache Layer
```

---

## 13. Success Metrics

### 13.1 Functional Metrics

- ✅ Detects phantom stock with >90% accuracy
- ✅ Processes 1000+ suppliers in <5 seconds
- ✅ Generates actionable alerts within 1 minute
- ✅ Zero false negatives for critical issues

### 13.2 Business Metrics

- Reduce production delays by 40%
- Decrease emergency expediting costs by 60%
- Improve inventory accuracy to 98%+
- ROI: 5x within first year

---

## 14. Future Roadmap

**Phase 1 (Current):** Hackathon prototype
**Phase 2:** ML-enhanced prediction models
**Phase 3:** Real-time IoT sensor integration
**Phase 4:** Blockchain-based supplier verification
**Phase 5:** Autonomous corrective actions

---

## 15. Conclusion

This agentic AI architecture provides:
- **Transparency:** Every decision is explainable
- **Modularity:** Easy to enhance individual agents
- **Scalability:** Proven architecture pattern
- **Effectiveness:** Solves real phantom stock problem

**Key Differentiator:** Multi-agent collaboration vs. monolithic AI

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Authors:** AIAG01 Hackathon Team
