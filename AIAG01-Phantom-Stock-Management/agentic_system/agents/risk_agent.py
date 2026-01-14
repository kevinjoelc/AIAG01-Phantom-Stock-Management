"""
Risk Agent - Autonomous phantom stock detection agent
"""
from agents.base_agent import BaseAgent
from models.messages import AgentMessage, RiskOutput

class RiskAgent(BaseAgent):
    """
    Autonomous agent for risk assessment
    
    INPUT: Validations from ValidationAgent
    PROCESS: Calculate risk scores, classify phantom stock
    OUTPUT: Risk assessments + critical risks + warnings
    """
    
    def __init__(self):
        super().__init__("RiskAgent", "Phantom Stock Detector")
        self.input_validations = []
        self.risk_assessments = []
        self.critical_risks = []
        self.warnings = []
        self.critical_threshold = 70
        self.warning_threshold = 40
    
    def receive(self, message: AgentMessage) -> None:
        """Receive validations from ValidationAgent"""
        self.input_validations = message.data.get("validations", [])
        print(f"[{self.name}] Received {len(self.input_validations)} validations")
    
    def process(self) -> None:
        """Calculate risk scores and classify phantom stock"""
        print(f"[{self.name}] Calculating risk scores...")
        
        self.risk_assessments = []
        self.critical_risks = []
        self.warnings = []
        
        for validation in self.input_validations:
            # Extract factors
            deviation = validation.get("deviation", 0)
            tier = validation.get("tier", 1)
            
            # Simulate historical issues (in production, fetch from DB)
            historical_issues = 1 if deviation > 0.3 else 0
            
            # Calculate risk score components
            deviation_score = min(deviation * 50, 50)  # Max 50 points
            tier_score = tier * 6.67  # Tier-3 = 20 points
            history_score = min(historical_issues * 10, 30)  # Max 30 points
            
            total_risk_score = deviation_score + tier_score + history_score
            
            # Rule: Classify risk level
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
                "escalate": escalate,
                "components": {
                    "deviation_score": round(deviation_score, 2),
                    "tier_score": round(tier_score, 2),
                    "history_score": round(history_score, 2)
                }
            }
            
            self.risk_assessments.append(risk_assessment)
            
            # Categorize by risk level
            if risk_level == "CRITICAL":
                self.critical_risks.append(risk_assessment)
            elif risk_level == "WARNING":
                self.warnings.append(risk_assessment)
        
        print(f"[{self.name}] Found {len(self.critical_risks)} critical risks, {len(self.warnings)} warnings")
    
    def send(self) -> RiskOutput:
        """Send risk assessments to SupervisorAgent"""
        output = RiskOutput(
            risk_assessments=self.risk_assessments,
            critical_risks=self.critical_risks,
            warnings=self.warnings,
            stats={
                "total_assessed": len(self.risk_assessments),
                "critical_count": len(self.critical_risks),
                "warning_count": len(self.warnings),
                "normal_count": len(self.risk_assessments) - len(self.critical_risks) - len(self.warnings)
            }
        )
        print(f"[{self.name}] Sending output to SupervisorAgent")
        return output
    
    def get_reasoning(self) -> str:
        return """
        RiskAgent Decision Logic:
        1. Receive validations from ValidationAgent
        2. Calculate risk score: (deviation × 50) + (tier × 6.67) + (history × 10)
        3. Classify risk levels:
           - Score > 70: CRITICAL (phantom stock likely)
           - Score > 40: WARNING (monitor closely)
           - Score ≤ 40: NORMAL
        4. Categorize risks by severity
        5. Send risk assessments to SupervisorAgent
        """
