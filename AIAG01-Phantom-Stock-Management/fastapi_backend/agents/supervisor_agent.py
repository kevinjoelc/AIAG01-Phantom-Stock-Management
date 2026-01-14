"""
Supervisor Agent - Makes final decisions and generates alerts
"""
from datetime import datetime
from typing import Dict

def supervisor_agent(risk_analysis: Dict, monitoring_data: Dict) -> Dict:
    alerts = []
    recommendations = []
    
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
    
    for anomaly in monitoring_data.get("anomalies", []):
        alert = {
            "alert_id": f"ALERT-DQ-{anomaly['supplier_id']}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "severity": "HIGH",
            "supplier_id": anomaly["supplier_id"],
            "message": f"Data quality issues: {', '.join(anomaly['issues'])}",
            "timestamp": datetime.now().isoformat()
        }
        alerts.append(alert)
    
    return {
        "agent": "Supervisor Agent",
        "alerts": alerts,
        "recommendations": recommendations,
        "total_alerts": len(alerts),
        "critical_alerts": len([a for a in alerts if a["severity"] == "CRITICAL"]),
        "warning_alerts": len([a for a in alerts if a["severity"] == "WARNING"]),
        "decision_timestamp": datetime.now().isoformat()
    }
