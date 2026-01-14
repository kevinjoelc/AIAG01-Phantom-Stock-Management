"""
Risk Analysis Agent
Calculates phantom stock probability and risk scores
"""
from typing import Dict, List

class RiskAnalysisAgent:
    def __init__(self):
        self.name = "Risk Analysis Agent"
        self.role = "Phantom Stock Detector"
        self.critical_threshold = 70
        self.warning_threshold = 40
        
    def calculate_risk_score(self, validation: Dict, historical_issues: int = 0) -> Dict:
        """
        Calculate risk score based on multiple factors
        Risk Score = (deviation * 50) + (tier_depth * 20) + (historical_issues * 30)
        """
        deviation = validation.get("deviation", 0)
        tier = validation.get("tier", 1)
        
        # Risk components
        deviation_score = min(deviation * 50, 50)  # Max 50 points
        tier_score = tier * 6.67  # Tier 3 = 20 points
        history_score = min(historical_issues * 10, 30)  # Max 30 points
        
        total_risk_score = deviation_score + tier_score + history_score
        
        # Classify risk level
        if total_risk_score > self.critical_threshold:
            risk_level = "CRITICAL"
            classification = "phantom_stock_likely"
            escalate = True
        elif total_risk_score > self.warning_threshold:
            risk_level = "WARNING"
            classification = "monitor_closely"
            escalate = True
        else:
            risk_level = "NORMAL"
            classification = "normal"
            escalate = False
        
        return {
            "supplier_id": validation["supplier_id"],
            "supplier_name": validation["supplier_name"],
            "tier": tier,
            "risk_score": round(total_risk_score, 2),
            "risk_level": risk_level,
            "classification": classification,
            "deviation_percentage": validation.get("deviation_percentage", 0),
            "reported_stock": validation.get("reported_stock", 0),
            "expected_stock": validation.get("expected_stock", 0),
            "escalate": escalate,
            "components": {
                "deviation_score": round(deviation_score, 2),
                "tier_score": round(tier_score, 2),
                "history_score": round(history_score, 2)
            }
        }
    
    def analyze_risks(self, validations: List[Dict]) -> Dict:
        """
        Analyze all validations and generate risk assessments
        """
        risk_assessments = []
        critical_risks = []
        warnings = []
        
        for validation in validations:
            # Simulate historical issues (in real system, fetch from database)
            historical_issues = 1 if validation.get("deviation", 0) > 0.3 else 0
            
            risk_assessment = self.calculate_risk_score(validation, historical_issues)
            risk_assessments.append(risk_assessment)
            
            if risk_assessment["risk_level"] == "CRITICAL":
                critical_risks.append(risk_assessment)
            elif risk_assessment["risk_level"] == "WARNING":
                warnings.append(risk_assessment)
        
        return {
            "agent": self.name,
            "risk_assessments": risk_assessments,
            "critical_risks": critical_risks,
            "warnings": warnings,
            "total_assessed": len(risk_assessments),
            "critical_count": len(critical_risks),
            "warning_count": len(warnings)
        }
    
    def get_reasoning(self) -> str:
        """Return agent's reasoning process"""
        return """
        Risk Analysis Agent Reasoning:
        1. Calculate risk score using weighted formula:
           - Deviation impact: 50% weight
           - Tier depth impact: 20% weight (deeper = riskier)
           - Historical issues: 30% weight
        2. Classify risk levels:
           - Score > 70: CRITICAL (phantom stock likely)
           - Score > 40: WARNING (monitor closely)
           - Score ≤ 40: NORMAL
        3. Escalate CRITICAL and WARNING to Supervisor
        4. Provide detailed risk breakdown for decision making
        """
