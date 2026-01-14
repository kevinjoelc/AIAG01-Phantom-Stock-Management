"""
AIAG01 - Phantom Stock Management Backend
Flask API with Agentic AI Architecture
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation.supplier_simulator import SupplierSimulator
from agents.supply_monitoring_agent import SupplyMonitoringAgent
from agents.validation_agent import ValidationAgent
from agents.risk_analysis_agent import RiskAnalysisAgent
from agents.supervisor_agent import SupervisorAgent

app = Flask(__name__)
CORS(app)

# Initialize components
simulator = SupplierSimulator()
monitoring_agent = SupplyMonitoringAgent()
validation_agent = ValidationAgent()
risk_agent = RiskAnalysisAgent()
supervisor_agent = SupervisorAgent()

# Global state (in production, use database)
current_inventory_data = []
current_shipment_data = []
agent_outputs = {}

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "AIAG01 Phantom Stock Management",
        "agents": {
            "monitoring": monitoring_agent.name,
            "validation": validation_agent.name,
            "risk_analysis": risk_agent.name,
            "supervisor": supervisor_agent.name
        }
    })

@app.route('/api/suppliers', methods=['GET'])
def get_suppliers():
    """Get all suppliers across all tiers"""
    suppliers = simulator.get_all_suppliers()
    return jsonify({
        "suppliers": suppliers,
        "total": len(suppliers),
        "by_tier": {
            "tier1": len([s for s in suppliers if s["tier"] == 1]),
            "tier2": len([s for s in suppliers if s["tier"] == 2]),
            "tier3": len([s for s in suppliers if s["tier"] == 3])
        }
    })

@app.route('/api/inventory/reported', methods=['GET'])
def get_reported_inventory():
    """Get reported inventory data"""
    global current_inventory_data
    
    days = request.args.get('days', default=30, type=int)
    current_inventory_data = simulator.generate_inventory_data(days_back=days)
    
    return jsonify({
        "inventory_data": current_inventory_data,
        "total_records": len(current_inventory_data)
    })

@app.route('/api/inventory/predicted', methods=['GET'])
def get_predicted_inventory():
    """Get predicted inventory (from Validation Agent)"""
    if not current_inventory_data:
        return jsonify({"error": "No inventory data available. Call /api/inventory/reported first"}), 400
    
    predictions = []
    for record in current_inventory_data:
        prediction = validation_agent.predict_expected_inventory(record)
        predictions.append(prediction)
    
    return jsonify({
        "predictions": predictions,
        "total": len(predictions)
    })

@app.route('/api/analysis/run', methods=['POST'])
def run_full_analysis():
    """
    Run complete agentic analysis pipeline
    This is the main endpoint that orchestrates all agents
    """
    global current_inventory_data, current_shipment_data, agent_outputs
    
    # Step 1: Generate fresh data
    current_inventory_data = simulator.generate_inventory_data(days_back=30)
    current_shipment_data = simulator.generate_shipment_data()
    
    # Step 2: Supply Monitoring Agent processes data
    monitoring_output = monitoring_agent.process_inventory_data(current_inventory_data)
    shipment_output = monitoring_agent.process_shipment_data(current_shipment_data)
    
    # Step 3: Validation Agent validates inventory
    validation_output = validation_agent.validate_inventory(monitoring_output["processed_data"])
    
    # Step 4: Risk Analysis Agent calculates risks
    risk_output = risk_agent.analyze_risks(validation_output["validations"])
    
    # Step 5: Supervisor Agent makes final decisions
    supervisor_output = supervisor_agent.verify_and_decide(risk_output, monitoring_output)
    
    # Store outputs
    agent_outputs = {
        "monitoring": monitoring_output,
        "shipment_monitoring": shipment_output,
        "validation": validation_output,
        "risk_analysis": risk_output,
        "supervisor": supervisor_output
    }
    
    # Generate summary
    summary = supervisor_agent.generate_summary(agent_outputs)
    
    return jsonify({
        "status": "analysis_complete",
        "summary": summary,
        "agent_outputs": agent_outputs
    })

@app.route('/api/risks', methods=['GET'])
def get_risks():
    """Get risk assessments"""
    if "risk_analysis" not in agent_outputs:
        return jsonify({"error": "No analysis available. Run /api/analysis/run first"}), 400
    
    return jsonify(agent_outputs["risk_analysis"])

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get active alerts"""
    if "supervisor" not in agent_outputs:
        return jsonify({"error": "No analysis available. Run /api/analysis/run first"}), 400
    
    return jsonify({
        "alerts": agent_outputs["supervisor"]["alerts"],
        "recommendations": agent_outputs["supervisor"]["recommendations"],
        "total_alerts": agent_outputs["supervisor"]["total_alerts"]
    })

@app.route('/api/agents/reasoning', methods=['GET'])
def get_agent_reasoning():
    """Get reasoning process for all agents"""
    return jsonify({
        "agents": {
            "supply_monitoring": {
                "name": monitoring_agent.name,
                "role": monitoring_agent.role,
                "reasoning": monitoring_agent.get_reasoning()
            },
            "validation": {
                "name": validation_agent.name,
                "role": validation_agent.role,
                "reasoning": validation_agent.get_reasoning()
            },
            "risk_analysis": {
                "name": risk_agent.name,
                "role": risk_agent.role,
                "reasoning": risk_agent.get_reasoning()
            },
            "supervisor": {
                "name": supervisor_agent.name,
                "role": supervisor_agent.role,
                "reasoning": supervisor_agent.get_reasoning()
            }
        }
    })

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_data():
    """Get complete dashboard data"""
    if not agent_outputs:
        # Run analysis if not done yet
        run_full_analysis()
    
    return jsonify({
        "suppliers": simulator.get_all_suppliers(),
        "summary": supervisor_agent.generate_summary(agent_outputs),
        "alerts": agent_outputs.get("supervisor", {}).get("alerts", []),
        "critical_risks": agent_outputs.get("risk_analysis", {}).get("critical_risks", []),
        "warnings": agent_outputs.get("risk_analysis", {}).get("warnings", [])
    })

if __name__ == '__main__':
    print("🚀 Starting AIAG01 Phantom Stock Management System")
    print("📊 Agentic AI Architecture Active")
    print("🔗 API available at http://localhost:5000")
    print("\n📋 Available Endpoints:")
    print("  GET  /api/health - Health check")
    print("  GET  /api/suppliers - List all suppliers")
    print("  POST /api/analysis/run - Run full agentic analysis")
    print("  GET  /api/risks - Get risk assessments")
    print("  GET  /api/alerts - Get active alerts")
    print("  GET  /api/agents/reasoning - Get agent reasoning")
    print("  GET  /api/dashboard - Get dashboard data")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
