"""
AIAG01 - Truly Agentic System (FastAPI)
Each agent is autonomous with clear input/output contracts
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator import AgentOrchestrator
from models.messages import AgentMessage

app = FastAPI(title="AIAG01 Agentic System", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = AgentOrchestrator()

# Supplier simulation data
def generate_sample_data():
    """Generate sample inventory data"""
    import random
    from datetime import datetime, timedelta
    
    suppliers = [
        {"id": "T1-001", "name": "Tier1 Electronics", "tier": 1, "capacity": 10000},
        {"id": "T2-001", "name": "Tier2 Parts Co", "tier": 2, "capacity": 5000},
        {"id": "T3-001", "name": "Tier3 Raw Materials", "tier": 3, "capacity": 3000},
    ]
    
    data = []
    for supplier in suppliers:
        production_rate = supplier["capacity"] * 0.7
        consumption_rate = production_rate * 0.8
        has_phantom = random.random() < 0.5
        
        for day in range(10):
            expected = production_rate - consumption_rate + random.randint(-100, 100)
            reported = expected * random.uniform(1.3, 1.8) if has_phantom else expected * random.uniform(0.95, 1.05)
            
            data.append({
                "supplier_id": supplier["id"],
                "supplier_name": supplier["name"],
                "tier": supplier["tier"],
                "date": (datetime.now() - timedelta(days=day)).strftime("%Y-%m-%d"),
                "reported_stock": max(0, int(reported)),
                "production_rate": int(production_rate),
                "consumption_rate": int(consumption_rate),
                "expected_stock": max(0, int(expected))
            })
    
    return data

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "system": "Truly Agentic Architecture",
        "agents": ["MonitoringAgent", "ValidationAgent", "RiskAgent", "SupervisorAgent"]
    }

@app.post("/api/analysis/run")
def run_analysis():
    """Run the autonomous agent pipeline"""
    inventory_data = generate_sample_data()
    result = orchestrator.run_pipeline(inventory_data)
    return result

@app.get("/api/agents/reasoning")
def get_reasoning():
    """Get reasoning from all agents"""
    return orchestrator.get_agent_reasoning()

@app.get("/api/alerts")
def get_alerts():
    """Get alerts from supervisor agent"""
    if "supervisor" not in orchestrator.agent_outputs:
        return {"error": "Run analysis first"}
    
    supervisor_output = orchestrator.agent_outputs["supervisor"]
    return {
        "alerts": supervisor_output["data"]["alerts"],
        "recommendations": supervisor_output["data"]["recommendations"],
        "total_alerts": supervisor_output["metadata"]["total_alerts"]
    }

@app.get("/api/suppliers")
def get_suppliers():
    """Get all supplier data"""
    suppliers = [
        {"id": "T1-001", "name": "Tier1 Electronics", "tier": 1, "capacity": 10000, "reliability": 0.95},
        {"id": "T1-002", "name": "Tier1 Components", "tier": 1, "capacity": 8000, "reliability": 0.90},
        {"id": "T2-001", "name": "Tier2 Parts Co", "tier": 2, "capacity": 5000, "reliability": 0.85},
        {"id": "T2-002", "name": "Tier2 Materials", "tier": 2, "capacity": 6000, "reliability": 0.80},
        {"id": "T2-003", "name": "Tier2 Assembly", "tier": 2, "capacity": 4500, "reliability": 0.88},
        {"id": "T3-001", "name": "Tier3 Raw Materials", "tier": 3, "capacity": 3000, "reliability": 0.75},
        {"id": "T3-002", "name": "Tier3 Metals Ltd", "tier": 3, "capacity": 3500, "reliability": 0.70},
        {"id": "T3-003", "name": "Tier3 Plastics Inc", "tier": 3, "capacity": 2800, "reliability": 0.78}
    ]
    return {
        "suppliers": suppliers,
        "total": len(suppliers),
        "by_tier": {
            "tier1": 2,
            "tier2": 3,
            "tier3": 3
        }
    }

@app.get("/api/predicted-stock")
def get_predicted_stock():
    """Get predicted stock for all suppliers"""
    if not orchestrator.agent_outputs:
        run_analysis()
    
    validation_output = orchestrator.agent_outputs.get("validation", {})
    validations = validation_output.get("data", {}).get("validations", [])
    
    predicted_stock = []
    for v in validations:
        predicted_stock.append({
            "supplier_id": v["supplier_id"],
            "supplier_name": v["supplier_name"],
            "tier": v["tier"],
            "reported_stock": v["reported_stock"],
            "predicted_stock": v["expected_stock"],
            "deviation": v["deviation"],
            "deviation_percentage": v["deviation_percentage"]
        })
    
    return {
        "predicted_stock": predicted_stock,
        "total": len(predicted_stock)
    }

@app.get("/api/risk-scores")
def get_risk_scores():
    """Get risk scores for all suppliers"""
    if not orchestrator.agent_outputs:
        run_analysis()
    
    risk_output = orchestrator.agent_outputs.get("risk", {})
    risk_assessments = risk_output.get("data", {}).get("risk_assessments", [])
    
    risk_scores = []
    for r in risk_assessments:
        risk_scores.append({
            "supplier_id": r["supplier_id"],
            "supplier_name": r["supplier_name"],
            "tier": r["tier"],
            "risk_score": r["risk_score"],
            "risk_level": r["risk_level"],
            "classification": r["classification"],
            "components": r.get("components", {})
        })
    
    return {
        "risk_scores": risk_scores,
        "total": len(risk_scores),
        "summary": {
            "critical": risk_output.get("metadata", {}).get("critical_count", 0),
            "warning": risk_output.get("metadata", {}).get("warning_count", 0),
            "normal": risk_output.get("metadata", {}).get("normal_count", 0)
        }
    }

@app.get("/api/dashboard")
def get_dashboard():
    """Get complete dashboard data"""
    if not orchestrator.agent_outputs:
        run_analysis()
    
    supervisor_output = orchestrator.agent_outputs["supervisor"]
    risk_output = orchestrator.agent_outputs["risk"]
    validation_output = orchestrator.agent_outputs["validation"]
    
    return {
        "summary": {
            "phantom_stock_detected": risk_output["metadata"]["critical_count"],
            "total_alerts": supervisor_output["metadata"]["total_alerts"],
            "status": supervisor_output["data"]["decision"],
            "total_suppliers": 8,
            "high_deviations": validation_output["metadata"]["high_deviation_count"]
        },
        "alerts": supervisor_output["data"]["alerts"],
        "critical_risks": risk_output["data"]["critical_risks"],
        "warnings": risk_output["data"]["warnings"]
    }

@app.get("/api/pipeline/trace")
def get_pipeline_trace():
    """Get full pipeline execution trace"""
    return {
        "pipeline": "MonitoringAgent → ValidationAgent → RiskAgent → SupervisorAgent",
        "agent_outputs": orchestrator.agent_outputs,
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

if __name__ == "__main__":
    import uvicorn
    print("Starting Truly Agentic System")
    print("4 Autonomous Agents Active")
    print("API: http://localhost:8001")
    print("Docs: http://localhost:8001/docs")
    print("\nAgent Pipeline:")
    print("  MonitoringAgent -> ValidationAgent -> RiskAgent -> SupervisorAgent")
    uvicorn.run(app, host="0.0.0.0", port=8001)
