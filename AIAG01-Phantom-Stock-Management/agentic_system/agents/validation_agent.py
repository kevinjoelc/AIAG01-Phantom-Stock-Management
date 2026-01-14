"""
Validation Agent - Autonomous inventory prediction agent
"""
from agents.base_agent import BaseAgent
from models.messages import AgentMessage, ValidationOutput

class ValidationAgent(BaseAgent):
    """
    Autonomous agent for inventory validation
    
    INPUT: Validated data from MonitoringAgent
    PROCESS: Predict expected inventory, calculate deviations
    OUTPUT: Validations + high deviations
    """
    
    def __init__(self):
        super().__init__("ValidationAgent", "Inventory Predictor")
        self.input_data = []
        self.validations = []
        self.high_deviations = []
        self.deviation_threshold = 0.20
    
    def receive(self, message: AgentMessage) -> None:
        """Receive validated data from MonitoringAgent"""
        self.input_data = message.data.get("processed_data", [])
        print(f"[{self.name}] Received {len(self.input_data)} validated records")
    
    def process(self) -> None:
        """Predict expected inventory and calculate deviations"""
        print(f"[{self.name}] Calculating inventory deviations...")
        
        self.validations = []
        self.high_deviations = []
        
        for record in self.input_data:
            # Skip poor quality data
            if record.get("data_quality") == "poor":
                continue
            
            reported = record.get("reported_stock", 0)
            expected = record.get("expected_stock", 0)
            
            # Calculate deviation
            if expected > 0:
                deviation = abs(reported - expected) / expected
            else:
                deviation = 0
            
            validation = {
                "supplier_id": record.get("supplier_id"),
                "supplier_name": record.get("supplier_name"),
                "tier": record.get("tier"),
                "reported_stock": reported,
                "expected_stock": expected,
                "deviation": round(deviation, 3),
                "deviation_percentage": round(deviation * 100, 2)
            }
            
            # Rule: Flag high deviations
            if deviation > self.deviation_threshold:
                validation["flag"] = "high_deviation"
                validation["escalate"] = True
                self.high_deviations.append(validation)
            else:
                validation["flag"] = "normal"
                validation["escalate"] = False
            
            self.validations.append(validation)
        
        print(f"[{self.name}] Found {len(self.high_deviations)} high deviations")
    
    def send(self) -> ValidationOutput:
        """Send validations to RiskAgent"""
        output = ValidationOutput(
            validations=self.validations,
            high_deviations=self.high_deviations,
            stats={
                "total_validated": len(self.validations),
                "high_deviation_count": len(self.high_deviations),
                "deviation_rate": len(self.high_deviations) / len(self.validations) if self.validations else 0
            }
        )
        print(f"[{self.name}] Sending output to RiskAgent")
        return output
    
    def get_reasoning(self) -> str:
        return """
        ValidationAgent Decision Logic:
        1. Receive validated data from MonitoringAgent
        2. Calculate expected inventory (production - consumption)
        3. Compare reported vs expected
        4. Calculate deviation percentage
        5. Flag deviations > 20% as high_deviation
        6. Send validations to RiskAgent
        """
