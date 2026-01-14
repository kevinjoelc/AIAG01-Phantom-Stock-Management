"""
Supervisor Agent - Autonomous decision-making agent
"""
from agents.base_agent import BaseAgent
from models.messages import AgentMessage, SupervisorOutput
from datetime import datetime

class SupervisorAgent(BaseAgent):
    """
    Autonomous agent for final decision making
    
    INPUT: Risk assessments from RiskAgent
    PROCESS: Generate alerts and recommendations
    OUTPUT: Alerts + recommendations + final decision
    """
    
    def __init__(self):
        super().__init__("SupervisorAgent", "Decision Maker")
        self.input_risks = {}
        self.alerts = []
        self.recommendations = []
        self.final_decision = ""
    
    def receive(self, message: AgentMessage) -> None:
        """Receive risk assessments from RiskAgent"""
        self.input_risks = message.data
        critical_count = len(self.input_risks.get("critical_risks", []))
        warning_count = len(self.input_risks.get("warnings", []))
        print(f"[{self.name}] Received {critical_count} critical risks, {warning_count} warnings")
    
    def process(self) -> None:
        """Generate alerts and recommendations based on risk levels"""
        print(f"[{self.name}] Making final decisions...")
        
        self.alerts = []
        self.recommendations = []
        
        # Rule 1: Process critical risks
        for critical in self.input_risks.get("critical_risks", []):
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
            
            self.alerts.append(alert)
            self.recommendations.append(recommendation)
        
        # Rule 2: Process warnings
        for warning in self.input_risks.get("warnings", []):
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
            
            self.alerts.append(alert)
            self.recommendations.append(recommendation)
        
        # Rule 3: Make final decision
        critical_count = len([a for a in self.alerts if a["severity"] == "CRITICAL"])
        if critical_count > 0:
            self.final_decision = "ATTENTION_REQUIRED"
        else:
            self.final_decision = "NORMAL"
        
        print(f"[{self.name}] Generated {len(self.alerts)} alerts, Decision: {self.final_decision}")
    
    def send(self) -> SupervisorOutput:
        """Send final output (alerts and recommendations)"""
        output = SupervisorOutput(
            alerts=self.alerts,
            recommendations=self.recommendations,
            decision=self.final_decision,
            stats={
                "total_alerts": len(self.alerts),
                "critical_alerts": len([a for a in self.alerts if a["severity"] == "CRITICAL"]),
                "warning_alerts": len([a for a in self.alerts if a["severity"] == "WARNING"]),
                "decision_timestamp": datetime.now().isoformat()
            }
        )
        print(f"[{self.name}] Final decision: {self.final_decision}")
        return output
    
    def get_reasoning(self) -> str:
        return """
        SupervisorAgent Decision Logic:
        1. Receive risk assessments from RiskAgent
        2. For CRITICAL risks:
           - Generate CRITICAL alert
           - Recommend IMMEDIATE_AUDIT (P0)
        3. For WARNING risks:
           - Generate WARNING alert
           - Recommend INCREASE_MONITORING (P1)
        4. Make final decision:
           - ATTENTION_REQUIRED if any critical alerts
           - NORMAL otherwise
        5. Send alerts and recommendations to dashboard
        """
