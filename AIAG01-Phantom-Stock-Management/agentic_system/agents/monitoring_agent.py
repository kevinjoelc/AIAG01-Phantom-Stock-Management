"""
Monitoring Agent - Autonomous data validation agent
"""
from agents.base_agent import BaseAgent
from models.messages import AgentMessage, MonitoringOutput
from datetime import datetime

class MonitoringAgent(BaseAgent):
    """
    Autonomous agent for data quality monitoring
    
    INPUT: Raw inventory data
    PROCESS: Validate data quality, detect anomalies
    OUTPUT: Validated data + anomalies
    """
    
    def __init__(self):
        super().__init__("MonitoringAgent", "Data Quality Validator")
        self.input_data = []
        self.processed_data = []
        self.anomalies = []
    
    def receive(self, message: AgentMessage) -> None:
        """Receive raw inventory data"""
        self.input_data = message.data.get("inventory_data", [])
        print(f"[{self.name}] Received {len(self.input_data)} records")
    
    def process(self) -> None:
        """Validate data quality and detect anomalies"""
        print(f"[{self.name}] Processing data quality checks...")
        
        self.processed_data = []
        self.anomalies = []
        
        for record in self.input_data:
            quality_issues = []
            
            # Rule 1: Check for negative stock
            if record.get("reported_stock", 0) < 0:
                quality_issues.append("negative_stock")
            
            # Rule 2: Check for invalid production rate
            if record.get("production_rate", 0) <= 0:
                quality_issues.append("invalid_production_rate")
            
            # Rule 3: Check for missing critical fields
            required_fields = ["supplier_id", "reported_stock", "production_rate"]
            if not all(field in record for field in required_fields):
                quality_issues.append("missing_fields")
            
            # Flag anomalies
            if quality_issues:
                self.anomalies.append({
                    "supplier_id": record.get("supplier_id"),
                    "issues": quality_issues,
                    "severity": "high"
                })
            
            # Add to processed data
            self.processed_data.append({
                **record,
                "monitored_at": datetime.now().isoformat(),
                "data_quality": "poor" if quality_issues else "good",
                "quality_issues": quality_issues
            })
        
        print(f"[{self.name}] Found {len(self.anomalies)} anomalies")
    
    def send(self) -> MonitoringOutput:
        """Send validated data to next agent"""
        output = MonitoringOutput(
            processed_data=self.processed_data,
            anomalies=self.anomalies,
            stats={
                "total_records": len(self.processed_data),
                "anomaly_count": len(self.anomalies),
                "quality_rate": (len(self.processed_data) - len(self.anomalies)) / len(self.processed_data) if self.processed_data else 0
            }
        )
        print(f"[{self.name}] Sending output to ValidationAgent")
        return output
    
    def get_reasoning(self) -> str:
        return """
        MonitoringAgent Decision Logic:
        1. Receive raw inventory data
        2. Check for negative stock values
        3. Validate production rates > 0
        4. Ensure all required fields present
        5. Flag anomalies with severity
        6. Send validated data to ValidationAgent
        """
