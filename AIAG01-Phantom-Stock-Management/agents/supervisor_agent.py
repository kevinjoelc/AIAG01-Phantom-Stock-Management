"""
Supervisor Agent
Verifies agent conclusions and triggers alerts
"""
from typing import Dict, List
from datetime import datetime

class SupervisorAgent:
    def __init__(self):
        self.name = "Supervisor Agent"
        self.role = "Decision Maker and Alert Generator"
        
    def verify_and_decide(self, risk_analysis: Dict, monitoring_data: Dict) -> Dict:
        """
        Verify conclusions from all agents and make final decisions
        """
        alerts = []
        recommendations = []
        
        # Process critical risks
        for critical in risk_analysis.get("critical_risks", []):
            alert = {
                "alert_id": f"ALERT-{critical['supplier_id']}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "severity": "CRITICAL",
                "supplier_id": critical["supplier_id"],
                "supplier_name": critical["supplier_name"],
                "tier": critical["tier"],
                "message": f"CRITICAL: Phantom stock detected at {critical['supplier_name']}",
                "risk_score": critical["risk_score"],
                "deviation": f"{critical['deviation_percentage']}%",
                "reported_stock": critical["reported_stock"],
                "expected_stock": critical["expected_stock"],
                "timestamp": datetime.now().isoformat()
            }
            
            recommendation = {
                "supplier_id": critical["supplier_id"],
                "action": "IMMEDIATE_AUDIT",
                "description": f"Conduct immediate physical inventory audit at {critical['supplier_name']}",
                "priority": "P0",
                "estimated_impact": "High supply chain disruption risk"
            }
            
            alerts.append(alert)
            recommendations.append(recommendation)
        
        # Process warnings
        for warning in risk_analysis.get("warnings", []):
            alert = {
                "alert_id": f"ALERT-{warning['supplier_id']}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "severity": "WARNING",
                "supplier_id": warning["supplier_id"],
                "supplier_name": warning["supplier_name"],
                "tier": warning["tier"],
                "message": f"WARNING: Potential disruption at {warning['supplier_name']}",
                "risk_score": warning["risk_score"],
                "deviation": f"{warning['deviation_percentage']}%",
                "timestamp": datetime.now().isoformat()
            }
            
            recommendation = {
                "supplier_id": warning["supplier_id"],
                "action": "INCREASE_MONITORING",
                "description": f"Increase monitoring frequency for {warning['supplier_name']}",
                "priority": "P1",
                "estimated_impact": "Medium supply chain disruption risk"
            }
            
            alerts.append(alert)
            recommendations.append(recommendation)
        
        # Check for data quality issues from monitoring agent
        if monitoring_data.get("anomaly_count", 0) > 0:
            for anomaly in monitoring_data.get("anomalies", []):
                alert = {
                    "alert_id": f"ALERT-DQ-{anomaly['supplier_id']}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "severity": "HIGH",
                    "supplier_id": anomaly["supplier_id"],
                    "message": f"Data quality issues detected: {', '.join(anomaly['issues'])}",
                    "timestamp": datetime.now().isoformat()
                }
                alerts.append(alert)
        
        return {
            "agent": self.name,
            "alerts": alerts,
            "recommendations": recommendations,
            "total_alerts": len(alerts),
            "critical_alerts": len([a for a in alerts if a["severity"] == "CRITICAL"]),
            "warning_alerts": len([a for a in alerts if a["severity"] == "WARNING"]),
            "decision_timestamp": datetime.now().isoformat()
        }
    
    def generate_summary(self, all_agent_outputs: Dict) -> Dict:
        """
        Generate executive summary of the entire analysis
        """
        return {
            "agent": self.name,
            "summary": {
                "total_suppliers_monitored": all_agent_outputs.get("monitoring", {}).get("total_records", 0),
                "validations_performed": all_agent_outputs.get("validation", {}).get("total_validated", 0),
                "risks_identified": all_agent_outputs.get("risk_analysis", {}).get("critical_count", 0) + 
                                   all_agent_outputs.get("risk_analysis", {}).get("warning_count", 0),
                "alerts_generated": all_agent_outputs.get("supervisor", {}).get("total_alerts", 0),
                "phantom_stock_detected": all_agent_outputs.get("risk_analysis", {}).get("critical_count", 0),
                "status": "ATTENTION_REQUIRED" if all_agent_outputs.get("supervisor", {}).get("critical_alerts", 0) > 0 else "NORMAL"
            }
        }
    
    def get_reasoning(self) -> str:
        """Return agent's reasoning process"""
        return """
        Supervisor Agent Reasoning:
        1. Review all agent outputs for consistency
        2. Verify risk classifications are justified
        3. Generate alerts based on severity:
           - CRITICAL (risk > 70): Immediate audit required
           - WARNING (risk > 40): Increase monitoring
        4. Create actionable recommendations with priority
        5. Check for data quality issues from monitoring
        6. Generate executive summary for dashboard
        7. Log all decisions for audit trail
        """
