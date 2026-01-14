"""
Agent Service - Orchestrates all AI agents
"""
from datetime import datetime
from typing import Dict, List
from services.supplier_service import SupplierService
from agents.monitoring_agent import monitoring_agent
from agents.validation_agent import validation_agent
from agents.risk_agent import risk_agent
from agents.supervisor_agent import supervisor_agent

class AgentService:
    def __init__(self):
        self.supplier_service = SupplierService()
        self.agent_outputs = {}
    
    def run_full_analysis(self) -> Dict:
        inventory_data = self.supplier_service.generate_inventory_data(30)
        
        monitoring_output = monitoring_agent(inventory_data)
        validation_output = validation_agent(monitoring_output["processed_data"])
        risk_output = risk_agent(validation_output["validations"])
        supervisor_output = supervisor_agent(risk_output, monitoring_output)
        
        self.agent_outputs = {
            "monitoring": monitoring_output,
            "validation": validation_output,
            "risk_analysis": risk_output,
            "supervisor": supervisor_output
        }
        
        summary = {
            "total_suppliers_monitored": monitoring_output["total_records"],
            "validations_performed": validation_output["total_validated"],
            "risks_identified": risk_output["critical_count"] + risk_output["warning_count"],
            "alerts_generated": supervisor_output["total_alerts"],
            "phantom_stock_detected": risk_output["critical_count"],
            "status": "ATTENTION_REQUIRED" if supervisor_output["critical_alerts"] > 0 else "NORMAL"
        }
        
        return {
            "status": "analysis_complete",
            "summary": summary,
            "agent_outputs": self.agent_outputs
        }
    
    def get_risks(self) -> Dict:
        if "risk_analysis" not in self.agent_outputs:
            self.run_full_analysis()
        return self.agent_outputs["risk_analysis"]
    
    def get_alerts(self) -> Dict:
        if "supervisor" not in self.agent_outputs:
            self.run_full_analysis()
        return {
            "alerts": self.agent_outputs["supervisor"]["alerts"],
            "recommendations": self.agent_outputs["supervisor"]["recommendations"],
            "total_alerts": self.agent_outputs["supervisor"]["total_alerts"]
        }
    
    def get_reasoning(self) -> Dict:
        return {
            "agents": {
                "supply_monitoring": {
                    "name": "Supply Monitoring Agent",
                    "role": "Data Collector and Normalizer",
                    "reasoning": "Validates data quality, checks for negative values and missing fields"
                },
                "validation": {
                    "name": "Validation Agent",
                    "role": "Predictive Validator",
                    "reasoning": "Predicts expected inventory and calculates deviations"
                },
                "risk_analysis": {
                    "name": "Risk Analysis Agent",
                    "role": "Phantom Stock Detector",
                    "reasoning": "Calculates risk scores using deviation, tier depth, and history"
                },
                "supervisor": {
                    "name": "Supervisor Agent",
                    "role": "Decision Maker",
                    "reasoning": "Generates alerts and recommendations based on risk levels"
                }
            }
        }
    
    def get_dashboard_data(self) -> Dict:
        if not self.agent_outputs:
            self.run_full_analysis()
        
        return {
            "suppliers": self.supplier_service.get_all_suppliers(),
            "summary": {
                "total_suppliers_monitored": self.agent_outputs["monitoring"]["total_records"],
                "phantom_stock_detected": self.agent_outputs["risk_analysis"]["critical_count"],
                "status": "ATTENTION_REQUIRED" if self.agent_outputs["supervisor"]["critical_alerts"] > 0 else "NORMAL"
            },
            "alerts": self.agent_outputs["supervisor"]["alerts"],
            "critical_risks": self.agent_outputs["risk_analysis"]["critical_risks"],
            "warnings": self.agent_outputs["risk_analysis"]["warnings"]
        }
