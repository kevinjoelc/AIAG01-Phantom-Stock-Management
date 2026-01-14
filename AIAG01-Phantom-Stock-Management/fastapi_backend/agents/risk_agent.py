"""
Risk Analysis Agent - Calculates phantom stock risk scores
"""
from typing import Dict, List

def risk_agent(validations: List[Dict]) -> Dict:
    risk_assessments = []
    critical_risks = []
    warnings = []
    critical_threshold = 70
    warning_threshold = 40
    
    for validation in validations:
        deviation = validation.get("deviation", 0)
        tier = validation.get("tier", 1)
        historical_issues = 1 if deviation > 0.3 else 0
        
        deviation_score = min(deviation * 50, 50)
        tier_score = tier * 6.67
        history_score = min(historical_issues * 10, 30)
        
        total_risk_score = deviation_score + tier_score + history_score
        
        if total_risk_score > critical_threshold:
            risk_level = "CRITICAL"
            classification = "phantom_stock_likely"
            escalate = True
        elif total_risk_score > warning_threshold:
            risk_level = "WARNING"
            classification = "monitor_closely"
            escalate = True
        else:
            risk_level = "NORMAL"
            classification = "normal"
            escalate = False
        
        risk_assessment = {
            "supplier_id": validation["supplier_id"],
            "supplier_name": validation["supplier_name"],
            "tier": tier,
            "risk_score": round(total_risk_score, 2),
            "risk_level": risk_level,
            "classification": classification,
            "deviation_percentage": validation.get("deviation_percentage", 0),
            "reported_stock": validation.get("reported_stock", 0),
            "expected_stock": validation.get("expected_stock", 0),
            "escalate": escalate
        }
        
        risk_assessments.append(risk_assessment)
        
        if risk_level == "CRITICAL":
            critical_risks.append(risk_assessment)
        elif risk_level == "WARNING":
            warnings.append(risk_assessment)
    
    return {
        "agent": "Risk Analysis Agent",
        "risk_assessments": risk_assessments,
        "critical_risks": critical_risks,
        "warnings": warnings,
        "total_assessed": len(risk_assessments),
        "critical_count": len(critical_risks),
        "warning_count": len(warnings)
    }
