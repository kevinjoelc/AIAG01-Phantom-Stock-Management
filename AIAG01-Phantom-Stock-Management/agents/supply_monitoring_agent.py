"""
Supply Monitoring Agent
Collects and normalizes inventory, production, and shipment data
"""
from typing import Dict, List
from datetime import datetime

class SupplyMonitoringAgent:
    def __init__(self):
        self.name = "Supply Monitoring Agent"
        self.role = "Data Collector and Normalizer"
        
    def process_inventory_data(self, inventory_data: List[Dict]) -> Dict:
        """
        Process and validate incoming inventory data
        Returns structured data with quality flags
        """
        processed_data = []
        anomalies = []
        
        for record in inventory_data:
            # Data quality checks
            quality_issues = []
            
            if record["reported_stock"] < 0:
                quality_issues.append("negative_stock")
            
            if record["production_rate"] <= 0:
                quality_issues.append("invalid_production_rate")
            
            # Check for missing critical fields
            required_fields = ["supplier_id", "reported_stock", "production_rate"]
            if not all(field in record for field in required_fields):
                quality_issues.append("missing_fields")
            
            # Flag anomalies
            if quality_issues:
                anomalies.append({
                    "supplier_id": record["supplier_id"],
                    "issues": quality_issues,
                    "severity": "high",
                    "escalate": True
                })
            
            # Add monitoring metadata
            processed_record = {
                **record,
                "monitored_at": datetime.now().isoformat(),
                "data_quality": "poor" if quality_issues else "good",
                "quality_issues": quality_issues
            }
            
            processed_data.append(processed_record)
        
        return {
            "agent": self.name,
            "processed_data": processed_data,
            "anomalies": anomalies,
            "total_records": len(processed_data),
            "anomaly_count": len(anomalies)
        }
    
    def process_shipment_data(self, shipment_data: List[Dict]) -> Dict:
        """
        Process shipment logs and flag logistics anomalies
        """
        logistics_anomalies = []
        
        for shipment in shipment_data:
            if shipment["delay_days"] > 7:
                logistics_anomalies.append({
                    "supplier_id": shipment["supplier_id"],
                    "shipment_id": shipment["shipment_id"],
                    "delay_days": shipment["delay_days"],
                    "flag": "logistics_anomaly",
                    "escalate": True
                })
        
        return {
            "agent": self.name,
            "shipment_data": shipment_data,
            "logistics_anomalies": logistics_anomalies,
            "total_shipments": len(shipment_data),
            "delayed_shipments": len(logistics_anomalies)
        }
    
    def get_reasoning(self) -> str:
        """Return agent's reasoning process"""
        return """
        Supply Monitoring Agent Reasoning:
        1. Validate all incoming data for completeness
        2. Check for negative or impossible values
        3. Flag data quality issues immediately
        4. Identify logistics anomalies (delays > 7 days)
        5. Escalate critical issues to Supervisor
        6. Pass clean data to Validation Agent
        """
