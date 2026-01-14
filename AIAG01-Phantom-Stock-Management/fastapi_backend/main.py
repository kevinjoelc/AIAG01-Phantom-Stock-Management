"""
AIAG01 - Phantom Stock Management Backend (FastAPI)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.supplier_service import SupplierService
from services.agent_service import AgentService

app = FastAPI(title="AIAG01 Phantom Stock Management", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

supplier_service = SupplierService()
agent_service = AgentService()

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AIAG01 Phantom Stock Management",
        "agents": ["monitoring", "validation", "risk_analysis", "supervisor"]
    }

@app.get("/api/suppliers")
def get_suppliers():
    suppliers = supplier_service.get_all_suppliers()
    return {
        "suppliers": suppliers,
        "total": len(suppliers),
        "by_tier": {
            "tier1": len([s for s in suppliers if s["tier"] == 1]),
            "tier2": len([s for s in suppliers if s["tier"] == 2]),
            "tier3": len([s for s in suppliers if s["tier"] == 3])
        }
    }

@app.get("/api/inventory/reported")
def get_reported_inventory(days: int = 30):
    inventory_data = supplier_service.generate_inventory_data(days)
    return {
        "inventory_data": inventory_data,
        "total_records": len(inventory_data)
    }

@app.post("/api/analysis/run")
def run_analysis():
    result = agent_service.run_full_analysis()
    return result

@app.get("/api/risks")
def get_risks():
    return agent_service.get_risks()

@app.get("/api/alerts")
def get_alerts():
    return agent_service.get_alerts()

@app.get("/api/agents/reasoning")
def get_agent_reasoning():
    return agent_service.get_reasoning()

@app.get("/api/dashboard")
def get_dashboard():
    return agent_service.get_dashboard_data()

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting AIAG01 Phantom Stock Management System")
    print("📊 Agentic AI Architecture Active")
    print("🔗 API: http://localhost:8000")
    print("📖 Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
